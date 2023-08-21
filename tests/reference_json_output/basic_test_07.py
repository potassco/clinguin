import json


class BasicTest07:

    @classmethod
    def get_reference_json(cls):

        json_dict ={"id":"root","type":"root","parent":"root","attributes":[],"callbacks":[],"children":[{"id":"window","type":"window","parent":"root","attributes":[{"id":"window","key":"height","value":"500"},{"id":"window","key":"width","value":"450"},{"id":"window","key":"pos_x","value":"0"},{"id":"window","key":"pos_y","value":"100"}],"callbacks":[],"children":[{"id":"canv","type":"canvas","parent":"window","attributes":[{"id":"canv","key":"height","value":"500"},{"id":"canv","key":"width","value":"450"},{"id":"canv","key":"image_path","value":"\"./examples/basic/test_07/tommi.jpg\""},{"id":"canv","key":"resize","value":"true"}],"callbacks":[],"children":[]}]}]}

        return json.loads(json.dumps(json_dict))
    
