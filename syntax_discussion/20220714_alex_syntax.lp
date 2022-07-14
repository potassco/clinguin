% added feedback from 2022-07-11 meeting
% Syntax (Extension of Logic-Program):
% This syntax is the syntax used in the Prototype (Simple client server V2)

% element(ID,TYPE,PARENT_ID)
%   -> Adds an element to the GUI
%   -> ID       -> Must be unique, alphanumeric
%   -> TYPE     -> One of:
%       - window        - Creates a window
%       - container     - A container (div in HTML, frame in tkinter)
%       - dropdownmenu      - Dropdown menu
%       - dropdownmenuitem - An option of the dropdown
%   -> PARENT_ID -> Parent of the element to add, for window maybe ''root''?

% attribute(ELEMENT_ID, ATTRIBUTE_KEY, ATTRIBUTE_VALUE)
%   -> Defines an attribute of an element
%   -> ELEMENT_ID       -> The ID of the corresponding element
%   -> ATTRIBUTE_KEY    -> One of:
%       - backgroundcolor 	-> usable for window and container (anything possible which works for tkinter)
%	- width 		-> usable for window, container and dropdownmenu (pos. integer)
%	- height		-> usable for window and container (pos. integer)
%	- selected		-> usable for the dropdownmenu (must be an ID of a child dropdownmenuitem)
%	- initially_selected	-> basically like selected, just with a lower priority 
%	- gridx		-> useable for container (sets the grid position, non-neg. integer)
%	- gridy		-> useable for container (sets the grid position, non-neg. integer)
%	- label		-> useable for dropdownmenuitem (if the displayed label should differ from the ID)
% callback(ELEMENT_ID, ACTION, POLICY)
%   -> ELEMENT_ID       -> The ID of the corresponding element - currently ONLY works for dropdownmenuitem elements
%   -> ACTION           -> click (the only thing that works currently)
%   -> POLICY           -> Function in the solver that shall be executed, like ''assume(predicateXYZ)'' (adds an assumption), ''solve'' (solve the LP)
 
