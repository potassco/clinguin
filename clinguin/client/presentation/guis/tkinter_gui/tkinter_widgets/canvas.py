"""
Contains the canvas class.
"""
import io
import base64

import tkinter as tk
from tkinter import font

from PIL import ImageTk
import PIL.Image as TImage


from .root_cmp import *

class Canvas(RootCmp, LayoutFollower, ConfigureSize):
    """
    The canvas class resembles a widget, which is generally regarded as an ''empty sheet of paper'', so there is an area, where one can display images, draw something or does something similar. One can look up what actual options are available through the syntax-definition.
    """

    def _initWidget(self, elements):
        canvas_frame = tk.Frame(elements[str(self._parent)].getWidget())

        self._canvas = tk.Canvas(canvas_frame)

        return canvas_frame

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.image] = {"value":"", "value_type" : ImageType}
        attributes[AttributeNames.image_path] = {"value":"", "value_type" : PathType}
        attributes[AttributeNames.resize] = {"value": True, "value_type" : BooleanType}
        return attributes

    def _setImage(self, elements):

        image_base64 = self._attributes[AttributeNames.image]["value"]
        image_file = self._attributes[AttributeNames.image_path]["value"]

        if image_base64 != "" and image_file != "":
            self._logger.error("One cannot set both attributes " + AttributeNames.image + " and " + AttributeNames.image_path + " for the same canvas with id " + str(self._id))

        elif image_base64 == "" and image_file != "":
            try:
                
                image_open = Image.open(image_file)

                height = self._attributes[AttributeNames.height]["value"]
                width = self._attributes[AttributeNames.width]["value"]
                resize_flag = self._attributes[AttributeNames.resize]["value"]
                
                should_resize = resize_flag and height > 0 and width > 0
                
                if should_resize:
                    image_open = image_open.resize((width, height))

                tkinter_image = ImageTk.PhotoImage(image_open, master=self._canvas)

                self._canvas.create_image(0,0,anchor=tk.NW, image=tkinter_image)

                # DO NOT DELETE THIS SEEMINGLY UNECESSARY LINE (this is due to a tkinter bug)
                self._image = tkinter_image
            except Exception as e:
                self._logger.error(e)
                self._logger.error("Could not render image (likely the provided file " + image_file + " is not a valid image).")

        elif image_base64 != "" and image_file == "":
            try:
                image_initial_bytes = image_base64.encode('utf-8')
                image_decoded = base64.b64decode(image_initial_bytes)

                image_bytes = io.BytesIO(image_decoded)
                image_open = TImage.open(image_bytes)

                image_open = image_open.resize((self._attributes[AttributeNames.width]["value"], self._attributes[AttributeNames.width]["value"]))
                tkinter_image = ImageTk.PhotoImage(image_open, master=self._canvas)


                self._canvas.create_image(0,0,anchor=tk.NW, image=tkinter_image)

                # DO NOT DELETE THIS SEEMINGLY UNECESSARY LINE
                self._image = tkinter_image
            except Exception:
                self._logger.error("Could not render image (likely Base64 encoding is wrong).")
            

    def _addComponentToElements(self, elements):
        self._canvas.pack(expand=True, fill='both')

        elements[str(self._id)] = self

