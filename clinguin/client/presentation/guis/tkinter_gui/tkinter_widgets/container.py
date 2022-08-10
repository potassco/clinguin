import tkinter as tk

from .root_cmp import *

class Container(RootCmp):

    def _initWidget(self, elements):
        container = tk.Frame(elements[str(self._parent)].getWidget())
        return container

    @classmethod
    def getAttributes(cls):
        attributes = {}
        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType, "description": "CUSTOM-BACKGROUND-COLOR-DESCRIPTION <- Now normal:" + AttributeNames.descriptions[AttributeNames.backgroundcolor]}
        attributes[AttributeNames.width] = {"value":-1, "value_type" : IntegerType}
        attributes[AttributeNames.height] = {"value":-1, "value_type" : IntegerType}
        attributes[AttributeNames.child_org] = {"value":ChildLayoutType.FLEX, "value_type" : ChildLayoutType}
        attributes[AttributeNames.border_width] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.border_color] = {"value":"black", "value_type" : ColorType}

        # Layout-Control
        attributes[AttributeNames.grid_column] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.grid_row] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.grid_column_span] = {"value":1, "value_type" : IntegerType}
        attributes[AttributeNames.grid_row_span] = {"value":1, "value_type" : IntegerType}

        attributes[AttributeNames.pos_x] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.pos_y] = {"value":0, "value_type" : IntegerType}

        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":False, "value_type" : BooleanType}
        attributes[AttributeNames.onhover_background_color] = {"value":"", "value_type" : ColorType}
        attributes[AttributeNames.onhover_border_color] = {"value":"", "value_type" : ColorType}

        return attributes

    @classmethod
    def getCallbacks(cls):
        callbacks = {}

        callbacks["click"] = {"policy":None}

        return callbacks

    #----------------------------------------------------------------------------------------------
    #-----Attributes----
    #----------------------------------------------------------------------------------------------

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        self._widget.configure(background = value)

    def _setWidth(self, elements, key = AttributeNames.width):
        value = self._attributes[key]["value"]
        self._widget.configure(width = int(value))

    def _setHeight(self, elements, key = AttributeNames.height):
        value = self._attributes[key]["value"]
        self._widget.configure(height = int(value))

    def _setChildOrg(self, elements, key = AttributeNames.child_org):
        value = self._attributes[key]["value"]
        self._child_org = value

        if value == ChildLayoutType.FLEX or value == ChildLayoutType.RELSTATIC or value == ChildLayoutType.ABSSTATIC:
            self._widget.pack_propagate(0)
        elif value == ChildLayoutType.GRID:
            self._widget.grid_propagate(0)
        else:
            self._logger.warn("For element " + self._id + " ,for the children-organisation (arg:  " + key + "), the value " + value + " is not a valid option")
    
    def getChildOrg(self):
        return self._child_org
        

    def _setBorderWidth(self, elements, key = AttributeNames.border_width):
        value = self._attributes[key]["value"]
        if value > 0:
            # Not using borderwidth as one cannot set the color of the default border
            self._widget.configure(highlightthickness = int(value))
        elif value == 0:
            pass
        else:
            self._logger.warn("For element " + self._id + " ,setBorderwidth for " + key + " is lesser than 0: " + str(value))


    def _setBorderBackgroundColor(self, elements, key = AttributeNames.border_color):
        # Not using borderwidth as one cannot set the color of the default border
        value = self._attributes[key]["value"]
        self._widget.configure(highlightbackground = value, highlightcolor = value)

    def _setLayout(self, elements):
        parent = elements[self._parent]
        if hasattr(parent, "getChildOrg"):
            parent_org = getattr(parent, "getChildOrg")()
        else:
            self._logger.warn("Could not find necessary attribute childOrg() in id: " + str(self._parent))
            return

        if parent_org == ChildLayoutType.FLEX:
            self._widget.pack(fill='both')
            self._widget.pack_propagate(0)               

        elif parent_org == ChildLayoutType.GRID:
            grid_pos_column = self._attributes[AttributeNames.grid_column]['value']
            grid_pos_row = self._attributes[AttributeNames.grid_row]['value']

            grid_span_column = self._attributes[AttributeNames.grid_column_span]['value']
            grid_span_row = self._attributes[AttributeNames.grid_row_span]['value']

            if int(grid_pos_column) >= 0 and int(grid_pos_row) >= 0 and int(grid_span_column) >= 1 and int(grid_span_row) >= 1:
                self._widget.grid(
                    column=int(grid_pos_column), 
                    row=int(grid_pos_row),
                    columnspan=int(grid_span_column),
                    rowspan = int(grid_span_row))
                self._widget.grid_propagate(0)
            else:
                self._logger.warn("Could not set grid-layout due to illegal values for element: " + str(self._id)) 

        elif parent_org == ChildLayoutType.ABSSTATIC or parent_org == ChildLayoutType.RELSTATIC:
            x = self._attributes[AttributeNames.pos_x]["value"]
            y = self._attributes[AttributeNames.pos_y]["value"]

            if int(x) >= 0 and int(y) >= 0:
                if parent_org == ChildLayoutType.ABSSTATIC:
                    self._widget.place(
                        x=int(x), 
                        y=int(y))
                    self._widget.pack_propagate(0)               
                elif parent_org == ChildLayoutType.RELSTATIC:
                    self._widget.place(
                        relx=int(x)/100, 
                        rely=int(y)/100)
                    self._widget.pack_propagate(0)               
                else:
                    self._logger.error("For element " + self._id + " an unknown error while positioning has occured!")
                    raise Exception("For element " + self._id + " an unknown error while positioning has occured!")
            else:
                self._logger.warn("For element " + self._id + " ,either posx or posy are not non-negative-numbers.")
        else:
            self._logger.warn("For element " + self._id + " no child layout was defined!")
            

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_color = self._attributes[AttributeNames.onhover_background_color]["value"]
        on_hover_border_color = self._attributes[AttributeNames.onhover_border_color]["value"]

        if on_hover == True:
            def enter(event):
                if on_hover_color != "":
                    self._setBackgroundColor(elements, key = AttributeNames.onhover_background_color)
                if on_hover_border_color != "":
                    self._setBorderBackgroundColor(elements, key = AttributeNames.onhover_border_color)

            def leave(event):
                self._setBackgroundColor(elements, key = AttributeNames.backgroundcolor)
                self._setBorderBackgroundColor(elements, key = AttributeNames.border_color)
            
            self._widget.bind('<Enter>', enter)
            self._widget.bind('<Leave>', leave)
 
    #----------------------------------------------------------------------------------------------
    #-----Actions----
    #----------------------------------------------------------------------------------------------
       
    def _defineClickEvent(self, elements, key = CallbackNames.click):
        if self._callbacks[key] and self._callbacks[key]["policy"]:
            def dropdownmenuitemClick(event):
                self._base_engine.assume(self._callbacks[key]["policy"])

            self._widget.bind('<Button-1>', dropdownmenuitemClick)





