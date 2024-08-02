"""
Module that contains the ClientBase class
"""

import logging
import time

from clinguin.client.api.api import Api
from clinguin.client.api.frontend_operation_dto import FrontendOperationDto
from clinguin.utils import CaseConverter, Logger


class ClientBase:
    """
    ClientBase is the ''base'' of the client.
    It contains the logic which is responsible for connecting to the server,
    what to do in case of errors, forward the Json to the correct GUI, etc.
    """

    endpoint_health = "health"

    def __init__(self, args):
        self._logger = logging.getLogger(Logger.client_logger_name)

        self.api = Api()
        self.connected = False

        self.solve_dto = FrontendOperationDto("solve")

        self.frontend_generator = args.frontend(self, args)

    def start_up(self):
        """
        Code executed on first startup.
        """
        self.connect()
        (status_code, response) = self.api.get("")
        if status_code == 200:
            self.draw(response)
            self.frontend_generator.draw(response["children"][0]["id"])
        else:
            self._logger.error("Connection error, status code: %s", str(status_code))

            self.connected = False
            self.connect()

    def connect(self):
        """
        Connect/reconnect to server.
        """
        while not self.connected:
            (status_code, _) = self.api.get(self.endpoint_health)

            if status_code == 200:
                self.connected = True
            else:
                self._logger.info("Waiting for connection")
                time.sleep(1)

    def draw(self, response):
        """
        Draws the GUI.
        """
        self.base_engine(response)
        if len(response["children"]) == 0:
            raise Exception("Empty UI! check the logs and the provided files.")
        self.frontend_generator.draw_postprocessing(response["children"][0]["id"])

    def base_engine(self, response):
        """
        Handles the response of the server to draw the GUI.
        For this it iterates through the received Json/Dict
        in a top-down preorder fashion.

        Parameters:
            response (dict): Json from which one can draw the GUI.
        """
        children = response["children"]

        for child in children:
            snake_case_name = child["type"]
            camel_case_name = CaseConverter.snake_case_to_camel_case(snake_case_name)

            method = None

            if hasattr(self.frontend_generator, camel_case_name):
                method = getattr(self.frontend_generator, camel_case_name)

            elif hasattr(self.frontend_generator, snake_case_name):
                method = getattr(self.frontend_generator, snake_case_name)

            if method and callable(method):
                method(
                    child["id"],
                    child["parent"],
                    child["attributes"],
                    child["when"],
                )
                self.base_engine(child)
            else:
                self._logger.error("Could not find element type: %s", child["type"])

    def post_with_operation(self, click_operation):
        """
        Prepare post request for API.
        """
        (status_code, json) = self.api.post(
            "backend", FrontendOperationDto(click_operation)
        )
        if status_code == 200:
            self.draw(json)
        else:
            self._logger.error("Connection error, status code: %s", str(status_code))

            self.connected = False
            self.connect()
