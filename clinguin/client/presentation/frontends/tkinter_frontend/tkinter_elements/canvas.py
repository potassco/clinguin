"""
Contains the canvas class.
"""

import base64
import io
import tkinter as tk

import PIL.Image as TImage
from PIL import ImageTk

from clinguin.utils.attribute_types import BooleanType, ImageType, PathType

from ..tkinter_utils import AttributeNames, ConfigureSize, LayoutFollower
from .root_cmp import RootCmp


class Canvas(RootCmp, LayoutFollower, ConfigureSize):
    """
    The canvas class resembles a element,
    which is generally regarded as an ''empty sheet of paper'',
    so there is an area, where one can display images, draw something or does something similar.
    One can look up what actual options are available through the syntax-definition.
    Implementation wise it is similarly implemented to the label, button and dropdownmenu.
    """

    def __init__(self, args, cid, parent, attributes, callbacks, base_engine):
        super().__init__(args, cid, parent, attributes, callbacks, base_engine)

        self._canvas = None
        self._image = None

    def _init_element(self, elements):
        canvas_frame = tk.Frame(elements[str(self._parent)].get_element())

        self._canvas = tk.Canvas(canvas_frame)

        return canvas_frame

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.image] = {"value": "", "value_type": ImageType}
        attributes[AttributeNames.image_path] = {"value": "", "value_type": PathType}
        attributes[AttributeNames.resize] = {"value": True, "value_type": BooleanType}
        return attributes

    def _set_image(self, elements):
        self._logger.debug(str(elements))

        image_base64 = self._attributes[AttributeNames.image]["value"]
        image_file = self._attributes[AttributeNames.image_path]["value"]

        if image_base64 != "" and image_file != "":
            self._logger.error(
                "One cannot set both attributes %s and %s for the same canvas with id %s",
                AttributeNames.image,
                AttributeNames.image_path,
                str(self._id),
            )

        elif image_base64 == "" and image_file != "":
            try:
                image_open = TImage.open(image_file)

                height = self._attributes[AttributeNames.height]["value"]
                width = self._attributes[AttributeNames.width]["value"]
                resize_flag = self._attributes[AttributeNames.resize]["value"]

                if height > 0 and width > 0 and resize_flag:
                    image_open = image_open.resize((width, height))

                tkinter_image = ImageTk.PhotoImage(image_open, master=self._canvas)

                self._canvas.create_image(0, 0, anchor=tk.NW, image=tkinter_image)

                # DO NOT DELETE THIS SEEMINGLY UNECESSARY LINE (this is due to a tkinter bug)
                self._image = tkinter_image
            except Exception as e:
                self._logger.error(e)
                self._logger.error(
                    "Could not render image (likely the provided file <%s>is not a valid image).",
                    image_file,
                )

        elif image_base64 != "" and image_file == "":
            try:
                image_initial_bytes = image_base64.encode("utf-8")
                image_decoded = base64.b64decode(image_initial_bytes)

                image_bytes = io.BytesIO(image_decoded)
                image_open = TImage.open(image_bytes)

                height = self._attributes[AttributeNames.height]["value"]
                width = self._attributes[AttributeNames.width]["value"]
                resize_flag = self._attributes[AttributeNames.resize]["value"]

                if height > 0 and width > 0 and resize_flag:
                    image_open = image_open.resize((width, height))

                tkinter_image = ImageTk.PhotoImage(image_open, master=self._canvas)

                self._canvas.create_image(0, 0, anchor=tk.NW, image=tkinter_image)

                # DO NOT DELETE THIS SEEMINGLY UNECESSARY LINE
                self._image = tkinter_image
            except Exception:
                self._logger.error(
                    "Could not render image (likely Base64 encoding is wrong)."
                )

    def _add_component_to_elements(self, elements):
        self._canvas.pack(expand=True, fill="both")

        elements[str(self._id)] = self
