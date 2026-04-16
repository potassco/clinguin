"""Client module for serving the Svelte frontend."""

import importlib
import logging
import os
import shutil
import subprocess
import sys

import uvicorn
from fastapi import FastAPI
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
        custom_path: str | None = None,
        log_level: int | None = None,
    ):
        """
        Initialize the client.

        Args:
            port (int): Port to serve the client.
            host (str): Host to bind the client to. Use 0.0.0.0 for external access.
            server_url (str): Full URL of the Clinguin server the frontend will connect to.
            build (bool): Whether to rebuild the frontend on startup.
            custom_path (str): Path to custom frontend files to include before building.
            log_level (int): Log level for the client.
        """
        self.port = port
        self.host = host
        self.server_url = server_url

        if os.path.exists(os.path.dirname(__file__)):
            # Development mode (running from source)
            package_path = os.path.dirname(__file__)
        else:
            # Installed mode (running from `site-packages/`)
            package_path = os.path.dirname(importlib.resources.files(clinguin))

        self.svelte_src_path = os.path.join(package_path, "svelte")
        self.frontend_dist_path = os.path.join(package_path, "svelte", "build")
        self.custom_path = custom_path or os.path.expanduser("~/.clinguin/client/")

        if log_level is not None:
            configure_logging(stream=sys.stderr, level=log_level, use_color=True)

        if custom_path and not build:  # nocoverage
            log.warning("Svelte will be rebuilt to include custom files.")  # nocoverage
            build = True

        if build:
            self.build_frontend()  # nocoverage (Mocked in tests)

        self.app = FastAPI()

        if os.path.exists(self.frontend_dist_path):
            log.info("Serving Svelte frontend from %s", self.frontend_dist_path)
            self.app.mount("/", StaticFiles(directory=self.frontend_dist_path, html=True), name="frontend")
        else:  # nocoverage
            log.error("No frontend found at %s", self.frontend_dist_path)
            log.error("Run with --build to build the frontend first.")

    def run(self) -> None:
        """Run the client."""
        log.info("🚀 Starting client on %s:%s", self.host, self.port)
        log.info("Frontend will call server at: %s", self.server_url)
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    def build_frontend(self) -> None:
        """
        Build the Svelte frontend.
        Injects VITE_SERVER_URL so the frontend knows which backend to connect to.
        """
        if not os.path.exists(self.svelte_src_path):  # nocoverage
            raise RuntimeError(f"Svelte source folder not found: {self.svelte_src_path}")

        log.debug("Installing dependencies...")
        subprocess.run(
            ["npm", "install", "--silent", "--no-fund"],
            cwd=self.svelte_src_path,
            check=True,
        )

        log.debug("Building Svelte frontend...")
        env = os.environ.copy()
        env["VITE_SERVER_URL"] = self.server_url
        subprocess.run(
            ["npm", "run", "build"],
            cwd=self.svelte_src_path,
            env=env,
            check=True,
        )

        if not os.path.exists(self.frontend_dist_path):  # nocoverage
            raise RuntimeError(f"Svelte build failed. Expected output not found: {self.frontend_dist_path}")

        log.warning("Svelte frontend built. Refresh your browser to see changes.")

    def include_custom_files(self, custom_path: str, svelte_src_path: str) -> None:  # nocoverage
        """
        Copy user-provided custom CSS and components into the Svelte project before building.

        Args:
            custom_path (str): Path to user-provided custom files (e.g., ~/.clinguin/client/)
            svelte_src_path (str): Path to the Svelte project (e.g., clinguin/client/svelte/)
        """
        custom_path = os.path.expanduser(custom_path)

        if not os.path.exists(custom_path):
            log.info("No custom files found at %s. Skipping customization.", custom_path)
            return

        log.info("Copying user customizations from %s to %s/src/custom/", custom_path, svelte_src_path)

        for item in os.listdir(custom_path):
            src_item = os.path.join(custom_path, item)
            dest_item = os.path.join(svelte_src_path, "src/custom", item)

            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy(src_item, dest_item)

        log.info("Custom files successfully included.")
