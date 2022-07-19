import json
import httpx

from clinguin.client.api.call_dto import CallDto

class Api:
    
    def __init__(self, instance, base_url = "http://127.0.0.1:8000/"):
        self.base_url = base_url
        self._instance = instance

    def get(self, endpoint):
        self._instance.logger.info("Sending GET request to: " + str(self.base_url + endpoint))
        try:
            r = httpx.get(self.base_url + endpoint)
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")

    def post(self, endpoint, body:CallDto):
        self._instance.logger.info("Sending POST request to: " + str(self.base_url + endpoint) + ", with the content: " + str(body.function))
        try:
            r = httpx.post(self.base_url + endpoint, data = body.toJSON())
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")


