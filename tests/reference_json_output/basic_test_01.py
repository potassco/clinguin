import json


class BasicTest01:
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
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "flex"},
                    ],
                    "do": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "dropdown_menu",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "100"},
                                {"id": "c", "key": "height", "value": "50"},
                            ],
                            "do": [],
                            "children": [
                                {
                                    "id": "mi(2)",
                                    "type": "dropdown_menu_item",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "mi(2)", "key": "label", "value": "2"}
                                    ],
                                    "do": [
                                        {
                                            "id": "mi(2)",
                                            "action_type": "click",
                                            "interaction_type": "callback",
                                            "policy": "add_assumption(p(2))",
                                        }
                                    ],
                                    "children": [],
                                },
                                {
                                    "id": "mi(1)",
                                    "type": "dropdown_menu_item",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "mi(1)", "key": "label", "value": "1"}
                                    ],
                                    "do": [
                                        {
                                            "id": "mi(1)",
                                            "action_type": "click",
                                            "interaction_type": "callback",
                                            "policy": "add_assumption(p(1))",
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
                                {"id": "c2", "key": "width", "value": "100"},
                                {"id": "c2", "key": "height", "value": "50"},
                                {"id": "c2", "key": "border_width", "value": "20"},
                                {"id": "c2", "key": "border_color", "value": "pink"},
                                {"id": "c2", "key": "background_color", "value": "red"},
                            ],
                            "do": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))

    @classmethod
    def post_p_1_reference_json(cls):
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
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "flex"},
                    ],
                    "do": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "dropdown_menu",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "100"},
                                {"id": "c", "key": "height", "value": "50"},
                                {"id": "c", "key": "selected", "value": "mi(1)"},
                            ],
                            "do": [],
                            "children": [
                                {
                                    "id": "mi(1)",
                                    "type": "dropdown_menu_item",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "mi(1)", "key": "label", "value": "1"}
                                    ],
                                    "do": [
                                        {
                                            "id": "mi(1)",
                                            "action_type": "click",
                                            "interaction_type": "callback",
                                            "policy": "add_assumption(p(1))",
                                        }
                                    ],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c2", "key": "width", "value": "100"},
                                {"id": "c2", "key": "height", "value": "50"},
                                {"id": "c2", "key": "border_width", "value": "20"},
                                {"id": "c2", "key": "border_color", "value": "pink"},
                                {"id": "c2", "key": "background_color", "value": "red"},
                            ],
                            "do": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))

    @classmethod
    def get_p_1_reference_json(cls):
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
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "flex"},
                    ],
                    "do": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "dropdown_menu",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "100"},
                                {"id": "c", "key": "height", "value": "50"},
                                {"id": "c", "key": "selected", "value": "mi(1)"},
                            ],
                            "do": [],
                            "children": [
                                {
                                    "id": "mi(1)",
                                    "type": "dropdown_menu_item",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "mi(1)", "key": "label", "value": "1"}
                                    ],
                                    "do": [
                                        {
                                            "id": "mi(1)",
                                            "action_type": "click",
                                            "interaction_type": "callback",
                                            "policy": "add_assumption(p(1))",
                                        }
                                    ],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c2", "key": "width", "value": "100"},
                                {"id": "c2", "key": "height", "value": "50"},
                                {"id": "c2", "key": "border_width", "value": "20"},
                                {"id": "c2", "key": "border_color", "value": "pink"},
                                {"id": "c2", "key": "background_color", "value": "red"},
                            ],
                            "do": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))

    @classmethod
    def post_p_2_reference_json(cls):
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
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "flex"},
                    ],
                    "do": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "dropdown_menu",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "100"},
                                {"id": "c", "key": "height", "value": "50"},
                                {"id": "c", "key": "selected", "value": "mi(2)"},
                            ],
                            "do": [],
                            "children": [
                                {
                                    "id": "mi(2)",
                                    "type": "dropdown_menu_item",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "mi(2)", "key": "label", "value": "2"}
                                    ],
                                    "do": [
                                        {
                                            "id": "mi(2)",
                                            "action_type": "click",
                                            "interaction_type": "callback",
                                            "policy": "add_assumption(p(2))",
                                        }
                                    ],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c2", "key": "width", "value": "100"},
                                {"id": "c2", "key": "height", "value": "50"},
                                {"id": "c2", "key": "border_width", "value": "20"},
                                {"id": "c2", "key": "border_color", "value": "pink"},
                                {"id": "c2", "key": "background_color", "value": "red"},
                            ],
                            "do": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }
        return json.loads(json.dumps(json_dict))

    @classmethod
    def get_p_2_reference_json(cls):
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
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "flex"},
                    ],
                    "do": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "dropdown_menu",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "100"},
                                {"id": "c", "key": "height", "value": "50"},
                                {"id": "c", "key": "selected", "value": "mi(2)"},
                            ],
                            "do": [],
                            "children": [
                                {
                                    "id": "mi(2)",
                                    "type": "dropdown_menu_item",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "mi(2)", "key": "label", "value": "2"}
                                    ],
                                    "do": [
                                        {
                                            "id": "mi(2)",
                                            "action_type": "click",
                                            "interaction_type": "callback",
                                            "policy": "add_assumption(p(2))",
                                        }
                                    ],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c2", "key": "width", "value": "100"},
                                {"id": "c2", "key": "height", "value": "50"},
                                {"id": "c2", "key": "border_width", "value": "20"},
                                {"id": "c2", "key": "border_color", "value": "pink"},
                                {"id": "c2", "key": "background_color", "value": "red"},
                            ],
                            "do": [],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))
