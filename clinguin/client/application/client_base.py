"""
Module that contains the ClientBase class
"""
import time
import logging

from clinguin.utils import CaseConverter, Logger
from clinguin.client.api.api import Api
from clinguin.client.api.frontend_policy_dto import FrontendPolicyDto

class ClientBase:   
    """
    ClientBase is the ''base'' of the client. It contains the logic which is responsible for connecting to the server, what to do in case of errors, forward the Json to the correct GUI, etc.
    """

    endpoint_health = "health"

    def __init__(self, args):
        self._logger = logging.getLogger(Logger.client_logger_name)

        self.api = Api()
        self.connected = False

        self.solve_dto = FrontendPolicyDto("solve")

        self.gui_generator = args.client(self, args)

    def start_up(self):
        self.connect()
        (status_code, response) = self.api.get("")
        if status_code == 200:
            self.draw(response)
            self.gui_generator.draw(response['children'][0]['id'])
        else:
            self._logger.error(
                "Connection error, status code: %s", str(status_code))

            self.connected = False
            self.connect()

    def connect(self):
        while not self.connected:
            (status_code, _) = self.api.get(self.endpoint_health)

            if status_code == 200:
                self.connected = True
            else:
                self._logger.info("Waiting for connection")
                time.sleep(1)

    def draw(self, response):
        self.base_engine(response)

    def base_engine(self, response):
        """
        Handles the response of the server to draw the GUI. For this it iterates through the received Json/Dict in a top-down preorder fashion.

        Parameters:
            response (dict): Json from which one can draw the GUI.
        """

        children = response['children']

        for child in children:
            snake_case_name = child['type']
            camel_case_name = CaseConverter.snake_case_to_camel_case(snake_case_name)

            method = None

            if hasattr(self.gui_generator, camel_case_name):
                method = getattr(self.gui_generator, camel_case_name)
            elif hasattr(self.gui_generator, snake_case_name):
                method = getattr(self.gui_generator, snake_case_name)

            if method and callable(method):
                method(
                    child['id'],
                    child['parent'],
                    child['attributes'],
                    child['callbacks'])
                self.base_engine(child)
            else:
                self._logger.error(
                    "Could not find element type: %s", child['type'])

    def post_with_policy(self, click_policy):
        (status_code, json) = self.api.post("backend", FrontendPolicyDto(click_policy))
        if status_code == 200:
            self.draw(json)
        else:
            self._logger.error(
                "Connection error, status code: %s", str(status_code))

            self.connected = False
            self.connect()


