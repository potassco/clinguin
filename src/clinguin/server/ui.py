class UIState:
    """
    The UIState is the low-level-access-class for handling the facts defining the UI state
    """

    unifiers = []

    def __init__(self, ui_files, domain_state, constants_arg_list):
        self._factbase = None
        self._ui_files = ui_files
        self._domain_state = domain_state
        self._constants_arg_list = constants_arg_list

    def __str__(self):
        return ""

    @property
    def is_empty(self):
        return self._factbase is None

    def _set_fb_symbols(self, symbols):
        pass

    def ui_control(self):
        pass

    def update_ui_state(self):
        pass

    def add_message(self, title, message, attribute_type="info"):
        pass

    def add_element(self, cid, t, parent):
        pass

    def add_attribute(self, cid, key, value):
        pass

    def add_attribute_direct(self, new_attribute):
        pass

    def get_elements(self):
        pass

    def get_attributes(self, key=None):
        pass

    def get_callbacks(self):
        pass

    def get_attributes_grouped(self):
        pass

    def get_callbacks_grouped(self):
        pass

    def get_attributes_for_element_id(self, element_id):
        pass

    def get_callbacks_for_element_id(self, element_id):
        pass

    def replace_attribute(self, old_attribute, new_attribute):
        pass

    @classmethod
    def symbols_to_facts(cls, symbols):
        pass

    def replace_images_with_b64(self, image_attribute_key="image"):
        pass
