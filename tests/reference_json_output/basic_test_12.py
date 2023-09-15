import json

class BasicTest12:
    @classmethod
    def get_reference_json(cls):
        json_dict = {"id":"root","type":"root","parent":"root","attributes":[],"do":[],"children":[{"id":"w","type":"window","parent":"root","attributes":[{"id":"w","key":"child_layout","value":"absstatic"}],"do":[],"children":[{"id":"c1","type":"container","parent":"w","attributes":[{"id":"c1","key":"pos_x","value":"0"},{"id":"c1","key":"pos_y","value":"0"},{"id":"c1","key":"height","value":"200"},{"id":"c1","key":"width","value":"500"},{"id":"c1","key":"child_layout","value":"flex"},{"id":"c1","key":"flex_direction","value":"row_reverse"}],"do":[],"children":[{"id":"b1","type":"button","parent":"c1","attributes":[{"id":"b1","key":"label","value":"\"Add Name\""}],"do":[{"id":"b1","action_type":"click","interaction_type":"callback","policy":"add_atom(name(_value_context(t1_content)))"}],"children":[]},{"id":"t1","type":"textfield","parent":"c1","attributes":[{"id":"t1","key":"placeholder","value":"\"Type Name Here\""}],"do":[{"id":"t1","action_type":"type","interaction_type":"context","policy":"(t1_content,_value)"}],"children":[]}]},{"id":"c2","type":"container","parent":"w","attributes":[{"id":"c2","key":"pos_x","value":"0"},{"id":"c2","key":"pos_y","value":"250"},{"id":"c2","key":"height","value":"200"},{"id":"c2","key":"width","value":"500"},{"id":"c2","key":"child_layout","value":"flex"},{"id":"c2","key":"flex_direction","value":"column"}],"do":[],"children":[]}]}]}
        
        return json.loads(json.dumps(json_dict))
