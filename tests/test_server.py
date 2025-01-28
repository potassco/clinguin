import unittest
import asyncio
import websockets
import json
import multiprocessing
import time
import httpx
from clinguin.server.server import Server


def start_server():  # nocoverage
    """Function to start the server process."""
    server = Server(port=8000, host="127.0.0.1", mode="single")
    server.run()

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a subprocess
        cls.server_process = multiprocessing.Process(target=start_server, daemon=True)
        cls.server_process.start()

        # Wait for the server to initialize
        time.sleep(1)  # Allow time for the server to start

        # Initialize an HTTP client
        cls.http_client = httpx.Client(base_url="http://127.0.0.1:8000")

    @classmethod
    def tearDownClass(cls):
        # Terminate the server subprocess
        cls.server_process.terminate()
        cls.server_process.join()
        cls.http_client.close()

    def test_info_endpoint(self):
        """Test the /info endpoint."""
        response = self.http_client.get("/info")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "running")
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["active_sessions"], 0)

    def test_operation_endpoint(self):
        """Test the /operation endpoint."""
        request_data = {"operation": "test_operation", "client_version": 1}
        response = self.http_client.post("/operation", json=request_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("result", data)
        self.assertIn("version", data)
        self.assertEqual(data["version"], 2)

    async def websocket_test_logic(self):
        """Test WebSocket interactions."""
        uri = "ws://127.0.0.1:8000/ws"
        async with websockets.connect(uri) as ws1, websockets.connect(uri) as ws2:
            # Receive initial connection messages
            msg1 = await ws1.recv()
            msg2 = await ws2.recv()

            data1 = json.loads(msg1)
            data2 = json.loads(msg2)

            self.assertIn("session_id", data1)
            self.assertIn("session_id", data2)

            # Perform an operation using the HTTP client
            request_data = {"operation": "test_operation", "client_version": 2}
            response = self.http_client.post("/operation", json=request_data)
            self.assertEqual(response.status_code, 200)

            # Both clients should receive a version update
            update1 = await ws1.recv()
            update2 = await ws2.recv()

            update_data1 = json.loads(update1)
            update_data2 = json.loads(update2)

            self.assertEqual(update_data1["type"], "version_update")
            self.assertEqual(update_data1["new_version"], 3)
            self.assertEqual(update_data2["type"], "version_update")
            self.assertEqual(update_data2["new_version"], 3)

    def test_websocket_notifications(self):
        """Run the asynchronous WebSocket test logic."""
        asyncio.run(self.websocket_test_logic())


