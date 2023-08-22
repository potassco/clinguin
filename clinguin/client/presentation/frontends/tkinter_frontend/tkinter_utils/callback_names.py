"""
This module contains the CallbackNames class.
"""


class CallbackNames:
    """
    This class contains all possible names for actions for callbacks and their descriptions.
    """

    click = "click"
    clear = "clear"

    descriptions = {
        click: "The click action, is the action that is executed if one clicks with the left-mouse button on a element.",
        clear: "The clearlick action, is the action that is executed when the empty option of a dropdown menu is selected.",
    }
