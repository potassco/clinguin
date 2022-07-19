import time

from clinguin.client.api.api import Api
from clinguin.client.api.call_dto import CallDto

from clinguin.client.presentation.abstract_gui import AbstractGui
from clinguin.client.presentation.tkinter.tkinter_gui import TkinterGui

class ClientBase:

    endpoint_health = "health"

    def __init__(self, instance):
        self.api = Api(instance)
        self.connected = False
        self._instance = instance

        self.solve_dto = CallDto("solve")

        self.gui_generator = TkinterGui(self, instance)


    def startUp(self):
        self.connect()
        self.draw()
 
    def connect(self):
        while (self.connected == False):
            (status_code, json) = self.api.get(self.endpoint_health)

            if status_code == 200:
                self._instance.logger.info("Successfully connected to server")
                self.connected = True
            else:
                self._instance.logger.info("Waiting for connection")
                time.sleep(1)

    def draw(self):
        (status_code, response) = self.api.post("", self.solve_dto)
        if status_code == 200:
            self.baseEngine(response)
            self._instance.logger.info("Draw of GUI complete")
            self.gui_generator.draw(response['children'][0]['id'])
        else:
            self._instance.logger.error("Connection error, staus code: " + str(status_code))

            self.connected = False
            self.connect()


    def baseEngine(self, response):
        children = response['children']

        for child in children:

            if hasattr(self.gui_generator, child['type']):
                method = getattr(self.gui_generator, child['type'])
                
                method(child['id'], child['parent'], child['attributes'], child['callbacks'])


                self.baseEngine(child)
            else:
                self._instance.logger.warning("Could not find element type: " + child['type'])

    def assume(self, click_policy):
        self.api.post("", CallDto(click_policy))

        time.sleep(1)
        self.draw()



