import json


class BasicTest06:
    @classmethod
    def get_reference_json(cls):
        json_dict = {
            "id": "root",
            "type": "root",
            "parent": "root",
            "attributes": [],
            "do": [],
            "children": [
                {
                    "id": "w",
                    "type": "window",
                    "parent": "root",
                    "attributes": [
                        {"id": "w", "key": "background_color", "value": "pink"},
                        {"id": "w", "key": "child_layout", "value": "flex"},
                        {"id": "w", "key": "flex_direction", "value": '"row-reverse"'},
                    ],
                    "do": [],
                    "children": [
                        {
                            "id": "c3",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c3", "key": "border_width", "value": "3"},
                                {
                                    "id": "c3",
                                    "key": "background_color",
                                    "value": '"#00ff00"',
                                },
                                {"id": "c3", "key": "width", "value": "200"},
                                {"id": "c3", "key": "height", "value": "200"},
                            ],
                            "do": [],
                            "children": [],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c2", "key": "border_width", "value": "3"},
                                {
                                    "id": "c2",
                                    "key": "background_color",
                                    "value": '"#0000ff"',
                                },
                                {"id": "c2", "key": "width", "value": "200"},
                                {"id": "c2", "key": "height", "value": "200"},
                            ],
                            "do": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))
