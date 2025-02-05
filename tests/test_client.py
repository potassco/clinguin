import pytest
import os
import shutil
from unittest.mock import patch
from clinguin.client import Client

ANGULAR_SRC_PATH = os.path.abspath("src/clinguin/client/angular")  # Ensure absolute path
FRONTEND_DIST_PATH = os.path.abspath("src/clinguin/client/dist")
ANGULAR_DIST_PATH = os.path.join(ANGULAR_SRC_PATH, "dist/browser")  # ✅ Expected output path


@pytest.fixture
def client():
    """Provides a Client instance with a test configuration."""
    return Client(port=8001, build=False)  # Don't trigger build immediately


@patch("subprocess.run")  # ✅ Mock subprocess calls
@patch("shutil.copytree")  # ✅ Mock copying directories
@patch("shutil.copy")  # ✅ Mock copying files
@patch("shutil.rmtree")  # ✅ Mock deleting files
@patch(
    "os.path.exists",
    side_effect=lambda path: path.startswith(os.path.abspath(ANGULAR_SRC_PATH))
    or path == ANGULAR_DIST_PATH
    or path == FRONTEND_DIST_PATH,
)  # ✅ Ensure `dist/browser/` exists
def test_build_frontend(mock_exists, mock_rmtree, mock_copy, mock_copytree, mock_subprocess, client):
    """Test that the frontend builds correctly and custom files are included."""

    # ✅ Simulate Angular build output by manually creating `dist/browser/`
    os.makedirs(ANGULAR_DIST_PATH, exist_ok=True)

    # ✅ Run the frontend build process
    client.build_frontend()

    # ✅ Ensure Angular build commands were called
    mock_subprocess.assert_any_call(["npm", "install", "--silent", "--no-fund"], cwd=ANGULAR_SRC_PATH, check=True)
    mock_subprocess.assert_any_call(["npx", "ng", "build", "--output-path=dist"], cwd=ANGULAR_SRC_PATH, check=True)

    # ✅ Ensure old build was removed
    mock_rmtree.assert_called_with(os.path.join(FRONTEND_DIST_PATH, "browser"), ignore_errors=True)

    # Cleanup
    shutil.rmtree(ANGULAR_DIST_PATH, ignore_errors=True)  # ✅ Remove simulated build output


@patch("uvicorn.run")  # ✅ Mock Uvicorn so it doesn't actually start the server
@patch(
    "os.path.exists", side_effect=lambda path: path in [FRONTEND_DIST_PATH, os.path.join(FRONTEND_DIST_PATH, "browser")]
)  # ✅ Mock frontend existence
def test_run(mock_exists, mock_uvicorn, client):
    """Test that `Client.run()` starts Uvicorn with the correct settings."""

    # ✅ Run the client
    client.run()

    # ✅ Ensure Uvicorn is called with the correct parameters
    mock_uvicorn.assert_called_once_with(client.app, host="127.0.0.1", port=8001, log_level="info")
