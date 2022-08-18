import json
import httpx
import logging
import traceback

from .frontend_policy_dto import FrontendPolicyDto

class Api:

    def __init__(self, args, base_url="http://127.0.0.1:8000/"):

        self._logger = logging.getLogger(args.log_args['name'])

        self.base_url = base_url

    def get(self, endpoint):
        try:
            self._logger.debug("Sending GET to " +
                               str(self.base_url) + str(endpoint))
            r = httpx.get(self.base_url + endpoint, timeout=10000)
            j = r.json()
            # self._logger.debug(json.dumps(j, indent=4, sort_keys=True))
            return (r.status_code, r.json())
        except httpx.ConnectError:
            return (-1, "")
        except:
            self._logger.error("Some other connection-error occured.")
            self._logger.error("<<<BEGIN-STACKTRACE>>>")
            traceback.print_exc()
            self._logger.error("<<<END-STACKTRACE>>>")
            return (-2, "")



    def post(self, endpoint, body: FrontendPolicyDto):
        try:
            self._logger.debug("Sending POST to " +
                               str(self.base_url) +
                               str(endpoint) +
                               " with content:" +
                               str(body.function))
            
            data = body.toJSON()
            r = httpx.post(self.base_url + endpoint, data=data, timeout=10000)
            return (r.status_code, r.json())
        except httpx.ConnectError:
            self._logger.warning("Https-connect-error occured.")
            return (-1, "")
        except:
            self._logger.error("Some other connection-error occured.")
            self._logger.error("<<<BEGIN-STACKTRACE>>>")
            traceback.print_exc()
            self._logger.error("<<<END-STACKTRACE>>>")
            return (-2, "")


            
