"""Server module for handling HTTP and WebSocket connections, and redirecting operations to the backend."""

import logging
import sys
import time
import traceback
import uuid
from types import SimpleNamespace
from typing import Any, Callable, Coroutine, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from clinguin.server.backends import ClingoBackend
from clinguin.utils.errors import get_server_error_alert

from ..utils.logging import colored, configure_logging

log = logging.getLogger(__name__)


class OperationRequest(BaseModel):
    """Request body for the operation endpoint."""

    operation: str
    client_version: int


class Server:
    """FastAPI server for handling HTTP and WebSocket connections."""

    def __init__(
        self,
        backend_class: ClingoBackend,
        backend_args: SimpleNamespace,
        port: int = 8000,
        host: str = "127.0.0.1",
        multi: bool = False,
        log_level: Optional[int] = None,
    ):
        """Initialize the server with the given port and host.
        Args:
            port (int): The port to run the server on (8000 by default).
            host (str): The host to run the server on (Local host by default, pass 0.0.0.0 to allow external access).
            multi (bool): Uses one backend instance per client if True.
            log_level (int): The log level for the server
        """
        self.backend_class = backend_class
        self.backend_args = backend_args
        self.port = port
        self.host = host
        self.multi = multi
        self.app = FastAPI()
        self.sessions: dict[str, WebSocket] = {}
        self.backends: dict[str, ClingoBackend] = {}
        self.version = 1

        if log_level is not None:
            configure_logging(
                stream=sys.stderr, level=log_level, use_color=True
            )  # Set up logging globally # nocoverage

        # Add middleware for request logging
        self.app.middleware("http")(self.log_requests)

        self.app.get("/info")(self.get_info)
        self.app.post("/operation")(self.execute_operation)
        self.app.websocket("/ws")(self.websocket_endpoint)

    def get_backend(self, session_id: str) -> ClingoBackend:
        """Get the backend for the given session ID."""
        if self.multi:
            if session_id not in self.backends:
                self.backends[session_id] = self.backend_class(args=self.backend_args)
            return self.backends[session_id]
        return self.backend_class(args=self.backend_args)

    def get_session_from_request(self, fastapi_request: Request) -> str:
        """Get the backend by inspecting the fastapi request."""
        initiator_session_id = fastapi_request.headers.get("session-id")
        if not initiator_session_id:
            log.error("Missing session ID in headers.")
            raise HTTPException(
                status_code=400,
                detail="Missing session ID in headers.",
            )
        return initiator_session_id

    def run(self) -> None:
        """Run the FastAPI server."""
        log.info("🚀 Starting server on %s:%s", self.host, self.port)
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="warning")

    async def log_requests(
        self, request: Request, call_next: Callable[[Request], Coroutine[Any, Any, Response]]
    ) -> Response:
        """Middleware to log details of every request."""
        log.info(colored(f"=>=>=>=>=>=>=> {request.method}", "green"))
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        log.debug("Completed in %.2fs with status %s", duration, response.status_code)
        log.info(colored(f"<------------- {response.status_code}", "green"))
        return response

    # ---------- HTTP endpoints ----------

    async def get_info(self, fastapi_request: Request) -> dict[str, int | str]:
        """Retrieve server status or session information."""
        session = self.get_session_from_request(fastapi_request)
        backend = self.get_backend(session)
        response = {"status": "running", "version": self.version, "active_sessions": len(self.sessions)}
        try:
            json = backend.get()
            print(json)
            self.last_response = json
            response.update(json)
            log.debug("Response: %s", response)
        except Exception as e:
            log.error("Handling global exception in endpoint")
            log.error(e)
            log.error(traceback.format_exc())
            response.update(get_server_error_alert(str(e), self.last_response))
        return JSONResponse(content=response)

    async def execute_operation(self, request_body: OperationRequest, fastapi_request: Request) -> dict[str, Any]:
        """Execute an operation provided by the client."""

        if request_body.client_version < self.version:
            log.warning("Client version is outdated.")
            raise HTTPException(
                status_code=409,
                detail="Outdated version. Please sync with the latest version.",
            )

        # Get the session ID from the request headers
        session = self.get_session_from_request(fastapi_request)
        self.get_backend(session)

        # TODO call actual operation
        # Example operation handling
        operation_result = {"message": f"Executed operation: {request_body.operation}"}

        # Increment version and notify all clients in single-backend mode
        self.version += 1
        await self.notify_clients(exclude_session_id=session)

        return {"result": operation_result, "version": self.version}

    # ---------- WebSocket endpoint ----------

    async def websocket_endpoint(self, websocket: WebSocket) -> None:
        """Handle WebSocket connections for session management."""
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = websocket
        log.info(colored("=>=>=>=>=>=>=> WS", "blue"))
        log.info("WebSocket connected: %s", session_id)
        try:
            await websocket.send_json({"message": "Connected", "session_id": session_id})
            while True:
                await websocket.receive_json()
                # Handle incoming WebSocket messages (e.g., operations, pings)
                # if "operation" in data:
                #     await websocket.send_json({"message": f"Operation {data['operation']} received"})
        except WebSocketDisconnect:
            log.info(colored("<-------------", "blue"))
            log.info("Client %s disconnected", session_id)
            del self.sessions[session_id]
        except (ValueError, TypeError, RuntimeError) as e:  # nocoverage
            log.error("Error: %s", e)
            await websocket.send_json({"error": str(e)})
            del self.sessions[session_id]

    async def notify_clients(self, exclude_session_id: str | None = None) -> None:
        """Notify all connected clients of a version update in single-backend mode."""
        log.info("Notifying clients of version update")
        disconnected_sessions: list[str] = []

        for session_id, websocket in self.sessions.items():
            if session_id == exclude_session_id:
                continue
            try:
                await websocket.send_json({"type": "version_update", "new_version": self.version})
            except WebSocketDisconnect:  # nocoverage
                log.info(colored("<-------------", "blue"))
                log.info("Client %s disconnected", session_id)
                disconnected_sessions.append(session_id)

        # Remove disconnected sessions
        for session_id in disconnected_sessions:
            del self.sessions[session_id]  # nocoverage
