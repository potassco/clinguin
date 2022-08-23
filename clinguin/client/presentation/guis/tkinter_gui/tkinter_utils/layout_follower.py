import logging
from clinguin.utils import Logger

from .extension_class import *

class LayoutFollower(ExtensionClass):

    def __init__(self):
        self._logger = logging.getLogger(Logger.client_logger_name)

    @classmethod
    def getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}
        # Layout-Control
        attributes[AttributeNames.grid_column] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.grid_row] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.grid_column_span] = {"value":1, "value_type" : IntegerType}
        attributes[AttributeNames.grid_row_span] = {"value":1, "value_type" : IntegerType}

        attributes[AttributeNames.pos_x] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.pos_y] = {"value":0, "value_type" : IntegerType}

        return attributes


    def _setLayout(self, elements):
        parent = elements[self._parent]
        if hasattr(parent, "getChildOrg"):
            parent_org = getattr(parent, "getChildOrg")()
        else:
            self._logger.warn("Could not find necessary attribute childOrg() in id: " + str(self._parent))
            return

        if parent_org == ChildLayoutType.FLEX:
            self._widget.pack(expand=True, fill='both')

        elif parent_org == ChildLayoutType.GRID:
            grid_pos_column = self._attributes[AttributeNames.grid_column]['value']
            grid_pos_row = self._attributes[AttributeNames.grid_row]['value']

            grid_span_column = self._attributes[AttributeNames.grid_column_span]['value']
            grid_span_row = self._attributes[AttributeNames.grid_row_span]['value']

            if int(grid_pos_column) >= 0 and int(grid_pos_row) >= 0 and int(grid_span_column) >= 1 and int(grid_span_row) >= 1:
                self._widget.grid(
                    column=grid_pos_column, 
                    row=grid_pos_row,
                    columnspan=int(grid_span_column),
                    rowspan = int(grid_span_row))
            else:
                self._logger.warn("Could not set grid-layout due to illegal values for element: " + str(self._id)) 

        elif parent_org == ChildLayoutType.ABSSTATIC or parent_org == ChildLayoutType.RELSTATIC:
            self._widget.pack(expand=True, fill='both')

            x = self._attributes[AttributeNames.pos_x]["value"]
            y = self._attributes[AttributeNames.pos_y]["value"]

            if int(x) >= 0 and int(y) >= 0:
                if parent_org == ChildLayoutType.ABSSTATIC:
                    self._widget.place(
                        x=int(x), 
                        y=int(y))
                elif parent_org == ChildLayoutType.RELSTATIC:
                    self._widget.place(
                        relx=int(x)/100, 
                        rely=int(y)/100)
                else:
                    self._logger.error("For element " + self._id + " an unknown error while positioning has occured!")
                    raise Exception("For element " + self._id + " an unknown error while positioning has occured!")
            else:
                self._logger.warn("For element " + self._id + " ,either posx or posy are not non-negative-numbers.")
        else:
            self._logger.warn("For element " + self._id + " no child layout was defined!")

