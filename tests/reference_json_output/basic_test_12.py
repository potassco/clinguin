import json


class BasicTest12:
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
                        {"id": "w", "key": "child_layout", "value": "absstatic"}
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "c1",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c1", "key": "pos_x", "value": "0"},
                                {"id": "c1", "key": "pos_y", "value": "0"},
                                {"id": "c1", "key": "height", "value": "200"},
                                {"id": "c1", "key": "width", "value": "500"},
                                {"id": "c1", "key": "child_layout", "value": "flex"},
                                {
                                    "id": "c1",
                                    "key": "flex_direction",
                                    "value": "row_reverse",
                                },
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "b1",
                                    "type": "button",
                                    "parent": "c1",
                                    "attributes": [
                                        {
                                            "id": "b1",
                                            "key": "label",
                                            "value": '"Add Name"',
                                        }
                                    ],
                                    "when": [
                                        {
                                            "id": "b1",
                                            "event": "click",
                                            "action": "callback",
                                            "operation": "add_atom(name(_context_value(t1_content)))",
                                        }
                                    ],
                                    "children": [],
                                },
                                {
                                    "id": "t1",
                                    "type": "textfield",
                                    "parent": "c1",
                                    "attributes": [
                                        {
                                            "id": "t1",
                                            "key": "placeholder",
                                            "value": '"Type Name Here"',
                                        }
                                    ],
                                    "when": [
                                        {
                                            "id": "t1",
                                            "event": "input",
                                            "action": "context",
                                            "operation": "(t1_content,_value)",
                                        }
                                    ],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c2", "key": "pos_x", "value": "0"},
                                {"id": "c2", "key": "pos_y", "value": "250"},
                                {"id": "c2", "key": "height", "value": "200"},
                                {"id": "c2", "key": "width", "value": "500"},
                                {"id": "c2", "key": "child_layout", "value": "flex"},
                                {
                                    "id": "c2",
                                    "key": "flex_direction",
                                    "value": "column",
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
