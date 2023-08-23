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


def get_server_error_alert():
    """
    Returns a JSON, which corresponds to valid clinguin json syntax and displays an error message.
    """
    return {
            "id": "root",
            "type": "root",
            "parent": "root",
            "attributes": [],
            "callbacks": [],
            "children": [
                {
                    "id": "window",
                    "type": "window",
                    "parent": "root",
                    "attributes": [],
                    "callbacks": [],
                    "children": [
                        {
                            "id": "message",
                            "type": "message",
                            "parent": "window",
                            "callbacks": [],
                            "attributes": [
                                {
                                    "id": "message",
                                    "key": "message",
                                    "value": '"Server Error (Check logs)"',
                                }
                            ],
                            "children": [],
                        },
                    ],
                }
            ],
        }
