import json


class CallbackDto:
    def __init__(self, id, action, policy):
        self.id = str(id)
        self.action = str(action)
        self.policy = str(policy)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def clone(self):
        return CallbackDto(self.id, self.action, self.policy)
