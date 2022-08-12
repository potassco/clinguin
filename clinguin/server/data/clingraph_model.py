import copy

from .clinguin_model import *

from clorm import Predicate, RawField

from clingraph.graphviz import compute_graphs
from clingraph.orm import Factbase

import base64
#DEL:
from clingraph.graphviz import compute_graphs, render
from clinguin.utils import StandardTextProcessing

class GraphDao(Predicate):
    id = RawField

    class Meta:
        name = "graph"

class SubGraphDao(Predicate):
    id = RawField
    graph = RawField

    class Meta:
        name = "graph"


class NodeDao(Predicate):
    id = RawField
    graph = RawField

    class Meta:
        name = "node"

class NodeSugarDao(Predicate):
    id = RawField

    class Meta:
        name = "node"


class EdgeDao(Predicate):
    id = RawField

    class Meta:
        name = "edge"

class EdgeSugarDao(Predicate):
    id = RawField
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

    _intermediate_format = 'png'
    _encoding = 'utf-8'
    _attribute_image_key = 'image'
    _attribute_image_value = 'clingraph'

    def __init__(self, logger, factbase=None):
        super().__init__(logger, factbase)

        self.unifiers = Predicate.__subclasses__()


    def solveGraphs(self):
        symbols = []
        symbols.extend([e for e in self._factbase.query(NodeDao).all()])
        symbols.extend([e for e in self._factbase.query(NodeSugarDao).all()])
        symbols.extend([e for e in self._factbase.query(EdgeDao).all()])
        symbols.extend([e for e in self._factbase.query(EdgeSugarDao).all()])
        symbols.extend([e for e in self._factbase.query(GraphDao).all()])
        symbols.extend([e for e in self._factbase.query(SubGraphDao).all()])
        symbols.extend([e for e in self._factbase.query(AttrDao).all()])

        string = ""
        for symbol in symbols:
            string = string + str(symbol) + ".\n"

        # Why isn't this working?
        """
        clorm_fb = clorm.FactBase(nodes+edges+graphs+attrs) #... plus other symbols...
        clingraph_fb = Factbase()
        clingraph_fb.add_fb(clorm_fb)
        """

        clingraph_fb = Factbase()
        clingraph_fb.add_fact_string(string)
       
        graphs = compute_graphs(clingraph_fb)

        return graphs

    @classmethod
    def _createImageFromGraph(cls, graphs, position = None, key = None):
        if position != None: 
            if (len(graphs)-1) >= position:
                graph = graphs[list(graphs.keys())[position]]
            else:
                self._logger.error("Attempted to access not valid position")
                raise Exception("Attempted to access not valid position")
        elif key != None:
            if key in graphs:
                graph = graphs[key]
            else:
                self._logger.error("Key not found in graphs: " + str(key))
                raise Exception("Key not found in graphs: " + str(key))
        else:
            self._logger.error("Must either specify position or key!")
            raise Exception("Must either specify position or key!")

        graph.format = cls._intermediate_format
        img = graph.pipe()

        encoded = base64.b64encode(img)
        decoded = encoded.decode(cls._encoding)

        return decoded

    @classmethod
    def fillClingraphNamedPlaceholders(cls, logger, model, graphs):
        kept_symbols = list(model.getElements()) + list(model.getCallbacks())

        filled_attributes = []
        for attribute in model.getAttributes():
            if str(attribute.key) == cls._attribute_image_key:
                attribute_value = StandardTextProcessing.parseStringWithQuotes(str(attribute.value))

                if attribute_value.startswith(cls._attribute_image_value) and attribute_value != "clingraph":
                    splits = attribute_value.split("_")
                    splits.pop(0)
                    rest = ""   
                    for split in splits:
                        rest = rest + split

                    base64_key_image = cls._createImageFromGraph(graphs, key = rest)
                    filled_attributes.append(AttributeDao(Raw(Function(str(attribute.id),[])), Raw(Function(str(attribute.key),[])), Raw(String(str(base64_key_image)))))
                else:
                    filled_attributes.append(attribute)
            else:
                filled_attributes.append(attribute)

        return cls(logger, clorm.FactBase(copy.deepcopy(kept_symbols + filled_attributes)))

    @classmethod
    def fillClingraphDefaultPlaceholders(cls, logger, model, graphs, position):
        base64_position_image = cls._createImageFromGraph(graphs, position)

        kept_symbols = list(model.getElements()) + list(model.getCallbacks())

        filled_attributes = []
        for attribute in model.getAttributes():
            if str(attribute.key) == cls._attribute_image_key:
                attribute_value = StandardTextProcessing.parseStringWithQuotes(str(attribute.value))
                if attribute_value == cls._attribute_image_value:
                    filled_attributes.append(AttributeDao(Raw(Function(str(attribute.id),[])), Raw(Function(str(attribute.key),[])), Raw(String(str(base64_position_image)))))
                else:
                    filled_attributes.append(attribute)
            else:
                filled_attributes.append(attribute)

        return cls(logger, clorm.FactBase(copy.deepcopy(kept_symbols + filled_attributes)))

    
        









