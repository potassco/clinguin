import io
import base64

import tkinter as tk
from tkinter import font

from PIL import ImageTk, Image
import PIL.Image as TImage


from .root_cmp import *

class Canvas(RootCmp):


    def _initWidget(self, elements):
        canvas = tk.Canvas(elements[str(self._parent)].getWidget())
        return canvas

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}

        attributes[AttributeNames.image] = {"value":"", "value_type" : ImageType}
        attributes[AttributeNames.image_path] = {"value":"", "value_type" : PathType}
        attributes[AttributeNames.height] = {"value":50, "value_type" : IntegerType}
        attributes[AttributeNames.width] = {"value":50, "value_type" : IntegerType}
        attributes[AttributeNames.resize] = {"value": True, "value_type" : BooleanType}
        return attributes

    def _setSize(self, elements):
        self._widget.configure(height = self._attributes[AttributeNames.height]["value"])
        self._widget.configure(width = self._attributes[AttributeNames.width]["value"])

    def _setImage(self, elements):

        image_base64 = self._attributes[AttributeNames.image]["value"]
        image_file = self._attributes[AttributeNames.image_path]["value"]

        if image_base64 != "" and image_file != "":
            self._logger.error("One cannot set both attributes " + AttributeNames.image + " and " + AttributeNames.image_path + " for the same type with id " + str(self._id))

        elif image_base64 == "" and image_file != "":
            try:
                
                image_open = Image.open(image_file)
                if self._attributes[AttributeNames.resize]["value"]:
                    image_open = image_open.resize(
                        (self._attributes[AttributeNames.height]["value"], 
                        self._attributes[AttributeNames.width]["value"]))
                tkinter_image = ImageTk.PhotoImage(image_open, master=self._widget)

                self._widget.create_image(0,0,anchor=tk.NW, image=tkinter_image)

                # DO NOT DELETE THIS SEEMINGLY UNECESSARY LINE
                self._image = tkinter_image
            except Exception as e:
                self._logger.error(e)
                self._logger.debug("Could not render image (likely the provided file " + image_file + " is not a valid image).")

        elif image_base64 != "" and image_file == "":
            try:
                image_initial_bytes = image_base64.encode('utf-8')
                image_decoded = base64.b64decode(image_initial_bytes)

                image_bytes = io.BytesIO(image_decoded)
                image_open = TImage.open(image_bytes)

                image_open = image_open.resize((self._attributes[AttributeNames.width]["value"], self._attributes[AttributeNames.width]["value"]))
                tkinter_image = ImageTk.PhotoImage(image_open, master=self._widget)


                self._widget.create_image(0,0,anchor=tk.NW, image=tkinter_image)

                # DO NOT DELETE THIS SEEMINGLY UNECESSARY LINE
                self._image = tkinter_image
            except:
                self._logger.debug("Could not render image (likely Base64 encoding is wrong).")
            

    def _addComponentToElements(self, elements):
        self._widget.pack()
        elements[str(self._id)] = self

