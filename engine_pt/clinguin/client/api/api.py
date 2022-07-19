import json
import httpx

from client.api.call_dto import CallDto

class Api:
    
    def __init__(self, base_url = "http://127.0.0.1:8000/"):
        self.base_url = base_url

    def get(self, endpoint):
        try:
            r = httpx.get(self.base_url + endpoint)
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")

    def post(self, endpoint, body:CallDto):
        try:
            r = httpx.post(self.base_url + endpoint, data = body.toJSON())
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")


