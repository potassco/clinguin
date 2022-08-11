from .clinguin_model import *

from clorm import Predicate, RawField

from clingraph.graphviz import compute_graphs
from clingraph.orm import Factbase

import base64
#DEL:
from clingraph.graphviz import compute_graphs, render
import io
from PIL import ImageTk
import PIL.Image as TImage

import tkinter as tk

class GraphDao(Predicate):
    id = RawField

    class Meta:
        name = "graph"

class NodeDao(Predicate):
    name = RawField

    class Meta:
        name = "node"

class EdgeDao(Predicate):
    graph = RawField

    class Meta:
        name = "edge"

class AttrDao(Predicate):
    element_type = RawField
    element_id = RawField
    attr_id = RawField
    attr_value = RawField

    class Meta:
        name = "attr"

class ClingraphModel(ClinguinModel):

    def __init__(self, logger, factbase=None):
        super().__init__(logger, factbase)

        self.unifiers = [ElementDao, AttributeDao, CallbackDao, NodeDao, EdgeDao, AttrDao, GraphDao]


    def parseClingraph(self):
        nodes = [e for e in self._factbase.query(NodeDao).all()]
        edges = [e for e in self._factbase.query(EdgeDao).all()]
        graphs = [e for e in self._factbase.query(GraphDao).all()]
        attrs = [e for e in self._factbase.query(AttrDao).all()]

        string = ""
        for node in nodes:
            string = string + str(node) + ".\n"
        for node in edges:
            string = string + str(node) + ".\n"
        for node in graphs:
            string = string + str(node) + ".\n"
        for node in attrs:
            string = string + str(node) + ".\n"

        #print(string)

        # Why isn't this working?
        """
        clorm_fb = clorm.FactBase(nodes+edges+graphs+attrs)
        clingraph_fb = Factbase()
        clingraph_fb.add_fb(clorm_fb)
        """
        clingraph_fb = Factbase()
        clingraph_fb.add_fact_string(string)
       
        graphs = compute_graphs(clingraph_fb)

        return graphs

    def fillImagePlaceholders(self, graphs, position):

        graph = graphs[list(graphs.keys())[0]]
        graph.format = 'png'
        img = graph.pipe()

        encoded = base64.b64encode(img)
        decoded = encoded.decode('utf-8')
        #print(decoded)
        encoded2 = decoded.encode('utf-8')
        decoded2 = base64.b64decode(encoded2)
        
        kept_symbols = list(self.getElements()) + list(self.getCallbacks())
        #print(len(decoded))

        for attribute in self.getAttributes():
            if str(attribute.key) == "image" and str(attribute.value) == "clingraph":
                kept_symbols.append(AttributeDao(Raw(Function(str(attribute.id),[])), Raw(Function(str(attribute.key),[])), Raw(String(str(decoded)))))
            else:
                kept_symbols.append(attribute)

        self._factbase = clorm.FactBase(kept_symbols)


    
        








