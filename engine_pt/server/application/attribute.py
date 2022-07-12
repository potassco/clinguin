import json

class AttributeDto:
    def __init__(self, id, key, value):
        self.id = str(id)
        self.key = str(key)
        self.value = str(value)


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)



