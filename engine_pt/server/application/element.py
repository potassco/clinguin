import json

class ElementDto:
    def __init__(self, id, type, parent):
        self.id = str(id)
        self.type = str(type)
        self.parent = str(parent)
        self.children = []

    def setAttributes(self, attributes):
        self.attributes = attributes

    def setCallbacks(self, callbacks):
        self.callbacks = callbacks

    def addChild(self, child):
        self.children.append(child)


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)



