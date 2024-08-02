import json


class BasicTest03:
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
                        {"id": "w", "key": "height", "value": "500"},
                        {"id": "w", "key": "width", "value": "500"},
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "relstatic"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "250"},
                                {"id": "c", "key": "height", "value": "150"},
                                {"id": "c", "key": "border_width", "value": "2"},
                                {"id": "c", "key": "on_hover", "value": "true"},
                                {
                                    "id": "c",
                                    "key": "on_hover_background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "c",
                                    "key": "on_hover_border_color",
                                    "value": "red",
                                },
                                {"id": "c", "key": "pos_x", "value": "25"},
                                {"id": "c", "key": "pos_y", "value": "0"},
                                {
                                    "id": "c",
                                    "key": "child_layout",
                                    "value": "absstatic",
                                },
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "m",
                                    "type": "dropdown_menu",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "m", "key": "width", "value": "100"},
                                        {"id": "m", "key": "height", "value": "50"},
                                        {"id": "m", "key": "pos_x", "value": "0"},
                                        {"id": "m", "key": "pos_y", "value": "50"},
                                        {
                                            "id": "m",
                                            "key": "background_color",
                                            "value": "black",
                                        },
                                        {
                                            "id": "m",
                                            "key": "foreground_color",
                                            "value": "white",
                                        },
                                        {"id": "m", "key": "on_hover", "value": "true"},
                                        {
                                            "id": "m",
                                            "key": "on_hover_background_color",
                                            "value": "white",
                                        },
                                        {
                                            "id": "m",
                                            "key": "on_hover_foreground_color",
                                            "value": "black",
                                        },
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "mi(2)",
                                            "type": "dropdown_menu_item",
                                            "parent": "m",
                                            "attributes": [
                                                {
                                                    "id": "mi(2)",
                                                    "key": "label",
                                                    "value": "2",
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "mi(2)",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "operation": "add_assumption(p(2))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "mi(1)",
                                            "type": "dropdown_menu_item",
                                            "parent": "m",
                                            "attributes": [
                                                {
                                                    "id": "mi(1)",
                                                    "key": "label",
                                                    "value": "1",
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "mi(1)",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "operation": "add_assumption(p(1))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "c4",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "c4", "key": "width", "value": "146"},
                                        {"id": "c4", "key": "height", "value": "146"},
                                        {
                                            "id": "c4",
                                            "key": "background_color",
                                            "value": "beige",
                                        },
                                        {"id": "c4", "key": "pos_x", "value": "100"},
                                        {"id": "c4", "key": "pos_y", "value": "0"},
                                        {
                                            "id": "c4",
                                            "key": "child_layout",
                                            "value": "grid",
                                        },
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "c(3,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "cc",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "cc", "key": "width", "value": "100"},
                                        {"id": "cc", "key": "height", "value": "50"},
                                        {
                                            "id": "cc",
                                            "key": "background_color",
                                            "value": "green",
                                        },
                                        {
                                            "id": "cc",
                                            "key": "border_width",
                                            "value": "2",
                                        },
                                        {"id": "cc", "key": "pos_x", "value": "0"},
                                        {"id": "cc", "key": "pos_y", "value": "0"},
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "b",
                            "type": "button",
                            "parent": "w",
                            "attributes": [
                                {"id": "b", "key": "background_color", "value": "blue"},
                                {
                                    "id": "b",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "b", "key": "label", "value": '"Clear!"'},
                                {"id": "b", "key": "on_hover", "value": "true"},
                                {
                                    "id": "b",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "b",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "b", "key": "font_size", "value": "18"},
                                {"id": "b", "key": "font_weight", "value": '"bi"'},
                                {"id": "b", "key": "width", "value": "100"},
                                {"id": "b", "key": "height", "value": "50"},
                                {"id": "b", "key": "pos_x", "value": "40"},
                                {"id": "b", "key": "pos_y", "value": "70"},
                            ],
                            "when": [
                                {
                                    "id": "b",
                                    "event": "click",
                                    "interaction_type": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
                            "children": [],
                        },
                        {
                            "id": "l1",
                            "type": "label",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "l1",
                                    "key": "background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "l1",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "l1", "key": "label", "value": '"Clear!"'},
                                {"id": "l1", "key": "on_hover", "value": "true"},
                                {
                                    "id": "l1",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "l1",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "l1", "key": "font_size", "value": "15"},
                                {"id": "l1", "key": "font_weight", "value": '"i"'},
                                {"id": "l1", "key": "width", "value": "100"},
                                {"id": "l1", "key": "height", "value": "50"},
                                {"id": "l1", "key": "pos_x", "value": "40"},
                                {"id": "l1", "key": "pos_y", "value": "50"},
                            ],
                            "when": [
                                {
                                    "id": "l1",
                                    "event": "click",
                                    "interaction_type": "callback",
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
                    "id": "w",
                    "type": "window",
                    "parent": "root",
                    "attributes": [
                        {"id": "w", "key": "height", "value": "500"},
                        {"id": "w", "key": "width", "value": "500"},
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "relstatic"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "250"},
                                {"id": "c", "key": "height", "value": "150"},
                                {"id": "c", "key": "border_width", "value": "2"},
                                {"id": "c", "key": "on_hover", "value": "true"},
                                {
                                    "id": "c",
                                    "key": "on_hover_background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "c",
                                    "key": "on_hover_border_color",
                                    "value": "red",
                                },
                                {"id": "c", "key": "pos_x", "value": "25"},
                                {"id": "c", "key": "pos_y", "value": "0"},
                                {
                                    "id": "c",
                                    "key": "child_layout",
                                    "value": "absstatic",
                                },
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "m",
                                    "type": "dropdown_menu",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "m", "key": "width", "value": "100"},
                                        {"id": "m", "key": "height", "value": "50"},
                                        {"id": "m", "key": "pos_x", "value": "0"},
                                        {"id": "m", "key": "pos_y", "value": "50"},
                                        {
                                            "id": "m",
                                            "key": "background_color",
                                            "value": "black",
                                        },
                                        {
                                            "id": "m",
                                            "key": "foreground_color",
                                            "value": "white",
                                        },
                                        {"id": "m", "key": "on_hover", "value": "true"},
                                        {
                                            "id": "m",
                                            "key": "on_hover_background_color",
                                            "value": "white",
                                        },
                                        {
                                            "id": "m",
                                            "key": "on_hover_foreground_color",
                                            "value": "black",
                                        },
                                        {"id": "m", "key": "selected", "value": "1"},
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "mi(1)",
                                            "type": "dropdown_menu_item",
                                            "parent": "m",
                                            "attributes": [
                                                {
                                                    "id": "mi(1)",
                                                    "key": "label",
                                                    "value": "1",
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "mi(1)",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "operation": "add_assumption(p(1))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "c4",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "c4", "key": "width", "value": "146"},
                                        {"id": "c4", "key": "height", "value": "146"},
                                        {
                                            "id": "c4",
                                            "key": "background_color",
                                            "value": "beige",
                                        },
                                        {"id": "c4", "key": "pos_x", "value": "100"},
                                        {"id": "c4", "key": "pos_y", "value": "0"},
                                        {
                                            "id": "c4",
                                            "key": "child_layout",
                                            "value": "grid",
                                        },
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "c(3,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "cc",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "cc", "key": "width", "value": "100"},
                                        {"id": "cc", "key": "height", "value": "50"},
                                        {
                                            "id": "cc",
                                            "key": "background_color",
                                            "value": "green",
                                        },
                                        {
                                            "id": "cc",
                                            "key": "border_width",
                                            "value": "2",
                                        },
                                        {"id": "cc", "key": "pos_x", "value": "0"},
                                        {"id": "cc", "key": "pos_y", "value": "0"},
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "b",
                            "type": "button",
                            "parent": "w",
                            "attributes": [
                                {"id": "b", "key": "background_color", "value": "blue"},
                                {
                                    "id": "b",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "b", "key": "label", "value": '"Clear!"'},
                                {"id": "b", "key": "on_hover", "value": "true"},
                                {
                                    "id": "b",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "b",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "b", "key": "font_size", "value": "18"},
                                {"id": "b", "key": "font_weight", "value": '"bi"'},
                                {"id": "b", "key": "width", "value": "100"},
                                {"id": "b", "key": "height", "value": "50"},
                                {"id": "b", "key": "pos_x", "value": "40"},
                                {"id": "b", "key": "pos_y", "value": "70"},
                            ],
                            "when": [
                                {
                                    "id": "b",
                                    "event": "click",
                                    "interaction_type": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
                            "children": [],
                        },
                        {
                            "id": "l1",
                            "type": "label",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "l1",
                                    "key": "background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "l1",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "l1", "key": "label", "value": '"Clear!"'},
                                {"id": "l1", "key": "on_hover", "value": "true"},
                                {
                                    "id": "l1",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "l1",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "l1", "key": "font_size", "value": "15"},
                                {"id": "l1", "key": "font_weight", "value": '"i"'},
                                {"id": "l1", "key": "width", "value": "100"},
                                {"id": "l1", "key": "height", "value": "50"},
                                {"id": "l1", "key": "pos_x", "value": "40"},
                                {"id": "l1", "key": "pos_y", "value": "50"},
                            ],
                            "when": [
                                {
                                    "id": "l1",
                                    "event": "click",
                                    "interaction_type": "callback",
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
    def post_p_2_reference_json(cls):
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
                        {"id": "w", "key": "height", "value": "500"},
                        {"id": "w", "key": "width", "value": "500"},
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "relstatic"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "250"},
                                {"id": "c", "key": "height", "value": "150"},
                                {"id": "c", "key": "border_width", "value": "2"},
                                {"id": "c", "key": "on_hover", "value": "true"},
                                {
                                    "id": "c",
                                    "key": "on_hover_background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "c",
                                    "key": "on_hover_border_color",
                                    "value": "red",
                                },
                                {"id": "c", "key": "pos_x", "value": "25"},
                                {"id": "c", "key": "pos_y", "value": "0"},
                                {
                                    "id": "c",
                                    "key": "child_layout",
                                    "value": "absstatic",
                                },
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "m",
                                    "type": "dropdown_menu",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "m", "key": "width", "value": "100"},
                                        {"id": "m", "key": "height", "value": "50"},
                                        {"id": "m", "key": "pos_x", "value": "0"},
                                        {"id": "m", "key": "pos_y", "value": "50"},
                                        {
                                            "id": "m",
                                            "key": "background_color",
                                            "value": "black",
                                        },
                                        {
                                            "id": "m",
                                            "key": "foreground_color",
                                            "value": "white",
                                        },
                                        {"id": "m", "key": "on_hover", "value": "true"},
                                        {
                                            "id": "m",
                                            "key": "on_hover_background_color",
                                            "value": "white",
                                        },
                                        {
                                            "id": "m",
                                            "key": "on_hover_foreground_color",
                                            "value": "black",
                                        },
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "mi(2)",
                                            "type": "dropdown_menu_item",
                                            "parent": "m",
                                            "attributes": [
                                                {
                                                    "id": "mi(2)",
                                                    "key": "label",
                                                    "value": "2",
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "mi(2)",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "operation": "add_assumption(p(2))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "mi(1)",
                                            "type": "dropdown_menu_item",
                                            "parent": "m",
                                            "attributes": [
                                                {
                                                    "id": "mi(1)",
                                                    "key": "label",
                                                    "value": "1",
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "mi(1)",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "operation": "add_assumption(p(1))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "c4",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "c4", "key": "width", "value": "146"},
                                        {"id": "c4", "key": "height", "value": "146"},
                                        {
                                            "id": "c4",
                                            "key": "background_color",
                                            "value": "beige",
                                        },
                                        {"id": "c4", "key": "pos_x", "value": "100"},
                                        {"id": "c4", "key": "pos_y", "value": "0"},
                                        {
                                            "id": "c4",
                                            "key": "child_layout",
                                            "value": "grid",
                                        },
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "c(3,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "cc",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "cc", "key": "width", "value": "100"},
                                        {"id": "cc", "key": "height", "value": "50"},
                                        {
                                            "id": "cc",
                                            "key": "background_color",
                                            "value": "green",
                                        },
                                        {
                                            "id": "cc",
                                            "key": "border_width",
                                            "value": "2",
                                        },
                                        {"id": "cc", "key": "pos_x", "value": "0"},
                                        {"id": "cc", "key": "pos_y", "value": "0"},
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "b",
                            "type": "button",
                            "parent": "w",
                            "attributes": [
                                {"id": "b", "key": "background_color", "value": "blue"},
                                {
                                    "id": "b",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "b", "key": "label", "value": '"Clear!"'},
                                {"id": "b", "key": "on_hover", "value": "true"},
                                {
                                    "id": "b",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "b",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "b", "key": "font_size", "value": "18"},
                                {"id": "b", "key": "font_weight", "value": '"bi"'},
                                {"id": "b", "key": "width", "value": "100"},
                                {"id": "b", "key": "height", "value": "50"},
                                {"id": "b", "key": "pos_x", "value": "40"},
                                {"id": "b", "key": "pos_y", "value": "70"},
                            ],
                            "when": [
                                {
                                    "id": "b",
                                    "event": "click",
                                    "interaction_type": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
                            "children": [],
                        },
                        {
                            "id": "l1",
                            "type": "label",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "l1",
                                    "key": "background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "l1",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "l1", "key": "label", "value": '"Clear!"'},
                                {"id": "l1", "key": "on_hover", "value": "true"},
                                {
                                    "id": "l1",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "l1",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "l1", "key": "font_size", "value": "15"},
                                {"id": "l1", "key": "font_weight", "value": '"i"'},
                                {"id": "l1", "key": "width", "value": "100"},
                                {"id": "l1", "key": "height", "value": "50"},
                                {"id": "l1", "key": "pos_x", "value": "40"},
                                {"id": "l1", "key": "pos_y", "value": "50"},
                            ],
                            "when": [
                                {
                                    "id": "l1",
                                    "event": "click",
                                    "interaction_type": "callback",
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
                    "id": "w",
                    "type": "window",
                    "parent": "root",
                    "attributes": [
                        {"id": "w", "key": "height", "value": "500"},
                        {"id": "w", "key": "width", "value": "500"},
                        {"id": "w", "key": "background_color", "value": "white"},
                        {"id": "w", "key": "child_layout", "value": "relstatic"},
                    ],
                    "when": [],
                    "children": [
                        {
                            "id": "c",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c", "key": "width", "value": "250"},
                                {"id": "c", "key": "height", "value": "150"},
                                {"id": "c", "key": "border_width", "value": "2"},
                                {"id": "c", "key": "on_hover", "value": "true"},
                                {
                                    "id": "c",
                                    "key": "on_hover_background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "c",
                                    "key": "on_hover_border_color",
                                    "value": "red",
                                },
                                {"id": "c", "key": "pos_x", "value": "25"},
                                {"id": "c", "key": "pos_y", "value": "0"},
                                {
                                    "id": "c",
                                    "key": "child_layout",
                                    "value": "absstatic",
                                },
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "m",
                                    "type": "dropdown_menu",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "m", "key": "width", "value": "100"},
                                        {"id": "m", "key": "height", "value": "50"},
                                        {"id": "m", "key": "pos_x", "value": "0"},
                                        {"id": "m", "key": "pos_y", "value": "50"},
                                        {
                                            "id": "m",
                                            "key": "background_color",
                                            "value": "black",
                                        },
                                        {
                                            "id": "m",
                                            "key": "foreground_color",
                                            "value": "white",
                                        },
                                        {"id": "m", "key": "on_hover", "value": "true"},
                                        {
                                            "id": "m",
                                            "key": "on_hover_background_color",
                                            "value": "white",
                                        },
                                        {
                                            "id": "m",
                                            "key": "on_hover_foreground_color",
                                            "value": "black",
                                        },
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "mi(2)",
                                            "type": "dropdown_menu_item",
                                            "parent": "m",
                                            "attributes": [
                                                {
                                                    "id": "mi(2)",
                                                    "key": "label",
                                                    "value": "2",
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "mi(2)",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "operation": "add_assumption(p(2))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "mi(1)",
                                            "type": "dropdown_menu_item",
                                            "parent": "m",
                                            "attributes": [
                                                {
                                                    "id": "mi(1)",
                                                    "key": "label",
                                                    "value": "1",
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "mi(1)",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "operation": "add_assumption(p(1))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "c4",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "c4", "key": "width", "value": "146"},
                                        {"id": "c4", "key": "height", "value": "146"},
                                        {
                                            "id": "c4",
                                            "key": "background_color",
                                            "value": "beige",
                                        },
                                        {"id": "c4", "key": "pos_x", "value": "100"},
                                        {"id": "c4", "key": "pos_y", "value": "0"},
                                        {
                                            "id": "c4",
                                            "key": "child_layout",
                                            "value": "grid",
                                        },
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "c(3,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,3)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_row",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,3)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,2)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_row",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,2)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(3,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "grid_column",
                                                    "value": "3",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(3,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(2,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "background_color",
                                                    "value": "red",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "grid_column",
                                                    "value": "2",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(2,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                        {
                                            "id": "c(1,1)",
                                            "type": "container",
                                            "parent": "c4",
                                            "attributes": [
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "background_color",
                                                    "value": "pink",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_row",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "grid_column",
                                                    "value": "1",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "height",
                                                    "value": "48",
                                                },
                                                {
                                                    "id": "c(1,1)",
                                                    "key": "width",
                                                    "value": "48",
                                                },
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "cc",
                                    "type": "container",
                                    "parent": "c",
                                    "attributes": [
                                        {"id": "cc", "key": "width", "value": "100"},
                                        {"id": "cc", "key": "height", "value": "50"},
                                        {
                                            "id": "cc",
                                            "key": "background_color",
                                            "value": "green",
                                        },
                                        {
                                            "id": "cc",
                                            "key": "border_width",
                                            "value": "2",
                                        },
                                        {"id": "cc", "key": "pos_x", "value": "0"},
                                        {"id": "cc", "key": "pos_y", "value": "0"},
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "b",
                            "type": "button",
                            "parent": "w",
                            "attributes": [
                                {"id": "b", "key": "background_color", "value": "blue"},
                                {
                                    "id": "b",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "b", "key": "label", "value": '"Clear!"'},
                                {"id": "b", "key": "on_hover", "value": "true"},
                                {
                                    "id": "b",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "b",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "b", "key": "font_size", "value": "18"},
                                {"id": "b", "key": "font_weight", "value": '"bi"'},
                                {"id": "b", "key": "width", "value": "100"},
                                {"id": "b", "key": "height", "value": "50"},
                                {"id": "b", "key": "pos_x", "value": "40"},
                                {"id": "b", "key": "pos_y", "value": "70"},
                            ],
                            "when": [
                                {
                                    "id": "b",
                                    "event": "click",
                                    "interaction_type": "callback",
                                    "operation": "clear_assumptions",
                                }
                            ],
                            "children": [],
                        },
                        {
                            "id": "l1",
                            "type": "label",
                            "parent": "w",
                            "attributes": [
                                {
                                    "id": "l1",
                                    "key": "background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "l1",
                                    "key": "foreground_color",
                                    "value": "brown",
                                },
                                {"id": "l1", "key": "label", "value": '"Clear!"'},
                                {"id": "l1", "key": "on_hover", "value": "true"},
                                {
                                    "id": "l1",
                                    "key": "on_hover_background_color",
                                    "value": "gray",
                                },
                                {
                                    "id": "l1",
                                    "key": "on_hover_foreground_color",
                                    "value": "beige",
                                },
                                {"id": "l1", "key": "font_size", "value": "15"},
                                {"id": "l1", "key": "font_weight", "value": '"i"'},
                                {"id": "l1", "key": "width", "value": "100"},
                                {"id": "l1", "key": "height", "value": "50"},
                                {"id": "l1", "key": "pos_x", "value": "40"},
                                {"id": "l1", "key": "pos_y", "value": "50"},
                            ],
                            "when": [
                                {
                                    "id": "l1",
                                    "event": "click",
                                    "interaction_type": "callback",
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
