"""Test the Client class"""

# pylint: disable=redefined-outer-name


from types import SimpleNamespace
from unittest.mock import patch

import clinguin.cli as cli
from fastapi.testclient import TestClient
import logging
import pytest
from clinguin.client.client import Client


@pytest.fixture
def client():
    """Provides a Client instance with a test configuration."""
    return Client(port=8001, build=False, log_level=logging.INFO)  # Don't trigger build immediately


def test_backend_urls():
    """Ensure the client derives backend HTTP and WebSocket URLs correctly."""
    client = Client(port=8001, server_url="https://example.com/backend", build=False)

    assert client.backend_http_url("/info") == "https://example.com/backend/info"
    assert client.backend_ws_url("/ws") == "wss://example.com/backend/ws"


def test_static_assets_are_proxied(monkeypatch, client):
    """Ensure backend static assets stay reachable through the client origin."""
    captured = {}

    class FakeResponse:
        content = b"body { color: red; }"
        status_code = 200
        headers = {"content-type": "text/css; charset=utf-8"}

    class FakeAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def get(self, url, headers=None):
            captured["url"] = url
            captured["headers"] = headers
            return FakeResponse()

    monkeypatch.setattr("clinguin.client.client.httpx.AsyncClient", lambda timeout: FakeAsyncClient())

    response = TestClient(client.app).get("/static/generated.css")

    assert response.status_code == 200
    assert response.text == "body { color: red; }"
    assert captured["url"] == "http://127.0.0.1:8000/static/generated.css"


def test_cli_passes_server_url(monkeypatch):
    """Ensure the CLI forwards --server-url to Client."""
    captured = {}

    class FakeClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def run(self):
            captured["ran"] = True

    monkeypatch.setattr(cli, "Client", FakeClient)
    monkeypatch.setattr(
        cli,
        "get_parser",
        lambda: SimpleNamespace(
            parse_args=lambda: SimpleNamespace(
                command="client",
                port=8001,
                host="0.0.0.0",
                server_url="http://10.0.0.2:8000",
                build=False,
                theme=None,
                assets=None,
                log=logging.INFO,
            )
        ),
    )

    cli.main()

    assert captured["server_url"] == "http://10.0.0.2:8000"
    assert captured["ran"] is True


def test_share_starts_server_and_client(monkeypatch, capsys):
    """Ensure the share command wires a local server and public client together."""
    events = {}

    class FakeBackendArgs:
        @staticmethod
        def from_args(args):
            events["backend_args_source"] = args.command
            return "backend-args"

    class FakeBackendClass:
        args_class = FakeBackendArgs

    class FakeServer:
        def __init__(self, **kwargs):
            events["server_init"] = kwargs

        def run(self):
            events["server_ran"] = True

    class FakeClient:
        def __init__(self, **kwargs):
            events["client_init"] = kwargs

        def run(self):
            events["client_ran"] = True

    class FakeThread:
        def __init__(self, *, target, name, daemon):
            events["thread"] = {"name": name, "daemon": daemon}
            self._target = target

        def start(self):
            events["thread_started"] = True
            self._target()

    monkeypatch.setattr(cli, "Server", FakeServer)
    monkeypatch.setattr(cli, "Client", FakeClient)
    monkeypatch.setattr(cli.threading, "Thread", FakeThread)
    monkeypatch.setattr(
        cli,
        "get_parser",
        lambda: SimpleNamespace(
            parse_args=lambda: SimpleNamespace(
                command="share",
                backend_class=FakeBackendClass,
                multi=True,
                server_port=9000,
                server_host="127.0.0.1",
                client_port=9001,
                client_host="0.0.0.0",
                build=False,
                theme=None,
                assets=None,
                log=logging.INFO,
            )
        ),
    )

    cli.main()

    assert events["backend_args_source"] == "share"
    assert events["server_init"]["port"] == 9000
    assert events["server_init"]["host"] == "127.0.0.1"
    assert events["server_init"]["multi"] is True
    assert events["client_init"]["port"] == 9001
    assert events["client_init"]["host"] == "0.0.0.0"
    assert events["client_init"]["server_url"] == "http://127.0.0.1:9000"
    assert events["thread"] == {"name": "clinguin-server", "daemon": True}
    assert events["thread_started"] is True
    assert events["server_ran"] is True
    assert events["client_ran"] is True

    stdout = capsys.readouterr().out
    assert "Share URL: http://localhost:9001" in stdout
    assert "ngrok http 9001" in stdout


@patch("subprocess.run")  # Mock subprocess calls
@patch("shutil.copytree")  # Mock copying directories
@patch("shutil.copy")  # Mock copying files
@patch("shutil.rmtree")  # Mock deleting files
def test_build_frontend(
    mock_rmtree, mock_copy, mock_copytree, mock_subprocess, client
):  # pylint: disable=unused-argument
    """Test that the frontend builds correctly and custom files are included."""

    # Run the frontend build process
    client.build_frontend()

    # Ensure Svelte build commands were called
    mock_subprocess.assert_any_call(
        ["npm", "install", "--silent", "--no-fund"],
        cwd=client.svelte_src_path,
        check=True,
    )
    build_call = mock_subprocess.call_args_list[1]
    assert build_call.args == (["npm", "run", "build"],)
    assert build_call.kwargs["cwd"] == client.svelte_src_path
    assert build_call.kwargs["env"]["VITE_SERVER_URL"] == ""


@patch("uvicorn.run")  # Mock Uvicorn so it doesn't actually start the server
def test_run(mock_uvicorn, client):
    """Test that `Client.run()` starts Uvicorn with the correct settings."""

    # Run the client
    client.run()

    # Ensure Uvicorn is called with the correct parameters
    mock_uvicorn.assert_called_once_with(client.app, host="127.0.0.1", port=8001, log_level="info")
