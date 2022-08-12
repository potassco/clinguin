import io
import base64

import tkinter as tk
from tkinter import font

from PIL import ImageTk
import PIL.Image as TImage

from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render

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
        attributes[AttributeNames.height] = {"value":50, "value_type" : IntegerType}
        attributes[AttributeNames.width] = {"value":50, "value_type" : IntegerType}

        return attributes

    def _setSize(self, elements):
        self._widget.configure(height = self._attributes[AttributeNames.height]["value"])
        self._widget.configure(width = self._attributes[AttributeNames.width]["value"])

    def _setValues(self, elements):

        image_b64 = self._attributes[AttributeNames.image]["value"]

        if image_b64 != "": 
            try:
                image_initial_bytes = image_b64.encode('utf-8')
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

