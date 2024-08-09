import json


class BasicTest09:
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
                        {"id": "window", "key": "height", "value": "400"},
                        {"id": "window", "key": "width", "value": "400"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "dpm",
                            "type": "dropdown_menu",
                            "parent": "window",
                            "attributes": [],
                            "when": [],
                            "children": [
                                {
                                    "id": "dmp(1)",
                                    "type": "dropdown_menu_item",
                                    "parent": "dpm",
                                    "attributes": [
                                        {"id": "dmp(1)", "key": "label", "value": "1"}
                                    ],
                                    "when": [
                                        {
                                            "id": "dmp(1)",
                                            "event": "click",
                                            "action": "callback",
                                            "operation": "add_assumption(p(1),true)",
                                        }
                                    ],
                                    "children": [],
                                },
                                {
                                    "id": "dmp(2)",
                                    "type": "dropdown_menu_item",
                                    "parent": "dpm",
                                    "attributes": [
                                        {"id": "dmp(2)", "key": "label", "value": "2"}
                                    ],
                                    "when": [
                                        {
                                            "id": "dmp(2)",
                                            "event": "click",
                                            "action": "callback",
                                            "operation": "add_assumption(p(2),true)",
                                        }
                                    ],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "l",
                            "type": "label",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "l",
                                    "key": "label",
                                    "value": '"Clear assumptions"',
                                },
                                {"id": "l", "key": "font_weight", "value": '"italic"'},
                                {"id": "l", "key": "font_size", "value": "20"},
                                {
                                    "id": "l",
                                    "key": "background_color",
                                    "value": '"#ff4d4d"',
                                },
                                {"id": "l", "key": "on_hover", "value": '"True"'},
                                {
                                    "id": "l",
                                    "key": "on_hover_background_color",
                                    "value": '"#990000"',
                                },
                            ],
                            "when": [
                                {
                                    "id": "l",
                                    "event": "click",
                                    "action": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
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
            "when": [],
            "children": [
                {
                    "id": "window",
                    "type": "window",
                    "parent": "root",
                    "attributes": [
                        {"id": "window", "key": "height", "value": "400"},
                        {"id": "window", "key": "width", "value": "400"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "dpm",
                            "type": "dropdown_menu",
                            "parent": "window",
                            "attributes": [
                                {"id": "dpm", "key": "selected", "value": "2"}
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "dmp(2)",
                                    "type": "dropdown_menu_item",
                                    "parent": "dpm",
                                    "attributes": [
                                        {"id": "dmp(2)", "key": "label", "value": "2"}
                                    ],
                                    "when": [
                                        {
                                            "id": "dmp(2)",
                                            "event": "click",
                                            "action": "callback",
                                            "operation": "add_assumption(p(2),true)",
                                        }
                                    ],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "l",
                            "type": "label",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "l",
                                    "key": "label",
                                    "value": '"Clear assumptions"',
                                },
                                {"id": "l", "key": "font_weight", "value": '"italic"'},
                                {"id": "l", "key": "font_size", "value": "20"},
                                {
                                    "id": "l",
                                    "key": "background_color",
                                    "value": '"#ff4d4d"',
                                },
                                {"id": "l", "key": "on_hover", "value": '"True"'},
                                {
                                    "id": "l",
                                    "key": "on_hover_background_color",
                                    "value": '"#990000"',
                                },
                            ],
                            "when": [
                                {
                                    "id": "l",
                                    "event": "click",
                                    "action": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
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
            "when": [],
            "children": [
                {
                    "id": "window",
                    "type": "window",
                    "parent": "root",
                    "attributes": [
                        {"id": "window", "key": "height", "value": "400"},
                        {"id": "window", "key": "width", "value": "400"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "dpm",
                            "type": "dropdown_menu",
                            "parent": "window",
                            "attributes": [
                                {"id": "dpm", "key": "selected", "value": "2"}
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "dmp(2)",
                                    "type": "dropdown_menu_item",
                                    "parent": "dpm",
                                    "attributes": [
                                        {"id": "dmp(2)", "key": "label", "value": "2"}
                                    ],
                                    "when": [
                                        {
                                            "id": "dmp(2)",
                                            "event": "click",
                                            "action": "callback",
                                            "operation": "add_assumption(p(2),true)",
                                        }
                                    ],
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "id": "l",
                            "type": "label",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "l",
                                    "key": "label",
                                    "value": '"Clear assumptions"',
                                },
                                {"id": "l", "key": "font_weight", "value": '"italic"'},
                                {"id": "l", "key": "font_size", "value": "20"},
                                {
                                    "id": "l",
                                    "key": "background_color",
                                    "value": '"#ff4d4d"',
                                },
                                {"id": "l", "key": "on_hover", "value": '"True"'},
                                {
                                    "id": "l",
                                    "key": "on_hover_background_color",
                                    "value": '"#990000"',
                                },
                            ],
                            "when": [
                                {
                                    "id": "l",
                                    "event": "click",
                                    "action": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))

    @classmethod
    def post_p_3_reference_json(cls):
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
                        {"id": "window", "key": "height", "value": "400"},
                        {"id": "window", "key": "width", "value": "400"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "dpm",
                            "type": "dropdown_menu",
                            "parent": "window",
                            "attributes": [],
                            "when": [],
                            "children": [
                                {
                                    "id": "dmp(1)",
                                    "type": "dropdown_menu_item",
                                    "parent": "dpm",
                                    "attributes": [
                                        {"id": "dmp(1)", "key": "label", "value": "1"}
                                    ],
                                    "when": [
                                        {
                                            "id": "dmp(1)",
                                            "event": "click",
                                            "action": "callback",
                                            "operation": "add_assumption(p(1),true)",
                                        }
                                    ],
                                    "children": [],
                                },
                                {
                                    "id": "dmp(2)",
                                    "type": "dropdown_menu_item",
                                    "parent": "dpm",
                                    "attributes": [
                                        {"id": "dmp(2)", "key": "label", "value": "2"}
                                    ],
                                    "when": [
                                        {
                                            "id": "dmp(2)",
                                            "event": "click",
                                            "action": "callback",
                                            "operation": "add_assumption(p(2),true)",
                                        }
                                    ],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "l",
                            "type": "label",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "l",
                                    "key": "label",
                                    "value": '"Clear assumptions"',
                                },
                                {"id": "l", "key": "font_weight", "value": '"italic"'},
                                {"id": "l", "key": "font_size", "value": "20"},
                                {
                                    "id": "l",
                                    "key": "background_color",
                                    "value": '"#ff4d4d"',
                                },
                                {"id": "l", "key": "on_hover", "value": '"True"'},
                                {
                                    "id": "l",
                                    "key": "on_hover_background_color",
                                    "value": '"#990000"',
                                },
                            ],
                            "when": [
                                {
                                    "id": "l",
                                    "event": "click",
                                    "action": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))
