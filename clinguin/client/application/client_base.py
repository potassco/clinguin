import time
import logging

from clinguin.client.api.api import Api
from clinguin.client.api.call_dto import CallDto

from clinguin.client.presentation.abstract_gui import AbstractGui
from clinguin.client.presentation.tkinter.tkinter_gui import TkinterGui


class ClientBase:

    endpoint_health = "health"

    def __init__(self, args):
        self._logger = logging.getLogger(args.log_args['name'])

        self.api = Api(args)
        self.connected = False

        self.solve_dto = CallDto("solve")

        self.gui_generator = TkinterGui(self)

    def startUp(self):
        self.connect()
        self.draw()

    def connect(self):
        while (self.connected == False):
            (status_code, json) = self.api.get(self.endpoint_health)

            if status_code == 200:
                self.connected = True
            else:
                logging.getLogger("client").info("Waiting for connection")
                time.sleep(1)

    def draw(self):
        (status_code, response) = self.api.get("")
        if status_code == 200:
            self.baseEngine(response)
            self.gui_generator.draw(response['children'][0]['id'])
        else:
            logging.getLogger("client").error(
                "Connection error, status code: " + str(status_code))

            self.connected = False
            self.connect()

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

    def assume(self, click_policy):
        self.api.post("solver", CallDto(click_policy))

        time.sleep(1)
        self.draw()
