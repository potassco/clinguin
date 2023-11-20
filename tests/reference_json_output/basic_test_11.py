import json


class BasicTest11:
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
                    "id": "w",
                    "type": "window",
                    "parent": "root",
                    "attributes": [{"id": "w", "key": "child_layout", "value": "flex"}],
                    "when": [],
                    "children": [
                        {
                            "id": "c1",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "c1",
                                    "key": "background_color",
                                    "value": '"#ff0000"',
                                },
                                {"id": "c1", "key": "width", "value": "500"},
                                {
                                    "id": "c1",
                                    "key": "flex_direction",
                                    "value": '"column"',
                                },
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "l1",
                                    "type": "label",
                                    "parent": "c1",
                                    "attributes": [
                                        {
                                            "id": "l1",
                                            "key": "label",
                                            "value": '"Hallo Welt!"',
                                        },
                                        {
                                            "id": "l1",
                                            "key": "background_color",
                                            "value": '"#00ff00"',
                                        },
                                    ],
                                    "when": [],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "c2",
                                    "key": "background_color",
                                    "value": '"#0000ff"',
                                },
                                {"id": "c2", "key": "width", "value": "100"},
                                {"id": "c2", "key": "height", "value": "100"},
                                {
                                    "id": "c2",
                                    "key": "flex_direction",
                                    "value": '"column"',
                                },
                            ],
                            "when": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))
