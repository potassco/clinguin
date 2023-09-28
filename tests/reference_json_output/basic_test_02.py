import json


class BasicTest02:
    @classmethod
    def get_reference_json(cls):
        json_dict = {
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
                    "attributes": [
                        {"id": "window", "key": "background_color", "value": "black"},
                        {"id": "window", "key": "resizable_x", "value": "0"},
                        {"id": "window", "key": "child_layout", "value": "flex"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "c(1)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {"id": "c(1)", "key": "child_layout", "value": "flex"},
                                {
                                    "id": "c(1)",
                                    "key": "background_color",
                                    "value": '"#00ff00"',
                                },
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "mbutton(1)",
                                    "type": "label",
                                    "parent": "c(1)",
                                    "attributes": [
                                        {
                                            "id": "mbutton(1)",
                                            "key": "foreground_color",
                                            "value": "red",
                                        },
                                        {
                                            "id": "mbutton(1)",
                                            "key": "label",
                                            "value": '"TEST 02\\n Hello Potsdam"',
                                        },
                                    ],
                                    "when": [],
                                    "children": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))
