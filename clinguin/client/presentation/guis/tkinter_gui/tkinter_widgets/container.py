import tkinter as tk

from .root_cmp import RootCmp

from tkinter_gui.tkinter_utils.standard_text_processing import StandardTextProcessing
from tkinter_gui.tkinter_utils.attribute_names import AttributeNames
from tkinter_gui.tkinter_utils.callback_names import CallbackNames

class Container(RootCmp):

    def _initWidget(self, elements):
        container = tk.Frame(elements[str(self._parent)].getWidget())
        return container

    @classmethod
    def getAttributes(cls):
        attributes = {}
        attributes[AttributeNames.backgroundcolor] = {"value":"white", "description": "CUSTOM-BACKGROUND-COLOR-DESCRIPTION <- Now normal:" + AttributeNames.descriptions[AttributeNames.backgroundcolor]}
        attributes[AttributeNames.width] = {"value":str(-1)}
        attributes[AttributeNames.height] = {"value":str(-1)}
        attributes[AttributeNames.child_org] = {"value":"flex"}
        attributes[AttributeNames.border_width] = {"value":str(0)}
        attributes[AttributeNames.border_color] = {"value":"black"}

        # Layout-Control
        attributes[AttributeNames.grid_column] = {"value":str(0)}
        attributes[AttributeNames.grid_row] = {"value":str(0)}
        attributes[AttributeNames.grid_column_span] = {"value":str(1)}
        attributes[AttributeNames.grid_row_span] = {"value":str(1)}

        attributes[AttributeNames.pos_x] = {"value":str(0)}
        attributes[AttributeNames.pos_y] = {"value":str(0)}

        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":"false"}
        attributes[AttributeNames.onhover_background_color] = {"value":""}
        attributes[AttributeNames.onhover_border_color] = {"value":""}

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
        value = StandardTextProcessing.parseStringWithQuotes(value)
        self._widget.configure(background = value)

    def _setWidth(self, elements, key = AttributeNames.width):
        value = self._attributes[key]["value"]
        if value.isdigit() and int(value) >= -1:
            if int(value) >= 0:
                self._widget.configure(width = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setWidth for " + key + " is not a digit: " + value)


    def _setHeight(self, elements, key = AttributeNames.height):
        value = self._attributes[key]["value"]
        if value.isdigit() and int(value) >= -1:
            if int(value) >= 0:
                self._widget.configure(height = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setHeight for " + key + " is not a digit: " + value)

    def _setChildOrg(self, elements, key = AttributeNames.child_org):
        value = self._attributes[key]["value"]
        self._child_org = value

        if value == "flex" or value == "relstatic" or value == "absstatic":
            self._widget.pack_propagate(0)
        elif value == "grid":
            self._widget.grid_propagate(0)
        else:
            self._logger.warn("For element " + self._id + " ,for the children-organisation (arg:  " + key + "), the value " + value + " is not a valid option")
    
    def getChildOrg(self):
        return self._child_org
        

    def _setBorderWidth(self, elements, key = AttributeNames.border_width):
        value = self._attributes[key]["value"]
        if value.isdigit():
            if int(value) > 0:
                # Not using borderwidth as one cannot set the color of the default border
                self._widget.configure(highlightthickness = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setBorderwidth for " + key + " is not a digit: " + value)


    def _setBorderBackgroundColor(self, elements, key = AttributeNames.border_color):
        # Not using borderwidth as one cannot set the color of the default border
        value = self._attributes[key]["value"]
        value = StandardTextProcessing.parseStringWithQuotes(value)
        self._widget.configure(highlightbackground = value, highlightcolor = value)

    def _setLayout(self, elements):
        parent = elements[self._parent]
        if hasattr(parent, "getChildOrg"):
            parent_org = getattr(parent, "getChildOrg")()
        else:
            self._logger.warn("Could not find necessary attribute childOrg() in id: " + str(self._parent))
            return

        if parent_org == "flex":
            self._widget.pack(fill='both')
            self._widget.pack_propagate(0)               

        elif parent_org == "grid":
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

        elif parent_org == "absstatic" or parent_org =="relstatic":
            x = self._attributes[AttributeNames.pos_x]["value"]
            y = self._attributes[AttributeNames.pos_y]["value"]

            if x.isdigit() and y.isdigit():
                if int(x) >= 0 and int(y) >= 0:
                    if parent_org == "absstatic":
                        self._widget.place(
                            x=int(x), 
                            y=int(y))
                        self._widget.pack_propagate(0)               
                    elif parent_org == "relstatic":
                        self._widget.place(
                            relx=int(x)/100, 
                            rely=int(y)/100)
                        self._widget.pack_propagate(0)               
                else:
                    self._logger.warn("For element " + self._id + " ,either posx or posy are not non-negative-numbers.")
                
            else:
                self._logger.warn("For element " + self._id + " ,either posx or posy are not numbers.")

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_color = self._attributes[AttributeNames.onhover_background_color]["value"]
        on_hover_border_color = self._attributes[AttributeNames.onhover_border_color]["value"]

        if on_hover == "true":
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





