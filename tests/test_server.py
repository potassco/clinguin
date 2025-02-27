"""Tests for the server module."""

# pylint: disable=redefined-outer-name

import atexit
import asyncio
import json
import multiprocessing
import os
import signal
import sys
import time
from types import SimpleNamespace
from typing import Generator
from pathlib import Path

import logging

import httpx
import pytest
import websockets
from coverage import Coverage

from clinguin.server import Server
from clinguin.server.backends import ClingoBackend

WEBSOCKET_URL = "ws://127.0.0.1:8000/ws"
HTTP_URL = "http://127.0.0.1:8000"

TEST_DATA_DIR = Path(__file__).parent / "data"


backend_args = SimpleNamespace(
    domain_files=[str(TEST_DATA_DIR / "encoding.lp"), str(TEST_DATA_DIR / "instance.lp")],
    ui_files=[str(TEST_DATA_DIR / "ui.lp")],
)


def start_server():  # nocoverage
    """Start the server process with coverage tracking."""
    cov = Coverage(data_file=f".coverage.{os.getpid()}")
    cov.start()

    def stop_coverage():
        """Ensure coverage data is saved before process exits."""
        cov.stop()
        cov.save()

    # Handle termination signals (SIGTERM, SIGINT)
    def handle_signal(signum: int, _: None) -> None:
        print(f"Received signal: {signum}")
        stop_coverage()
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    # Ensure coverage saves before process exits
    atexit.register(stop_coverage)
    try:
        server = Server(
            backend_class=ClingoBackend,
            backend_args=ClingoBackend.args_class.from_args(backend_args),
            port=8000,
            host="127.0.0.1",
            log_level=logging.INFO,
        )
        server.run()
    finally:
        stop_coverage()  # Ensure we always save before exit
        sys.exit(0)  # Ensure a clean exit


@pytest.fixture(scope="module", autouse=True)
def server():
    """Starts the server in a separate process before tests."""
    process = multiprocessing.Process(target=start_server, daemon=True)
    process.start()
    time.sleep(3)  # Allow time for the server to start
    yield process
    process.terminate()
    process.join()


@pytest.fixture
def client() -> Generator[httpx.Client, None, None]:
    """Provides an HTTP client with a timeout."""
    with httpx.Client(base_url=HTTP_URL, timeout=5) as client:
        yield client


@pytest.mark.asyncio
async def test_info_endpoint():  # pylint: disable=unused-argument
    """Test the /info endpoint."""
    async with websockets.connect(WEBSOCKET_URL) as ws:
        # Receive initial connection messages
        msg = await asyncio.wait_for(ws.recv(), timeout=5)

        data = json.loads(msg)
        headers = {"session-id": data["session_id"]}

        async with httpx.AsyncClient(timeout=5) as client:

            response = await asyncio.wait_for(
                client.get(f"{HTTP_URL}/info", headers=headers),
                timeout=5,
            )
            data = response.json()

            assert response.status_code == 200
            assert data["status"] == "running"
            assert data["version"] == 1
            assert data["active_sessions"] == 1
            assert "ui" in data
            assert data["ui"]["id"] == "root"
            assert data["ui"]["children"][0]["id"] == "w"
            assert "ds" in data
            assert "_ds_context" in data["ds"]
            assert "_ds_constants" in data["ds"]
            assert "_ds_browsing" in data["ds"]
            assert "_ds_cautious_optimal" in data["ds"]
            assert "_ds_brave_optimal" in data["ds"]
            assert "_ds_cautious" in data["ds"]
            assert "_ds_brave" in data["ds"]
            assert "_ds_model" in data["ds"]
            assert "_ds_opt" in data["ds"]
            assert "_ds_unsat" in data["ds"]
            assert "_ds_assume" in data["ds"]


# def test_info_endpoint(server, client):  # pylint: disable=unused-argument
#     """Test the /info endpoint."""
#     response = client.get("/info")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "running"
#     assert data["version"] == 1
#     assert data["active_sessions"] == 0


@pytest.mark.asyncio
async def test_websocket_operation():
    """Test WebSocket connection with debug logging."""
    async with websockets.connect(WEBSOCKET_URL) as ws:
        msg = await asyncio.wait_for(ws.recv(), timeout=5)
        data = json.loads(msg)
        assert "session_id" in data
        headers = {"session-id": data["session_id"]}

        # Send a test operation
        async with httpx.AsyncClient(timeout=5) as client:

            response = await asyncio.wait_for(
                client.post(
                    f"{HTTP_URL}/operation",
                    json={"operation": "test_operation", "client_version": 1},
                    headers=headers,
                ),
                timeout=5,
            )
            data = response.json()

            assert response.status_code == 200
            assert "result" in data
            assert "version" in data
            assert data["version"] == 2


@pytest.mark.asyncio
async def test_websocket_version_notifications():
    """Test WebSocket version update notification."""
    async with websockets.connect(WEBSOCKET_URL) as ws1, websockets.connect(WEBSOCKET_URL) as ws2:
        # Receive initial connection messages
        msg1 = await asyncio.wait_for(ws1.recv(), timeout=5)
        msg2 = await asyncio.wait_for(ws2.recv(), timeout=5)

        data1 = json.loads(msg1)
        data2 = json.loads(msg2)

        assert "session_id" in data1
        assert "session_id" in data2

        headers1 = {"session-id": data1["session_id"]}

        # Perform an operation using the HTTP client
        async with httpx.AsyncClient(timeout=5) as client:
            response = await asyncio.wait_for(
                client.post(
                    f"{HTTP_URL}/operation", json={"operation": "test_operation", "client_version": 2}, headers=headers1
                ),
                timeout=5,
            )
            assert response.status_code == 200

        # The second WebSocket should receive a version update notification
        update2 = await asyncio.wait_for(ws2.recv(), timeout=5)
        update_data2 = json.loads(update2)
        assert update_data2["type"] == "version_update"
        assert update_data2["new_version"] == 3

        # Make a request without session id and get 400
        async with httpx.AsyncClient(timeout=5) as client:
            response = await asyncio.wait_for(
                client.post(f"{HTTP_URL}/operation", json={"operation": "test_operation", "client_version": 3}),
                timeout=5,
            )
            assert response.status_code == 400

            # Make an outdated request and get 409
            response = await asyncio.wait_for(
                client.post(
                    f"{HTTP_URL}/operation", json={"operation": "test_operation", "client_version": 2}, headers=headers1
                ),
                timeout=5,
            )
            assert response.status_code == 409


@pytest.mark.asyncio
async def test_websocket_disconnect():
    """Test that the WebSocket disconnects properly and is handled by the server."""
    async with websockets.connect(WEBSOCKET_URL) as ws:
        msg = await asyncio.wait_for(ws.recv(), timeout=5)  # Receive initial connection message
        data = json.loads(msg)
        assert "session_id" in data  # Ensure the session ID is received

    # Allow time for server to process the disconnect
    await asyncio.sleep(1)  # Prevents race conditions

    # Now, reconnect and check if the server has removed the old session
    async with websockets.connect(WEBSOCKET_URL) as ws2:
        msg2 = await asyncio.wait_for(ws2.recv(), timeout=5)  # Get session info
        data2 = json.loads(msg2)
        assert "session_id" in data2  # Ensure new session is assigned

        # The new session should be different if the old one was removed properly
        assert data["session_id"] != data2["session_id"]
