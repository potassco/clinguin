import time
import logging

from clinguin.client import Api
from clinguin.client import FrontendPolicyDto

from clinguin.client import AbstractGui

class ClientBase:

    endpoint_health = "health"

    def __init__(self, args):
        self._logger = logging.getLogger(args.log_args['name'])

        self.api = Api(args)
        self.connected = False

        self.solve_dto = FrontendPolicyDto("solve")

        self.gui_generator = args.client(self, args)

    def startUp(self):
        self.connect()
        (status_code, response) = self.api.get("")
        # self._logger.debug(response)
        if status_code == 200:
            self.draw(response)
            self.gui_generator.draw(response['children'][0]['id'])
        else:
            logging.getLogger("client").error(
                "Connection error, status code: " + str(status_code))

            self.connected = False
            self.connect()

    def connect(self):
        while (self.connected == False):
            (status_code, json) = self.api.get(self.endpoint_health)

            if status_code == 200:
                self.connected = True
            else:
                logging.getLogger("client").info("Waiting for connection")
                time.sleep(1)

    def draw(self, response):
        self.baseEngine(response)

    def baseEngine(self, response):
        children = response['children']

        for child in children:
            if hasattr(self.gui_generator, child['type']):
                method = getattr(self.gui_generator, child['type'])

                method(
                    child['id'],
                    child['parent'],
                    child['attributes'],
                    child['callbacks'])
                self.baseEngine(child)
            else:
                logging.getLogger("client").error(
                    "Could not find element type: " + child['type'])

    def postWithPolicy(self, click_policy):
        (status_code, json) = self.api.post("solver", FrontendPolicyDto(click_policy))
        if status_code == 200:
            self.draw(json)
        else:
            logging.getLogger("client").error(
                "Connection error, status code: " + str(status_code))

            self.connected = False
            self.connect()


