import json
import httpx
import logging

from clinguin.client.api.call_dto import CallDto


class Api:

    def __init__(self, args, base_url="http://127.0.0.1:8000/"):

        self._logger = logging.getLogger(args.log_args['name'])

        self.base_url = base_url

    def get(self, endpoint):
        try:
            self._logger.debug("Sending GET to " +
                               str(self.base_url) + str(endpoint))
            r = httpx.get(self.base_url + endpoint, timeout=10000)
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")

    def post(self, endpoint, body: CallDto):
        try:
            self._logger.debug("Sending POST to " +
                               str(self.base_url) +
                               str(endpoint) +
                               " with content:" +
                               str(body.function))
            
            data = body.toJSON()
            r = httpx.post(self.base_url + endpoint, data=data, timeout=10000)
            #TODO HANDLE other errors here... 500 Internal Server Error
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")
