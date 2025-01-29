from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from pydantic import BaseModel
import uuid
import logging
import sys
import time

from ..utils.logging import configure_logging, colored

log = logging.getLogger(__name__)


class OperationRequest(BaseModel):
    operation: str
    client_version: int


class Server:
    def __init__(self, port: int, host: str, mode: str, log_level: int = logging.INFO):
        self.port = port
        self.host = host
        self.mode = mode  # "multi" or "single"
        self.app = FastAPI()
        self.sessions = {}
        self.version = 1

        configure_logging(stream=sys.stderr, level=log_level, use_color=True)  # Set up logging globally

        # Add middleware for request logging
        self.app.middleware("http")(self.log_requests)

        self.app.get("/info")(self.get_info)
        self.app.post("/operation")(self.execute_operation)
        self.app.websocket("/ws")(self.websocket_endpoint)

    async def get_info(self):
        """Retrieve server status or session information."""
        return {
            "status": "running",
            "version": self.version,
            "active_sessions": len(self.sessions),
        }

    async def execute_operation(self, request_body: OperationRequest, fastapi_request: Request):
        """Execute an operation provided by the client."""
        if request_body.client_version < self.version:
            log.warning("Client version is outdated.")
            raise HTTPException(
                status_code=409,
                detail="Outdated version. Please sync with the latest version.",
            )

        # Get the session ID from the request headers
        initiator_session_id = fastapi_request.headers.get("session-id")
        if not initiator_session_id:
            raise HTTPException(
                status_code=400,
                detail="Missing session ID in headers.",
            )

        # Example operation handling
        operation_result = {"message": f"Executed operation: {request_body.operation}"}

        # Increment version and notify all clients in single-backend mode
        self.version += 1
        await self.notify_clients(exclude_session_id=initiator_session_id)

        return {"result": operation_result, "version": self.version}

    async def websocket_endpoint(self, websocket: WebSocket):
        """Handle WebSocket connections for session management."""
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = websocket
        log.info(colored("=>=>=>=>=>=>=> WS", "blue"))
        log.info(f"WebSocket connected: {session_id}")
        try:
            await websocket.send_json({"message": "Connected", "session_id": session_id})
            while True:
                await websocket.receive_json()
                # Handle incoming WebSocket messages (e.g., operations, pings)
                # if "operation" in data:
                #     await websocket.send_json({"message": f"Operation {data['operation']} received"})
        except WebSocketDisconnect:
            log.info(colored("<-------------", "blue"))
            log.info(f"Client {session_id} disconnected")
            del self.sessions[session_id]
        except Exception as e:  # nocoverage
            log.error(f"Error: {e}")
            await websocket.send_json({"error": str(e)})
            del self.sessions[session_id]

    async def notify_clients(self, exclude_session_id=None):
        """Notify all connected clients of a version update in single-backend mode."""
        log.info("Notifying clients of version update")
        disconnected_sessions = []

        for session_id, websocket in self.sessions.items():
            if session_id == exclude_session_id:
                continue
            try:
                await websocket.send_json({"type": "version_update", "new_version": self.version})
            except WebSocketDisconnect:  # nocoverage
                log.info(colored("<-------------", "blue"))
                log.info(f"Client {session_id} disconnected")
                disconnected_sessions.append(session_id)

        # Remove disconnected sessions
        for session_id in disconnected_sessions:
            del self.sessions[session_id]  # nocoverage

    def run(self):
        import uvicorn

        uvicorn.run(self.app, host=self.host, port=self.port, log_level="warning")

    async def log_requests(self, request: Request, call_next):
        """Middleware to log details of every request."""
        log.info(colored(f"=>=>=>=>=>=>=> {request.method}", "green"))
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        log.debug(f"Completed in {duration:.2f}s with status {response.status_code}")
        log.info(colored(f"<------------- {response.status_code}", "green"))
        return response
