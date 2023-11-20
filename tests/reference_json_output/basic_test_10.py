import json


class BasicTest10:
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
                    "attributes": [
                        {"id": "w", "key": "height", "value": "800"},
                        {"id": "w", "key": "width", "value": "600"},
                        {"id": "w", "key": "child_layout", "value": "flex"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "c6",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "c6",
                                    "key": "background_color",
                                    "value": '"#ff00ff"',
                                },
                                {"id": "c6", "key": "width", "value": "200"},
                                {"id": "c6", "key": "height", "value": "200"},
                                {
                                    "id": "c6",
                                    "key": "flex_direction",
                                    "value": '"column_reverse"',
                                },
                            ],
                            "when": [],
                            "children": [],
                        },
                        {
                            "id": "c5",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "c5",
                                    "key": "background_color",
                                    "value": '"#00ffff"',
                                },
                                {"id": "c5", "key": "width", "value": "200"},
                                {"id": "c5", "key": "height", "value": "200"},
                                {
                                    "id": "c5",
                                    "key": "flex_direction",
                                    "value": '"column"',
                                },
                            ],
                            "when": [],
                            "children": [],
                        },
                        {
                            "id": "c4",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "c4",
                                    "key": "background_color",
                                    "value": '"#ffff00"',
                                },
                                {"id": "c4", "key": "width", "value": "200"},
                                {"id": "c4", "key": "height", "value": "200"},
                                {
                                    "id": "c4",
                                    "key": "flex_direction",
                                    "value": '"column"',
                                },
                            ],
                            "when": [],
                            "children": [],
                        },
                        {
                            "id": "c3",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "c3",
                                    "key": "background_color",
                                    "value": '"#00ff00"',
                                },
                                {"id": "c3", "key": "width", "value": "200"},
                                {"id": "c3", "key": "height", "value": "200"},
                                {
                                    "id": "c3",
                                    "key": "flex_direction",
                                    "value": '"row_reverse"',
                                },
                            ],
                            "when": [],
                            "children": [],
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
                                {"id": "c2", "key": "width", "value": "200"},
                                {"id": "c2", "key": "height", "value": "200"},
                                {
                                    "id": "c2",
                                    "key": "flex_direction",
                                    "value": '"row_reverse"',
                                },
                            ],
                            "when": [],
                            "children": [],
                        },
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
                                {"id": "c1", "key": "width", "value": "200"},
                                {"id": "c1", "key": "height", "value": "200"},
                                {
                                    "id": "c1",
                                    "key": "flex_direction",
                                    "value": '"row_reverse"',
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
