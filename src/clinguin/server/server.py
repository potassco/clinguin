from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
import uuid
from ..utils.logging import get_logger


# Define a specific request model for operations
class OperationRequest(BaseModel):
    operation: str
    client_version: int


log = get_logger("main")


class Server:
    def __init__(self, port: int, host: str, mode: str):
        self.port = port
        self.host = host
        self.mode = mode  # "multi" or "single"
        self.app = FastAPI()
        self.sessions = {}
        self.version = 1

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

    async def execute_operation(self, request: OperationRequest):
        """Execute an operation provided by the client."""
        if request.client_version < self.version:
            raise HTTPException(
                status_code=409,
                detail="Outdated version. Please sync with the latest version.",
            )

        # Example operation handling
        operation_result = {"message": f"Executed operation: {request.operation}"}

        # Increment version and notify all clients in single-backend mode
        self.version += 1
        await self.notify_clients()

        return {"result": operation_result, "version": self.version}

    async def websocket_endpoint(self, websocket: WebSocket):
        """Handle WebSocket connections for session management."""
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = websocket
        try:
            await websocket.send_json(
                {"message": "Connected", "session_id": session_id}
            )
            while True:
                data = await websocket.receive_json()
                # Handle incoming WebSocket messages (e.g., operations, pings)
                if "operation" in data:
                    await websocket.send_json(
                        {"message": f"Operation {data['operation']} received"}
                    )
        except WebSocketDisconnect:
            print(f"Client {session_id} disconnected")
            del self.sessions[session_id]
        except Exception as e:
            print(f"Error: {e}")
            await websocket.send_json({"error": str(e)})
            del self.sessions[session_id]

    async def notify_clients(self):
        """Notify all connected clients of a version update in single-backend mode."""
        log.info("Notifying clients of version update")
        disconnected_sessions = []

        for session_id, websocket in self.sessions.items():
            try:
                await websocket.send_json(
                    {"type": "version_update", "new_version": self.version}
                )
            except WebSocketDisconnect:
                disconnected_sessions.append(session_id)

        # Remove disconnected sessions
        for session_id in disconnected_sessions:
            del self.sessions[session_id]

    def run(self):
        import uvicorn

        uvicorn.run(self.app, host =self.host, port=self.port, log_level="warning")


# Example usage:
# server = Server(port=8000, url="/ws", mode="single")
# server.run()
