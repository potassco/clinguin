% Syntax (Extension of Logic-Program):

% element(ID,TYPE,PARENT_ID)
%   -> Adds an element to the GUI
%   -> ID       -> Must be unique, alphanumeric
%   -> TYPE     -> One of:
%       - WINDOW        - Creates a window
%       - CONTAINER     - A container (div in HTML, frame in tkinter)
%       - LABEL         - A line of text
%       - BUTTON        - A button
%       - DROPDOWN      - Dropdown menu
%       - CANVAS        - One can draw whatever one likes, could be ''interesting'' to implement
%       - ...?
%   -> PARENT_ID -> Parent of the element to add, for window maybe ''root''?

% attribute(ELEMENT_ID, ATTRIBUTE_KEY, ATTRIBUTE_VALUE)
%   -> Defines an attribute of an element
%   -> ELEMENT_ID       -> The ID of the corresponding element
%   -> ATTRIBUTE_KEY    -> One of:
%       - BACKGROUND-COLOR / BC
%       - FONT-COLOR / FC
%       - CHILDREN-ORGANISATION
%       - X/Y 
%       - SHAPE
%       - ...
%   -> ATTRIBUTE_VALUE -> Depends on key:
%       - BC -> Green,Blue,... (some colors)
%       - FC -> same as BC
%       - CHILDREN-ORGANISATION -> grid/canvas/...
%       - X/Y -> Numeric value (outcome depends on parent-children-organisation)
%       - SHAPE -> Maybe oval or something like that
%       - ...

% callback(ELEMENT_ID, ACTION, ADD/RMV, PREDICATE)
%   -> ELEMENT_ID       -> The ID of the corresponding element
%   -> ACTION           -> CLICK,ON-HOVER,... (when the rule fires)
%   -> POLICY           -> If the predicate shall be assumed or removed (only removed from assumptions or removed from program?)
%   -> PREDICATE        -> The predicate 

 
