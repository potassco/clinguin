import json

class FrontendPolicyDto:

    def __init__(self, function):
        self.function = function

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
