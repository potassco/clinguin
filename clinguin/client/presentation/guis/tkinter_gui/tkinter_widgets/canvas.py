from tkinter import font
import tkinter as tk

from .root_cmp import *

import io
from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render
import base64
from PIL import ImageTk
import PIL.Image as TImage

import tkinter as tk


class Canvas(RootCmp):


    def _initWidget(self, elements):
        canvas = tk.Canvas(elements[str(self._parent)].getWidget())
        canvas.pack()
        return canvas

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}

        attributes[AttributeNames.image] = {"value":"", "value_type" : StringType}

        return attributes

    def _setValues(self, elements):

        image_b64 = self._attributes[AttributeNames.image]["value"]

        if image_b64 != "": 
            image_bytes = image_b64.encode('utf-8')

            bImg = TImage.open(io.BytesIO(base64.b64decode(image_bytes)))

            im2 = ImageTk.PhotoImage(bImg, master=self._widget)
            self._widget.create_image(10,10,anchor=tk.NW, image=im2)
            self._image = im2

       
            """
            fb = Factbase()
            fb.add_fact_string('''
            node(oscar).
            node(andres).
            edge((oscar,andres)).
            attr(node,andres,label,"Andres").
            attr(node,oscar,label,"Oscar").
            attr(edge,(oscar,andres),label,"friends").''')

            graphs = compute_graphs(fb)

            mygraph = graphs['default']
            mygraph.format = 'png'
            img = (graphs['default'].pipe())

            im = tk.PhotoImage(data=output)
            tk.Label(elements[str(self._parent)].getWidget(), image=im).pack()
 
            output = base64.b64encode(img)


            """
            """
            image_opened = TImage.open(io.BytesIO(base64.b64decode(output)))
            
            image_photo = ImageTk.PhotoImage(image_opened)
            self._widget.create_image(master=canvas, 10,10,anchor=tk.NW, image=image_photo)
            self._widget.pack()
            """
            #im = tk.PhotoImage(data=output)
            #tk.Label(root, image=im).pack()


            """
            print(len(image_b64))
            encoded2 = image_b64.encode('utf-8')
            image_decoded = base64.b64decode(encoded2)
            image_bytes = io.BytesIO(image_decoded)
            """
   



