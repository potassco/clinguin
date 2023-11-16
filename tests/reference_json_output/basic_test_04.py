import json


class BasicTest04:
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
                            "id": "m",
                            "type": "menu_bar",
                            "parent": "w",
                            "attributes": [],
                            "when": [],
                            "children": [
                                {
                                    "id": "ms2",
                                    "type": "menu_bar_section",
                                    "parent": "m",
                                    "attributes": [],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "ms2i2",
                                            "type": "menu_bar_section_item",
                                            "parent": "ms2",
                                            "attributes": [],
                                            "when": [],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "ms1",
                                    "type": "menu_bar_section",
                                    "parent": "m",
                                    "attributes": [
                                        {
                                            "id": "ms1",
                                            "key": "label",
                                            "value": '"Test2"',
                                        }
                                    ],
                                    "when": [],
                                    "children": [
                                        {
                                            "id": "ms1i2",
                                            "type": "menu_bar_section_item",
                                            "parent": "ms1",
                                            "attributes": [
                                                {
                                                    "id": "ms1i2",
                                                    "key": "label",
                                                    "value": '"Item Y"',
                                                }
                                            ],
                                            "when": [
                                                {
                                                    "id": "ms1i2",
                                                    "event": "click",
                                                    "interaction_type": "callback",
                                                    "policy": "clear_assumptions",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "ms1i1",
                                            "type": "menu_bar_section_item",
                                            "parent": "ms1",
                                            "attributes": [
                                                {
                                                    "id": "ms1i1",
                                                    "key": "label",
                                                    "value": '"Item X"',
                                                }
                                            ],
                                            "when": [],
                                            "children": [],
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "id": "c2",
                            "type": "container",
                            "parent": "w",
                            "attributes": [
                                {"id": "c2", "key": "width", "value": "180"},
                                {"id": "c2", "key": "height", "value": "180"},
                                {"id": "c2", "key": "border_width", "value": "2"},
                                {"id": "c2", "key": "on_hover", "value": "true"},
                                {
                                    "id": "c2",
                                    "key": "on_hover_background_color",
                                    "value": "blue",
                                },
                                {
                                    "id": "c2",
                                    "key": "on_hover_border_color",
                                    "value": "red",
                                },
                                {"id": "c2", "key": "pos_x", "value": "25"},
                                {"id": "c2", "key": "pos_y", "value": "50"},
                                {"id": "c2", "key": "child_layout", "value": "grid"},
                            ],
                            "when": [],
                            "children": [
                                {
                                    "id": "c24",
                                    "type": "container",
                                    "parent": "c2",
                                    "attributes": [
                                        {"id": "c24", "key": "width", "value": "60"},
                                        {"id": "c24", "key": "height", "value": "60"},
                                        {
                                            "id": "c24",
                                            "key": "background_color",
                                            "value": '"#000000"',
                                        },
                                        {
                                            "id": "c24",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                        {"id": "c24", "key": "grid_row", "value": "1"},
                                        {
                                            "id": "c24",
                                            "key": "grid_column_span",
                                            "value": "1",
                                        },
                                        {
                                            "id": "c24",
                                            "key": "grid_row_span",
                                            "value": "1",
                                        },
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                                {
                                    "id": "c23",
                                    "type": "container",
                                    "parent": "c2",
                                    "attributes": [
                                        {"id": "c23", "key": "width", "value": "120"},
                                        {"id": "c23", "key": "height", "value": "60"},
                                        {
                                            "id": "c23",
                                            "key": "background_color",
                                            "value": '"#999999"',
                                        },
                                        {
                                            "id": "c23",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                        {"id": "c23", "key": "grid_row", "value": "2"},
                                        {
                                            "id": "c23",
                                            "key": "grid_column_span",
                                            "value": "2",
                                        },
                                        {
                                            "id": "c23",
                                            "key": "grid_row_span",
                                            "value": "1",
                                        },
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                                {
                                    "id": "c22",
                                    "type": "container",
                                    "parent": "c2",
                                    "attributes": [
                                        {"id": "c22", "key": "width", "value": "60"},
                                        {"id": "c22", "key": "height", "value": "120"},
                                        {
                                            "id": "c22",
                                            "key": "background_color",
                                            "value": '"#0000ff"',
                                        },
                                        {
                                            "id": "c22",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                        {"id": "c22", "key": "grid_row", "value": "1"},
                                        {
                                            "id": "c22",
                                            "key": "grid_column_span",
                                            "value": "1",
                                        },
                                        {
                                            "id": "c22",
                                            "key": "grid_row_span",
                                            "value": "2",
                                        },
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                                {
                                    "id": "c21",
                                    "type": "container",
                                    "parent": "c2",
                                    "attributes": [
                                        {"id": "c21", "key": "width", "value": "60"},
                                        {"id": "c21", "key": "height", "value": "120"},
                                        {
                                            "id": "c21",
                                            "key": "background_color",
                                            "value": '"#00ff00"',
                                        },
                                        {
                                            "id": "c21",
                                            "key": "grid_column",
                                            "value": "2",
                                        },
                                        {"id": "c21", "key": "grid_row", "value": "0"},
                                        {
                                            "id": "c21",
                                            "key": "grid_column_span",
                                            "value": "1",
                                        },
                                        {
                                            "id": "c21",
                                            "key": "grid_row_span",
                                            "value": "2",
                                        },
                                    ],
                                    "when": [],
                                    "children": [],
                                },
                                {
                                    "id": "c20",
                                    "type": "container",
                                    "parent": "c2",
                                    "attributes": [
                                        {"id": "c20", "key": "width", "value": "120"},
                                        {"id": "c20", "key": "height", "value": "60"},
                                        {
                                            "id": "c20",
                                            "key": "background_color",
                                            "value": '"#ff0000"',
                                        },
                                        {
                                            "id": "c20",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                        {"id": "c20", "key": "grid_row", "value": "0"},
                                        {
                                            "id": "c20",
                                            "key": "grid_column_span",
                                            "value": "2",
                                        },
                                        {
                                            "id": "c20",
                                            "key": "grid_row_span",
                                            "value": "1",
                                        },
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
                                {"id": "b", "key": "font_size", "value": "15"},
                                {"id": "b", "key": "pos_x", "value": "25"},
                                {"id": "b", "key": "pos_y", "value": "0"},
                            ],
                            "when": [
                                {
                                    "id": "b",
                                    "event": "click",
                                    "interaction_type": "callback",
                                    "policy": "clear_assumptions",
                                }
                            ],
                            "children": [],
                        },
                    ],
                }
            ],
        }

        return json.loads(json.dumps(json_dict))
