import json


class Coloring:
    """
    As graphviz is non-deterministic in nature we cannot be sure we produce the correct output here.
    """

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
                        {"id": "window", "key": "child_layout", "value": "grid"}
                    ],
                    "callbacks": [],
                    "children": [
                        {
                            "id": "node(6)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(6)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(6)", "key": "grid_row", "value": "6"},
                                {"id": "node(6)", "key": "height", "value": "30"},
                                {"id": "node(6)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(6)",
                                    "type": "dropdown_menu",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {
                                            "id": "dmc(6)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(6)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(6,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(6,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(6,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(6,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(6)",
                                    "type": "label",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {"id": "l(6)", "key": "label", "value": "6"},
                                        {
                                            "id": "l(6)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(5)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(5)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(5)", "key": "grid_row", "value": "5"},
                                {"id": "node(5)", "key": "height", "value": "30"},
                                {"id": "node(5)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(5)",
                                    "type": "dropdown_menu",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {
                                            "id": "dmc(5)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(5)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(5,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(5,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(5,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(5,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(5)",
                                    "type": "label",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {"id": "l(5)", "key": "label", "value": "5"},
                                        {
                                            "id": "l(5)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(4)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(4)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(4)", "key": "grid_row", "value": "4"},
                                {"id": "node(4)", "key": "height", "value": "30"},
                                {"id": "node(4)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(4)",
                                    "type": "dropdown_menu",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {
                                            "id": "dmc(4)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(4)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(4,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(4,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(4)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(4,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(4,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(4,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(4,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(4)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(4,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(4,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(4,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(4,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(4)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(4,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(4)",
                                    "type": "label",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {"id": "l(4)", "key": "label", "value": "4"},
                                        {
                                            "id": "l(4)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(3)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(3)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(3)", "key": "grid_row", "value": "3"},
                                {"id": "node(3)", "key": "height", "value": "30"},
                                {"id": "node(3)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(3)",
                                    "type": "dropdown_menu",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {
                                            "id": "dmc(3)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(3)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(3,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(3,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(3)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(3,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(3,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(3,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(3,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(3)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(3,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(3,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(3)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(3,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(3,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(3,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(3)",
                                    "type": "label",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {"id": "l(3)", "key": "label", "value": "3"},
                                        {
                                            "id": "l(3)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(2)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(2)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(2)", "key": "grid_row", "value": "2"},
                                {"id": "node(2)", "key": "height", "value": "30"},
                                {"id": "node(2)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(2)",
                                    "type": "dropdown_menu",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {
                                            "id": "dmc(2)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(2)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(2,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(2,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(2)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(2,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(2,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(2,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(2,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(2)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(2,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(2,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(2)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(2,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(2,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(2,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(2)",
                                    "type": "label",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {"id": "l(2)", "key": "label", "value": "2"},
                                        {
                                            "id": "l(2)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(1)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(1)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(1)", "key": "grid_row", "value": "1"},
                                {"id": "node(1)", "key": "height", "value": "30"},
                                {"id": "node(1)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(1)",
                                    "type": "dropdown_menu",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {
                                            "id": "dmc(1)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(1)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(1,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(1,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(1)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(1,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(1,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(1)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(1,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(1,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(1,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(1,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(1)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(1,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(1,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(1,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(1)",
                                    "type": "label",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {"id": "l(1)", "key": "label", "value": "1"},
                                        {
                                            "id": "l(1)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "canv",
                            "type": "canvas",
                            "parent": "window",
                            "attributes": [
                                {"id": "canv", "key": "width", "value": "250"},
                                {"id": "canv", "key": "height", "value": "250"},
                                {"id": "canv", "key": "resize", "value": "true"},
                                {
                                    "id": "canv",
                                    "key": "image",
                                    "value": '"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cQW+973v0U4nK3Ach1/+8peQyWS48cYbkUwmccMNN9BOizEF88Zg3/nOdwAATz31VM4/d00Fx3H4xS9+AZ1Ohy1btiCZTOKmm26inRZjEuaFwXbt2oWXX34Zf/3rX5GXl0c7HUH46U9/CqlUiq1btyIcDuO73/0u7ZQYE5DzBuvt7cX27dtxxx134LLLLqOdjqDce++9UKvV2L59O5LJJL7//e/TTolxGjltsFQqhZtuugmlpaW4//77aadDhTvvvBNSqRS33347QqEQ7rrrLtopMU4hpw320EMP4f3338eBAwcW9CLFH/7wh9DpdPjOd74Dnudxzz330E6J8W9y1mCffPIJ7rvvPvzsZz/DihUraKdDnVtvvRVSqRS33norRkdH8dBDD9FOiYEcNVgqlcK2bduwcuXKnJ4KlWluvvlmaDQafPOb30QqlcIjjzxCO6UFT04a7Je//CUOHTqEjz76SJCl/rnEddddB6lUis2bNyMUCuHXv/71vH5tIXZyzmB9fX3YsWMHfvKTn2DZsmW00xElmzZtglQqxXXXXYdkMoknnniCHZBOiZwz2LZt27Bo0SL8+Mc/pp2KqNm4cSM0Gg2uvvpqJJNJ7Ny5k5mMAjllsGeffRa7d+/Gvn37cnLHXqH5yle+gjfeeANf+9rXEA6H8dxzz0Emy6mvPOfJmVua2+3GD37wA9x22204//zzaaeTM6xfvx5///vf8b//+7+49tprkUgkaKe0oMgZg919991QKBT42c9+RjuVnOOiiy7C3/72N7z11lv42te+hlgsRjulBUNOGOzIkSPYuXMnHn74Yej1etrp5CQXXHAB3nrrLbz77ru46qqrMDo6SjulBUFOGOz222/HmjVrcP3119NOJac599xzsWfPHnz44YfYsGEDQqEQ7ZTmPaI32EsvvYT33nsP//3f/83e52SAM888E++88w4++eQTbNiwAcFgkHZK8xpRG2x0dBQ//vGP8c1vfhNr166lnc68YeXKlXj33XfR2dmJyy67DIFAgHZK8xZRG+zBBx/EyMjIgp0pn00aGxuxd+9e9Pb2Yt26dfB4PLRTmpeI1mB2ux2PPvoo7r77bhQXF9NOZ15SX1+P9957DyMjI7jkkkvgdrtppzTvEK3BHnjgAZjNZtx22220U5nXVFVVYe/evQgEArjwwgsxNDREO6V5hSgN1t/f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"',
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

    @classmethod
    def post_assumption_1(cls):
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
                        {"id": "window", "key": "child_layout", "value": "grid"}
                    ],
                    "callbacks": [],
                    "children": [
                        {
                            "id": "node(6)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(6)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(6)", "key": "grid_row", "value": "6"},
                                {"id": "node(6)", "key": "height", "value": "30"},
                                {"id": "node(6)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(6)",
                                    "type": "dropdown_menu",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {
                                            "id": "dmc(6)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(6)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(6,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(6,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(6,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(6,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(6)",
                                    "type": "label",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {"id": "l(6)", "key": "label", "value": "6"},
                                        {
                                            "id": "l(6)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(5)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(5)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(5)", "key": "grid_row", "value": "5"},
                                {"id": "node(5)", "key": "height", "value": "30"},
                                {"id": "node(5)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(5)",
                                    "type": "dropdown_menu",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {
                                            "id": "dmc(5)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(5)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(5,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(5,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(5,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(5,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(5)",
                                    "type": "label",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {"id": "l(5)", "key": "label", "value": "5"},
                                        {
                                            "id": "l(5)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(1)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(1)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(1)", "key": "grid_row", "value": "1"},
                                {"id": "node(1)", "key": "height", "value": "30"},
                                {"id": "node(1)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(1)",
                                    "type": "dropdown_menu",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {
                                            "id": "dmc(1)",
                                            "key": "selected",
                                            "value": "blue",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(1)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(1,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(1,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(1)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(1,blue))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(1)",
                                    "type": "label",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {"id": "l(1)", "key": "label", "value": "1"},
                                        {
                                            "id": "l(1)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(4)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(4)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(4)", "key": "grid_row", "value": "4"},
                                {"id": "node(4)", "key": "height", "value": "30"},
                                {"id": "node(4)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(4)",
                                    "type": "dropdown_menu",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {
                                            "id": "dmc(4)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(4)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(4,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(4,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(4)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(4,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(4,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(4,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(4,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(4)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(4,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(4)",
                                    "type": "label",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {"id": "l(4)", "key": "label", "value": "4"},
                                        {
                                            "id": "l(4)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(3)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(3)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(3)", "key": "grid_row", "value": "3"},
                                {"id": "node(3)", "key": "height", "value": "30"},
                                {"id": "node(3)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(3)",
                                    "type": "dropdown_menu",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {
                                            "id": "dmc(3)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(3)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(3,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(3,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(3)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(3,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(3,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(3)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(3,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(3,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(3,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(3)",
                                    "type": "label",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {"id": "l(3)", "key": "label", "value": "3"},
                                        {
                                            "id": "l(3)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(2)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(2)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(2)", "key": "grid_row", "value": "2"},
                                {"id": "node(2)", "key": "height", "value": "30"},
                                {"id": "node(2)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(2)",
                                    "type": "dropdown_menu",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {
                                            "id": "dmc(2)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(2)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(2,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(2,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(2)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(2,green))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(2,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(2)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(2,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(2,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(2,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(2)",
                                    "type": "label",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {"id": "l(2)", "key": "label", "value": "2"},
                                        {
                                            "id": "l(2)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "canv",
                            "type": "canvas",
                            "parent": "window",
                            "attributes": [
                                {"id": "canv", "key": "width", "value": "250"},
                                {"id": "canv", "key": "height", "value": "250"},
                                {"id": "canv", "key": "resize", "value": "true"},
                                {
                                    "id": "canv",
                                    "key": "image",
                                    "value": '"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oLq6GvX19ejq6kJLWwe6zGb0ulwIBgPwedwIhUJIVCVBJpNBlaSGRqNBTnYWsjIzkJ2djdLSUlRUVKC8vPyEj5P4/X6cddZZ8Hg8+OGHH6DRaEZrgbAhjLjlxx9/JCkpKeTss88mvb29nNR47733SKw/Ji0tLSQ1NZUsWLCARKPRmB5baLAbzXHK7t27cf7552PatGn48ssvkZSURFvSkMnNzcW7776Lzz77DM88M7afc2MBi0O2bduGOXPm4PTTT8fHH3+MxMRE2pKGzZw5c7BixQo89NBD2L59O205nMECFmds3boVF1xwAebOnYuPP/4YCQnCu5k8VO677z5ceOGFuPLKK/s3vRhrsIDFERs3bsQFF1yAefPm4Z133on72Q8ikQhvvPEGpFIpFi9ejGg0SltSzGEBixM+//xzLFiwAAsWLMDf/vY3SKVj42F0vV6P9957D5s3b8bTTz9NW07MYQGLAz788EMsWLAAixYtGlPh6uO0007DE088gUceeQT//Oc/acuJKSxgAue9997DVVddhRtuuAGrV6+GWDw2/2T33nsvLrzwQlxzzTVwOMbO1k1j8681Rli/fj0WLlyIe+65B6tWrYrLVZWGSt/1GADceGN8rd47GCxgAuW1117DokWL8Jvf/GZMXpsMhF6vx5o1a7BhwwasX7+etpzYQPtON+NYVq1aRcRiMXnggQdoS+FkJseJuPPOO4lWqyXNzc281uUCdgYTGM8++yxuu+02PPbYY1i5ciVtOVR46qmnkJubi0WLFiESidCWMypYwATEk08+iaVLl+K5557DI488QlsONRISErB27Vrs2LEDzz33HG05o4P2KZRxhJUrVxKRSET+9Kc/0ZbyX9AYIvbxxBNPEIVCQaqrq6nUjwUsYAJg2bJlRCwWkzVr1tCWcgw0AxaJRMjpp59Opk+fTiKRCBUNo4UNESlCCMG9996LFStW4PXXX8f1119PW5KgEIvFWL16Nfbs2YNVq1bRljMiWMAoQQjB3XffjZdeeglvvvlm3G0sxxeVlZW4//778cADD6CpqYm2nGHDAkYBQgjuuOMOrF69Gu+//z4WLlxIW5KgWbZsGfLy8nD77bfTljJsWMB4JhKJYMmSJVizZg0++OADXHrppbQlCR6FQoE1a9bgq6++irsb0CxgPBKJRHDdddfhgw8+wGeffYb58+fT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"',
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

    @classmethod
    def post_assumption_2(cls):
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
                        {"id": "window", "key": "child_layout", "value": "grid"}
                    ],
                    "callbacks": [],
                    "children": [
                        {
                            "id": "node(6)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(6)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(6)", "key": "grid_row", "value": "6"},
                                {"id": "node(6)", "key": "height", "value": "30"},
                                {"id": "node(6)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(6)",
                                    "type": "dropdown_menu",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {
                                            "id": "dmc(6)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(6)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(6,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(6,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(6,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(6)",
                                    "type": "label",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {"id": "l(6)", "key": "label", "value": "6"},
                                        {
                                            "id": "l(6)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(5)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(5)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(5)", "key": "grid_row", "value": "5"},
                                {"id": "node(5)", "key": "height", "value": "30"},
                                {"id": "node(5)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(5)",
                                    "type": "dropdown_menu",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {
                                            "id": "dmc(5)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(5)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(5,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(5,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,blue))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                        {
                                            "id": "dmi(5,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,red))",
                                                }
                                            ],
                                            "children": [],
                                        },
                                    ],
                                },
                                {
                                    "id": "l(5)",
                                    "type": "label",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {"id": "l(5)", "key": "label", "value": "5"},
                                        {
                                            "id": "l(5)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(1)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(1)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(1)", "key": "grid_row", "value": "1"},
                                {"id": "node(1)", "key": "height", "value": "30"},
                                {"id": "node(1)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(1)",
                                    "type": "dropdown_menu",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {
                                            "id": "dmc(1)",
                                            "key": "selected",
                                            "value": "blue",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(1)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(1,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(1,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(1)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(1,blue))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(1)",
                                    "type": "label",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {"id": "l(1)", "key": "label", "value": "1"},
                                        {
                                            "id": "l(1)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(3)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(3)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(3)", "key": "grid_row", "value": "3"},
                                {"id": "node(3)", "key": "height", "value": "30"},
                                {"id": "node(3)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(3)",
                                    "type": "dropdown_menu",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {
                                            "id": "dmc(3)",
                                            "key": "selected",
                                            "value": "green",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(3)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(3,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(3,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(3)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(3,green))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(3)",
                                    "type": "label",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {"id": "l(3)", "key": "label", "value": "3"},
                                        {
                                            "id": "l(3)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(2)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(2)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(2)", "key": "grid_row", "value": "2"},
                                {"id": "node(2)", "key": "height", "value": "30"},
                                {"id": "node(2)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(2)",
                                    "type": "dropdown_menu",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {
                                            "id": "dmc(2)",
                                            "key": "selected",
                                            "value": "green",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(2)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(2,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(2,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(2)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(2,green))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(2)",
                                    "type": "label",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {"id": "l(2)", "key": "label", "value": "2"},
                                        {
                                            "id": "l(2)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(4)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(4)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(4)", "key": "grid_row", "value": "4"},
                                {"id": "node(4)", "key": "height", "value": "30"},
                                {"id": "node(4)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(4)",
                                    "type": "dropdown_menu",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {
                                            "id": "dmc(4)",
                                            "key": "selected",
                                            "value": "red",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(4)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(4,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(4,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(4)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(4,red))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(4)",
                                    "type": "label",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {"id": "l(4)", "key": "label", "value": "4"},
                                        {
                                            "id": "l(4)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "canv",
                            "type": "canvas",
                            "parent": "window",
                            "attributes": [
                                {"id": "canv", "key": "width", "value": "250"},
                                {"id": "canv", "key": "height", "value": "250"},
                                {"id": "canv", "key": "resize", "value": "true"},
                                {
                                    "id": "canv",
                                    "key": "image",
                                    "value": '"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jY2orq1Ho8UCt8uFUCgIv9eDcDiMOI0WcrkcGq0O8fHxyMrMQEZaKjIzMzFgwAAUFxejqKjonNtJAoEAxo4dC6/Xi507dyI+Pr67KRA2RKTH8uOPP5LExEQyfvx44na7YxLj3XffJdH+mFRXV5OkpCQya9YswnFcVNsWGuJEcw9l7969uOSSSzBy5Eh88cUX0Gq1tCV1mOzsbLzzzjvYuHEjnnqqd+9zEw3WA9m+fTsmTpyICy64AB999BHi4uJoS+o0EydOxPLly3Hfffdhx44dtOXEDNFgPYxt27Zh6tSpmDJlCj766COoVMKbTO4of//73zFt2jRcddVVpy696G2IButBbNq0CVOnTsX06dPx9ttv9/jVDxKJBK+99hpkMhnmz58PjuNoS4o6osF6CJ999hlmzZqFWbNm4Y033oBM1js2oxuNRrz77rvYsmULnnzySdpyoo5osB7ABx98gFmzZmHevHm9ylxtnH/++XjsscewZMkSfP/997TlRBXRYALn3XffxdVXX42//OUvKCkpAcP0zrfszjvvxLRp03DttdfC4eg9Vzf1znerl7B+/XrMnTsXd9xxB1avXt0jT1XqKG3jMQC4/vqedXrv2RANJlBefvllzJs3D3fddVevHJu0h9FoxJo1a7BhwwasX7+etpzoQHumW+R0Vq9eTRiGIffccw9tKTFZyXEubr31VqLX60lVVRWvcWOB+AQTGCtXrsTNN9+MBx98ECtWrKAthwpPPPEEsrOzMW/ePLAsS1tOtxANJiAef/xxLF68GE8//TSWLFlCWw41VCoV1q5di127duHpp5+mLad70H6EirSyYsUKIpFIyL/+9S/aUn4FjS5iG4899hhRKpXk8OHDVOJHA9FgAmDp0qWEYRiyZs0a2lJOg6bBWJYlF1xwARk1ahRhWZaKhu4idhEpQgjBnXfeieXLl+PVV1/FddddR1uSoGAYBiUlJdi3bx9Wr15NW06XEA1GCUIIbr/9djz//PN4/fXXe9zFcnwxaNAg3H333bjnnntQWVlJW06nEQ1GAUII/va3v6GkpATvvfce5s6dS1uSoFm6dCn69OmDW265hbaUTiMajGdYlsXChQuxZs0avP/++7jiiitoSxI8SqUSa9aswZdfftnjJqBFg/EIy7L485//jPfffx8bN27EjBkzaEvqMYwePRo33XQT7rjj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"',
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

    @classmethod
    def post_assumption_3(cls):
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
                        {"id": "window", "key": "child_layout", "value": "grid"}
                    ],
                    "callbacks": [],
                    "children": [
                        {
                            "id": "node(5)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(5)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(5)", "key": "grid_row", "value": "5"},
                                {"id": "node(5)", "key": "height", "value": "30"},
                                {"id": "node(5)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(5)",
                                    "type": "dropdown_menu",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {
                                            "id": "dmc(5)",
                                            "key": "selected",
                                            "value": "blue",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(5)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(5)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(5,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(5,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(5)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(5,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(5,blue))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(5)",
                                    "type": "label",
                                    "parent": "node(5)",
                                    "attributes": [
                                        {"id": "l(5)", "key": "label", "value": "5"},
                                        {
                                            "id": "l(5)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(1)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(1)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(1)", "key": "grid_row", "value": "1"},
                                {"id": "node(1)", "key": "height", "value": "30"},
                                {"id": "node(1)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(1)",
                                    "type": "dropdown_menu",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {
                                            "id": "dmc(1)",
                                            "key": "selected",
                                            "value": "blue",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(1)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(1)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(1,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(1,blue)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(1)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "key": "label",
                                                    "value": "blue",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(1,blue)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(1,blue))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(1)",
                                    "type": "label",
                                    "parent": "node(1)",
                                    "attributes": [
                                        {"id": "l(1)", "key": "label", "value": "1"},
                                        {
                                            "id": "l(1)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(3)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(3)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(3)", "key": "grid_row", "value": "3"},
                                {"id": "node(3)", "key": "height", "value": "30"},
                                {"id": "node(3)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(3)",
                                    "type": "dropdown_menu",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {
                                            "id": "dmc(3)",
                                            "key": "selected",
                                            "value": "green",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(3)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(3)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(3,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(3,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(3)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(3,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(3,green))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(3)",
                                    "type": "label",
                                    "parent": "node(3)",
                                    "attributes": [
                                        {"id": "l(3)", "key": "label", "value": "3"},
                                        {
                                            "id": "l(3)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(2)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(2)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(2)", "key": "grid_row", "value": "2"},
                                {"id": "node(2)", "key": "height", "value": "30"},
                                {"id": "node(2)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(2)",
                                    "type": "dropdown_menu",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {
                                            "id": "dmc(2)",
                                            "key": "selected",
                                            "value": "green",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(2)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(2)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(2,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(2,green)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(2)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "key": "label",
                                                    "value": "green",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(2,green)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(2,green))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(2)",
                                    "type": "label",
                                    "parent": "node(2)",
                                    "attributes": [
                                        {"id": "l(2)", "key": "label", "value": "2"},
                                        {
                                            "id": "l(2)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(6)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(6)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(6)", "key": "grid_row", "value": "6"},
                                {"id": "node(6)", "key": "height", "value": "30"},
                                {"id": "node(6)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(6)",
                                    "type": "dropdown_menu",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {
                                            "id": "dmc(6)",
                                            "key": "selected",
                                            "value": "red",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(6)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(6)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(6,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(6,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(6)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(6,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(6,red))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(6)",
                                    "type": "label",
                                    "parent": "node(6)",
                                    "attributes": [
                                        {"id": "l(6)", "key": "label", "value": "6"},
                                        {
                                            "id": "l(6)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "node(4)",
                            "type": "container",
                            "parent": "window",
                            "attributes": [
                                {
                                    "id": "node(4)",
                                    "key": "child_layout",
                                    "value": "grid",
                                },
                                {"id": "node(4)", "key": "grid_row", "value": "4"},
                                {"id": "node(4)", "key": "height", "value": "30"},
                                {"id": "node(4)", "key": "width", "value": "200"},
                            ],
                            "callbacks": [],
                            "children": [
                                {
                                    "id": "dmc(4)",
                                    "type": "dropdown_menu",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {
                                            "id": "dmc(4)",
                                            "key": "selected",
                                            "value": "red",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "height",
                                            "value": "30",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "width",
                                            "value": "100",
                                        },
                                        {
                                            "id": "dmc(4)",
                                            "key": "grid_column",
                                            "value": "1",
                                        },
                                    ],
                                    "callbacks": [
                                        {
                                            "id": "dmc(4)",
                                            "action": "clear",
                                            "policy": "remove_assumption_signature(assign(4,any))",
                                        }
                                    ],
                                    "children": [
                                        {
                                            "id": "dmi(4,red)",
                                            "type": "dropdown_menu_item",
                                            "parent": "dmc(4)",
                                            "attributes": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "key": "label",
                                                    "value": "red",
                                                }
                                            ],
                                            "callbacks": [
                                                {
                                                    "id": "dmi(4,red)",
                                                    "action": "click",
                                                    "policy": "add_assumption(assign(4,red))",
                                                }
                                            ],
                                            "children": [],
                                        }
                                    ],
                                },
                                {
                                    "id": "l(4)",
                                    "type": "label",
                                    "parent": "node(4)",
                                    "attributes": [
                                        {"id": "l(4)", "key": "label", "value": "4"},
                                        {
                                            "id": "l(4)",
                                            "key": "grid_column",
                                            "value": "0",
                                        },
                                    ],
                                    "callbacks": [],
                                    "children": [],
                                },
                            ],
                        },
                        {
                            "id": "canv",
                            "type": "canvas",
                            "parent": "window",
                            "attributes": [
                                {"id": "canv", "key": "width", "value": "250"},
                                {"id": "canv", "key": "height", "value": "250"},
                                {"id": "canv", "key": "resize", "value": "true"},
                                {
                                    "id": "canv",
                                    "key": "image",
                                    "value": '"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lVdeKbekRsfs2bNRqVQ88cQTckupNSGDSUCNub7//nu++uorhgwZIrekRklkZCRz5szhjTfeYP/+/XLLqRUhgwUYm83G1VdfzaZNm/jhhx+a5AUHUnLTTTdxySWXcP/998stpVaEDBZAbDYbo0ePJiMjg++//54+ffrILanRo1AoWLhwIZs2beLTT4P/YviQwQKExWJh1KhRHDhwgI0bN9KrVy+5JTUZLr74YiZOnMj//d//YbPZ5JZzXkIGCwAVFRVceeWVHDp0iPXr19OtWze5JTU5nnvuOSorK4P+XMWQwfxMeXk5w4cPJy8vj59++okuXbrILalJkpCQwGOPPcZzzz1HUVGR3HLOSchgfqS4uJhBgwZRVFTEhg0baNeundySmjT3338/UVFRQb1vLmQwP1FUVMSQIUOoqqpiw4YNtGnTRm5JTR69Xs8jjzzCG2+8QW5urtxyzkrIYH6goKCAwYMH43a72bJlC2lpaXJL+ttwxx13kJSUxOzZs+WWclZCBmsg2dnZ9O/fHyEEP/74IykpKXJL+luh1Wp57LHHePvttzl16pTccv5CyGAN4PTp0wwaNIiIiAg2b95McnKy3JL+lkyZMoW0tDRmzZolt5S/EDJYPTl69Cj9+vUjOjqadevWERcXJ7ekvy1qtZoZM2awfPlyjh07Jrec/4+QwerB4cOHGTx4MMnJyfzwww/ExsbKLelvz4033kibNm2Cbl0sZLA6snfvXgYOHEibNm1Yv379Oe9DDiEtKpWK++67j+XLl1NcXCy3nN8JGawO7N69m6FDh9K5c2e+/vrrOt2HHCLw3HTTTRiNRt566y25pfxOyGC1pDFf2fp3ITw8nFtvvZXXX38dl8sltxwgZLBasWXLFoYMGdKor2z9u3DvvfdSUlLCJ598IrcUIGSwC1JzZeuwYcMa/ZWtfwdSUlIYO3YsL730ktxSgJDBzkvNla0jR45sEle2/l2477772LVrV1Bcrh4y2Dn445Wt77//fpO7VbIpc/nll3PxxRezePFiuaWEDHY21qxZwz//+c8me2Xr34EpU6awatUqqqurZdURMtif+Oijj7j22muZMmVKk76ytalzww034PV6ZU92hP56/sDf6crWpk5MTAyjR49m2bJlsuoIGew3/o5XtjZ1brzxRrZs2UJeXp5sGkIGA9544w3+/e9/M23atKDe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"',
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
