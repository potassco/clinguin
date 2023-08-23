"""
Module that contains the AttributeNames class.
"""


class AttributeNames:  # pylint: disable=R0903
    """
    This class contains all the names for all the attributes that are used for the Frontend
    and also contains some standard descriptions of the attributes.
    """

    title = "title"
    message = "message"
    type = "type"

    label = "label"
    backgroundcolor = "background_color"
    foregroundcolor = "foreground_color"
    width = "width"
    height = "height"

    onhover = "on_hover"
    onhover_background_color = "on_hover_background_color"
    onhover_foreground_color = "on_hover_foreground_color"
    onhover_border_color = "on_hover_border_color"

    font_family = "font_family"
    font_size = "font_size"
    font_weight = "font_weight"

    resizable_x = "resizable_x"
    resizable_y = "resizable_y"

    child_layout = "child_layout"

    grid_column = "grid_column"
    grid_row = "grid_row"
    grid_column_span = "grid_column_span"
    grid_row_span = "grid_row_span"
    pos_x = "pos_x"
    pos_y = "pos_y"

    border_width = "border_width"
    border_color = "border_color"

    selected = "selected"
    fit_children_size = "fit"

    image = "image"
    image_path = "image_path"
    resize = "resize"

    flex_direction = "flex_direction"

    accelerator = "accelerator"
    descriptions = {
        title: "With this attribute one can set the title of a pop-up.",
        message: "With this attribute one can set the message of a pop-up.",
        type: "With this attribute one can set the look and feel of the pop-up.",
        label: "With this attribute one can set the label-text of the element.",
        backgroundcolor: "With this attribute one can define the background-color of the element.",
        foregroundcolor: "With this attribute one can set the foreground-color of the element.",
        width: "With this attribute one can set the width in pixels of the element.",
        height: "With this attribute one can set the height in pixels of the element.",
        onhover: "With this attribute one can enable or disable on-hover features for the element.",
        onhover_background_color: "With this attribute one can set the background color the element shall have, when"
        + "on_hover is enabled.",
        onhover_foreground_color: "With this attribute one can set the forground color the element shall have,"
        + "when on_hover is eneabled.",
        onhover_border_color: "With this attribute one can set the color the border of the element shall have,"
        + "when on_hover is enabled.",
        font_family: "With this attribute one can set the font-family of the element.",
        font_size: "With this attribute one can set the font size in pixels.",
        font_weight: "With this attribute one can set the font weight.",
        resizable_x: "With this attribute one can define if the element shall be resizable in x direction.",
        resizable_y: "With this attribute one can define if the element shall be resizable in y direction.",
        child_layout: "With this attribute one can define the layout of the children, i.e. how they are positioned.",
        grid_column: "With this attribute one can define in which column the element shall be positioned.",
        grid_row: "With this attribute one can define in which row the element shall be positioned.",
        grid_column_span: "With this attribute one can define, that the elements stretches over several columns.",
        grid_row_span: "With this attribute one can define, that the elements stretches over several rows.",
        pos_x: "With this attribute one sets the x-position of the element - it depends on the parent-child-layout"
        + "how this is defined (either pixels, relative as a percentage, ...).",
        pos_y: "With this attribute one sets the y-position of the element - it depends on the parent-child-layout"
        + "how this is defined (either pixels, relative as a percentage, ...).",
        border_width: "With this attribute one defines the width of the border in pixels.",
        border_color: "With this attribute one may set the border color.",
        selected: "With this attribute one may define the text that shall be displayed if something is selected.",
        fit_children_size: "[DEPRECATED] - With this attribute one can define that the element fits the children.",
        image: "Some backends define special values one can use, that e.g. a graph is shown (see corresponding"
        + "backend description).",
        image_path: "Include an image from a path.",
        resize: "With this attribute one can define if an image shall be resized.",
        accelerator: "The key binding for the menu option",
        flex_direction: "With this attribute one can set the ''direction'' (i.e., where it gets placed) of an"
        + "element which root has a specified flex layout.",
    }
