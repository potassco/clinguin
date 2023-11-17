import json


class Health:
    @classmethod
    def get_reference_json(cls):
        json_dict = {
            "name": "clinguin",
            "version": "0.0.2",
            "description": "An interactive visualizer for clingo",
        }

        return json.loads(json.dumps(json_dict))
