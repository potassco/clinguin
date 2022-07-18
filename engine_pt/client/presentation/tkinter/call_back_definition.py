
class CallBackDefinition:
    def __init__(self, id, parent, click_policy, callback):
        self._id = id
        self._parent = parent
        self._click_policy = click_policy
        self._callback = callback

    def __call__(self, *args):
        self._callback(self._id, self._parent, self._click_policy)

