"""Client module for serving the Svelte frontend."""

import importlib
import logging
import os
import shutil
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

import httpx
import uvicorn
import websockets
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import clinguin

from ..utils.logging import configure_logging

log = logging.getLogger(__name__)


class Client:
    """FastAPI client for serving the Svelte frontend."""

    def __init__(  # pylint: disable=R0917
        self,
        port: int,
        host: str = "127.0.0.1",
        server_url: str = "http://127.0.0.1:8000",
        build: bool = False,
        theme: str | None = None,
        assets: str | None = None,
        log_level: int | None = None,
    ):
        """
        Initialize the client.

        Args:
            port (int): Port to serve the client.
            host (str): Host to bind the client to. Use 0.0.0.0 for external access.
            server_url (str): Full URL of the Clinguin server the frontend will connect to.
            build (bool): Whether to rebuild the frontend on startup.
            theme (str | None): Path to a custom CSS file.
            assets (str | None): Path to a directory of static assets.
            log_level (int): Log level for the client.
        """
        self.port = port
        self.host = host
        self.server_url = server_url.rstrip("/")

        if os.path.exists(os.path.dirname(__file__)):
            # Development mode (running from source)
            package_path = os.path.dirname(__file__)
        else:
            # Installed mode (running from `site-packages/`)
            package_path = os.path.dirname(importlib.resources.files(clinguin))

        self.svelte_src_path = os.path.join(package_path, "svelte")
        self.frontend_dist_path = os.path.join(package_path, "svelte", "build")
        self.theme = theme or None
        self.assets = assets or None

        if log_level is not None:
            configure_logging(stream=sys.stderr, level=log_level, use_color=True)

        if (theme or assets) and not build:
            log.warning("Svelte will be rebuilt to include custom files.")  # nocoverage
            build = True

        if build:
            self.build_frontend()  # nocoverage (Mocked in tests)

        self.app = FastAPI()
        self.app.get("/info")(self.proxy_info)
        self.app.post("/operation")(self.proxy_operation)
        self.app.websocket("/ws")(self.proxy_websocket)

        if os.path.exists(self.frontend_dist_path):
            log.info("Serving Svelte frontend from %s", self.frontend_dist_path)
            self.app.mount("/", StaticFiles(directory=self.frontend_dist_path, html=True), name="frontend")
        else:  # nocoverage
            raise RuntimeError(
                f"No frontend found at {self.frontend_dist_path}. Run with --build to build the frontend first."
            )

    def run(self) -> None:
        """Run the client."""
        log.info("🚀 Starting client on %s:%s", self.host, self.port)
        log.info("Proxying frontend requests to server at: %s", self.server_url)
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    def backend_http_url(self, path: str) -> str:
        """Build a backend HTTP URL for the given path."""
        return f"{self.server_url}{path}"

    def backend_ws_url(self, path: str) -> str:
        """Build a backend WebSocket URL for the given path."""
        scheme, netloc, url_path, query, fragment = urlsplit(self.backend_http_url(path))
        ws_scheme = "wss" if scheme == "https" else "ws"
        return urlunsplit((ws_scheme, netloc, url_path, query, fragment))

    @staticmethod
    def _forward_headers(request: Request) -> dict[str, str]:
        """Forward only the headers the backend needs."""
        headers: dict[str, str] = {}
        for header_name in ("session-id", "content-type"):
            header_value = request.headers.get(header_name)
            if header_value:
                headers[header_name] = header_value
        return headers

    @staticmethod
    def _proxy_error_response(exc: Exception) -> JSONResponse:
        """Return a consistent upstream connection error response."""
        return JSONResponse(
            status_code=502,
            content={"detail": f"Could not reach backend server: {exc}"},
        )

    async def proxy_info(self, request: Request) -> Response:
        """Proxy GET /info to the backend server."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                upstream = await client.get(
                    self.backend_http_url("/info"),
                    headers=self._forward_headers(request),
                )
        except httpx.HTTPError as exc:
            return self._proxy_error_response(exc)

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type"),
        )

    async def proxy_operation(self, request: Request) -> Response:
        """Proxy POST /operation to the backend server."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                upstream = await client.post(
                    self.backend_http_url("/operation"),
                    content=await request.body(),
                    headers=self._forward_headers(request),
                )
        except httpx.HTTPError as exc:
            return self._proxy_error_response(exc)

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type"),
        )

    async def proxy_websocket(self, websocket: WebSocket) -> None:
        """Proxy /ws to the backend server so the frontend can stay same-origin."""
        await websocket.accept()
        try:
            async with websockets.connect(self.backend_ws_url("/ws")) as upstream:
                while True:
                    message = await upstream.recv()
                    if isinstance(message, bytes):
                        await websocket.send_bytes(message)
                    else:
                        await websocket.send_text(message)
        except WebSocketDisconnect:
            return
        except (OSError, websockets.WebSocketException) as exc:  # pragma: no cover - depends on network failures
            await websocket.send_json({"error": f"Could not connect to backend websocket: {exc}"})
            await websocket.close(code=1011)

    def build_frontend(self) -> None:
        """
        Build the Svelte frontend.
        Injects VITE_SERVER_URL and VITE_CUSTOM_THEME so the frontend
        knows which backend to connect to and which CSS file to load.
        """
        if not os.path.exists(self.svelte_src_path):  # nocoverage
            raise RuntimeError(f"Svelte source folder not found: {self.svelte_src_path}")

        log.debug("Installing dependencies...")
        subprocess.run(
            ["npm", "install", "--silent", "--no-fund"],
            cwd=self.svelte_src_path,
            check=True,
        )

        theme_filename = ""
        if self.theme:
            if not os.path.isfile(self.theme):  # nocoverage
                raise RuntimeError(f"Theme file not found: {self.theme}")
            theme_filename = os.path.basename(self.theme)
            dest = os.path.join(self.svelte_src_path, "static", theme_filename)
            shutil.copy(self.theme, dest)
            log.debug("Copied theme file %s → static/%s", self.theme, theme_filename)

        if self.assets:  # nocoverage
            if not os.path.isdir(self.assets):
                raise RuntimeError(f"Assets directory not found: {self.assets}")
            dest = os.path.join(self.svelte_src_path, "static", "assets")
            shutil.copytree(self.assets, dest, dirs_exist_ok=True)
            log.debug("Copied assets from %s → static/assets/", self.assets)

        log.debug("Building Svelte frontend...")
        env = os.environ.copy()
        env["VITE_SERVER_URL"] = ""
        env["VITE_CUSTOM_THEME"] = theme_filename
        subprocess.run(
            ["npm", "run", "build"],
            cwd=self.svelte_src_path,
            env=env,
            check=True,
        )

        if not os.path.exists(self.frontend_dist_path):  # nocoverage
            raise RuntimeError(f"Svelte build failed. Expected output not found: {self.frontend_dist_path}")

        log.info("Svelte frontend built. Refresh your browser to see changes.")

        if theme_filename:
            leftover = os.path.join(self.svelte_src_path, "static", theme_filename)
            if os.path.exists(leftover):
                os.remove(leftover)
                log.debug("Cleaned up static/%s after build", theme_filename)

        if self.assets:
            leftover_dir = os.path.join(self.svelte_src_path, "static", "assets")
            if os.path.exists(leftover_dir):
                shutil.rmtree(leftover_dir)
                log.debug("Cleaned up static/assets/ after build")
