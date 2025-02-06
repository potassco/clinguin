"""Client module for serving the Angular frontend."""

import logging
import os
import shutil
import subprocess
import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from ..utils.logging import configure_logging

log = logging.getLogger(__name__)


class Client:
    """FastAPI client for serving the Angular frontend."""

    def __init__(  # pylint: disable=R0917
        self,
        port: int,
        host: str = "127.0.0.1",
        build: bool = False,
        custom_path: Optional[str] = None,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the client.

        Args:
            port (int): Port to serve the client.
            host (str): Host to bind to.
            build (bool): Whether to rebuild the frontend on startup.
        """
        self.port = port
        self.host = host
        self.angular_src_path = os.path.abspath("src/clinguin/client/angular")  # Angular project location
        self.frontend_dist_path = os.path.abspath("src/clinguin/client/dist/browser")  # Serve the `browser/` subfolder
        self.custom_path = custom_path or os.path.expanduser("~/.clinguin/client/")  # User-provided customizations

        configure_logging(stream=sys.stderr, level=log_level, use_color=True)  # Set up logging globally

        if custom_path and not build:  # nocoverage
            log.warning("Angular will be rebuilt to include custom files.")  # nocoverage
            build = True

        if build:
            self.build_frontend()  # nocoverage (Mocked in tests)

        self.app = FastAPI()

        # Ensure `dist/browser/` exists before serving
        if os.path.exists(self.frontend_dist_path):
            log.info("Serving Angular frontend from %s", self.frontend_dist_path)
            self.app.mount("/", StaticFiles(directory=self.frontend_dist_path, html=True), name="frontend")
        else:  # nocoverage
            log.error("No frontend found at %s", self.frontend_dist_path)
            log.error("Make sure client is built before running the server.")

    def build_frontend(self) -> None:
        """
        Build the Angular frontend, ensuring custom files are included before building.
        This generates files that can be used by other users without the need to install angular.
        """

        if not os.path.exists(self.angular_src_path):  # nocoverage
            raise RuntimeError(f"Angular source folder not found: {self.angular_src_path}")

        log.debug("Disabling Angular analytics to prevent interactive prompts...")
        subprocess.run(["npx", "ng", "analytics", "off"], cwd=self.angular_src_path, check=True)

        log.debug("Installing dependencies...")
        subprocess.run(["npm", "install", "--silent", "--no-fund"], cwd=self.angular_src_path, check=True)

        log.debug("Building Angular frontend...")
        subprocess.run(["npx", "ng", "build", "--output-path=dist"], cwd=self.angular_src_path, check=True)

        # Ensure `dist/browser/` exists inside Angular build output
        built_output = os.path.join(self.angular_src_path, "dist", "browser")
        if not os.path.exists(built_output):
            raise RuntimeError(f"Angular build failed! Expected output not found: {built_output}")  # nocoverage

        # Move `dist/browser/` to `clinguin/client/dist/`
        log.debug("Moving built frontend from %s to %s...", built_output, self.frontend_dist_path)
        shutil.rmtree(self.frontend_dist_path, ignore_errors=True)
        shutil.move(built_output, self.frontend_dist_path)

        log.warning("Angular frontend successfully built. Make sure browser cache is refreshed to see changes.")

    def include_custom_files(self, custom_path: str, angular_src_path: str) -> None:  # nocoverage
        """
        Copy user-provided custom CSS and components into the Angular project before building.

        Args:
            custom_path (str): Path to user-provided custom files (e.g., ~/.clinguin/client/)
            angular_src_path (str): Path to the Angular project (e.g., clinguin/client/angular/)
        """
        custom_path = os.path.expanduser(custom_path)  # Expand `~` in path

        if not os.path.exists(custom_path):
            log.info("No custom files found at %s. Skipping customization.", custom_path)
            return

        log.info("Copying user customizations from %s to %s/src/custom/", custom_path, angular_src_path)

        for item in os.listdir(custom_path):
            src_item = os.path.join(custom_path, item)
            dest_item = os.path.join(angular_src_path, "src/custom", item)

            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy(src_item, dest_item)

        log.info("Custom files successfully included.")

    def run(self) -> None:
        """Run the client."""

        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")
