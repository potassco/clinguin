import json

class Health:

    @classmethod
    def get_reference_json(cls):
        return json.loads('{"name":"clinguin","version":"0.0.1b0","description":"An interactive visualizer for clingo"}')
                         