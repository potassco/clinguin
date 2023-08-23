import json


class BasicTest08:
    @classmethod
    def get_reference_json(cls):
        json_dict = {
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
                    "attributes": [
                        {"id": "window", "key": "height", "value": "600"},
                        {"id": "window", "key": "width", "value": "600"},
                        {"id": "window", "key": "child_layout", "value": "absstatic"},
                    ],
                    "callbacks": [],
                    "children": [
                        {
                            "id": "f1",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "f1",
                                    "key": "background_color",
                                    "value": '"#ff0000"',
                                }
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "b1",
                                    "type": "button",
                                    "parent": "f1",
                                    "attributes": [
                                        {
                                            "id": "b1",
                                            "key": "label",
                                            "value": '"My button"',
                                        },
                                        {
                                            "id": "b1",
                                            "key": "background_color",
                                            "value": '"#00ff00"',
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "m3",
                            "type": "message",
                            "parent": "window",
                            "attributes": [
                                {"id": "m3", "key": "type", "value": "warning"},
                                {"id": "m3", "key": "title", "value": '"WARNING"'},
                                {
                                    "id": "m3",
                                    "key": "message",
                                    "value": '"WARNING MESSAGE"',
                                },
                            ],
                            "callbacks": [],
                            "children": [],
                        },
                        {
                            "id": "m2",
                            "type": "message",
                            "parent": "window",
                            "attributes": [
                                {"id": "m2", "key": "type", "value": "error"},
                                {"id": "m2", "key": "title", "value": '"ERROR"'},
                                {
                                    "id": "m2",
                                    "key": "message",
                                    "value": '"ERROR MESSAGE"',
                                },
                            ],
                            "callbacks": [],
                            "children": [],
                        },
                        {
                            "id": "m1",
                            "type": "message",
                            "parent": "window",
                            "attributes": [
                                {"id": "m1", "key": "type", "value": "info"},
                                {"id": "m1", "key": "title", "value": '"INFO"'},
                                {
                                    "id": "m1",
                                    "key": "message",
                                    "value": '"INFO MESSAGE"',
                                },
                            ],
                            "callbacks": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))
