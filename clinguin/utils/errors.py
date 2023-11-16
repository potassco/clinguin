"""
This module provides different errors for clinguin.
"""


class NoModelError(Exception):
    """
    The NoModelError is raised, if the provided logic program is unsatisfiable.
    """

    def __init__(self, core=None) -> None:
        super().__init__()
        self.core = core


def get_server_error_alert(message="", last_response=None):
    """
    Returns a JSON, which corresponds to valid clinguin json syntax and displays an error message.
    """
    error_alert = {
        "id": "server_error",
        "type": "message",
        "parent": "window",
        "attributes": [
            {
                "id": "server_error",
                "key": "message",
                "value": message + " Check the server logs for more details.",
            },
            {"id": "server_error", "key": "title", "value": "Server error"},
            {"id": "server_error", "key": "type", "value": "danger"},
        ],
        "when": [],
        "children": [],
    }

    if last_response is None:
        return {
            "id": "root",
            "type": "root",
            "parent": "root",
            "attributes": [],
            "when": [],
            "children": [
                {
                    "id": "window",
                    "type": "window",
                    "parent": "root",
                    "attributes": [],
                    "when": [],
                    "children": [error_alert],
                }
            ],
        }

    last_response.children[0].children.append(error_alert)
    return last_response
