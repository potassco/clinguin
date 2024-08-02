"""
Module that contains the API-Class
"""

import json
import logging
import traceback
from urllib.request import Request, URLError, urlopen

from clinguin.utils import Logger

from .frontend_operation_dto import FrontendOperationDto


class Api:
    """
    The API class is responsible for handling API calls, i.e. sending requests and receiving the responses.
    For this two methods exists - GET and POST.
    This Api sends by default requests to the url:http://127.0.0.1:8000/
    """

    def __init__(self, base_url="http://127.0.0.1:8000/"):
        self._logger = logging.getLogger(Logger.client_logger_name)

        self.base_url = base_url

    def get(self, endpoint):
        """
        Used for get requests.
        """
        try:
            self._logger.info("<-- GET to %s%s", str(self.base_url), str(endpoint))
            url = self.base_url + endpoint
            with urlopen(url) as response:
                body = response.read()
                status = response.getcode()
            response_json = json.loads(body)
            self._logger.debug(response_json)
            return (status, response_json)
        except URLError:
            return (-1, "")
        except Exception:
            self._logger.error("Some other connection-error occured.")
            self._logger.error("<<<BEGIN-STACKTRACE>>>")
            traceback.print_exc()
            self._logger.error("<<<END-STACKTRACE>>>")
            return (-2, "")

    def post(self, endpoint, body: FrontendOperationDto):
        """
        Used for post requests.
        """
        try:
            self._logger.info(
                "<-- POST to %s%s   %s",
                str(self.base_url),
                str(endpoint),
                str(body.function),
            )

            data = body.to_JSON()
            data = data.encode("utf-8")
            req = Request(self.base_url + endpoint, data=data)
            req.add_header("Content-Type", "application/json")
            with urlopen(req) as response:
                body = response.read()
                status = response.getcode()
            response_json = json.loads(body)

            self._logger.debug(response_json)
            return (status, response_json)
        except URLError as e:
            self._logger.warning("Https-connect-error occured.")
            print(e)
            return (-1, "")
        except Exception:
            self._logger.error("Some other connection-error occured.")
            self._logger.error("<<<BEGIN-STACKTRACE>>>")
            traceback.print_exc()
            self._logger.error("<<<END-STACKTRACE>>>")
            return (-2, "")
