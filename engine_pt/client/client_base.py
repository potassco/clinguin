import time

from client.api import Api
from client.call_dto import CallDto

from client.abstract_gui import AbstractGui
from client.tkinter_gui import TkinterGui

class ClientBase:

    endpoint_health = "health"

    def __init__(self):
        self.api = Api()
        self.connected = False

        self.solve_dto = CallDto("solve")

        self.gui_generator = TkinterGui(self)

    def connect(self):
        while (self.connected == False):
            (status_code, json) = self.api.get(self.endpoint_health)

            if status_code == 200:
                self.connected = True
            else:
                time.sleep(1)
                
            
    def startUp(self):
        self.connect()
        self.draw()

    def draw(self):
        (status_code, response) = self.api.post("", self.solve_dto)
        if status_code != 200:
            self.connected = False
            self.startUp()


        self.baseEngine(response)

        self.gui_generator.draw(response['children'][0]['id'])



    def baseEngine(self, response):
        children = response['children']

        for child in children:
            print(child)

            if hasattr(self.gui_generator, child['type']):
                method = getattr(self.gui_generator, child['type'])
                
                method(child['id'], child['parent'], child['attributes'], child['callbacks'])


                self.baseEngine(child)
            else:
                print("COULD NOT FIND ELEMENT-TYPE: " + child['type'])


    def assume(self, click_policy):
        print("Try to assume: " + click_policy)
        self.api.post("", CallDto(click_policy))
        time.sleep(1)
        print("Now solving :-)")
        self.draw()



