"""
Module that contains the API-Class
"""
import logging
import traceback

import httpx

from clinguin.utils import Logger

from .frontend_policy_dto import FrontendPolicyDto


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
            r = httpx.get(self.base_url + endpoint, timeout=10000)
            self._logger.debug(r.json())
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")
        except Exception:
            self._logger.error("Some other connection-error occured.")
            self._logger.error("<<<BEGIN-STACKTRACE>>>")
            traceback.print_exc()
            self._logger.error("<<<END-STACKTRACE>>>")
            return (-2, "")

    def post(self, endpoint, body: FrontendPolicyDto):
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
            r = httpx.post(self.base_url + endpoint, data=data, timeout=10000)
            self._logger.debug(r.json())
            return (r.status_code, r.json())
        except httpx.ConnectError:
            self._logger.warning("Https-connect-error occured.")
            return (-1, "")
        except Exception:
            self._logger.error("Some other connection-error occured.")
            self._logger.error("<<<BEGIN-STACKTRACE>>>")
            traceback.print_exc()
            self._logger.error("<<<END-STACKTRACE>>>")
            return (-2, "")
