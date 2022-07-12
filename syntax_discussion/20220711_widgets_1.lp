% ------------------------------
% Window setup

element(window, window, root).
attribute(window, width, 900).
attribute(window, height, 900).
attribute(window, title, "Sudoku").
attribute(window, resizable_height, 0).
attribute(window, resizable_width, 0).

% NEW:
attribute(window, children-organisation, grid).

% ------------------------------
% Make frames to define grid

element(f(X,Y), container, window) :- pos(X,Y).

attribute(f(X,Y), background-color, white).
attribute(f(X,Y), grid_row, X) :- pos(X,Y).
attribute(f(X,Y), grid_column, Y) :- pos(X,Y).

attribute(f(X,Y), width, 100) :- pos(X,Y).
attribute(f(X,Y), height, 100) :- pos(X,Y).
attribute(f(X,Y), highlightbackground, black) :- pos(X,Y).
attribute(f(X,Y), highlightthickness, 1) :- pos(X,Y).

attribute(f(X,Y), children-organisation, canvas) :- pos(X,Y).

% ------------------------------
% Make menu buttons

element(m(X,Y), dropdown, f(X,Y)) :- pos(X,Y).

attribute(m(X,Y), font, "Arial 16") :- pos(X,Y).
attribute(m(X,Y), width, 30) :- pos(X,Y).
attribute(m(X,Y), height, 16) :- pos(X,Y).
attribute(m(X,Y), foreground-color, gray) :- pos(X,Y), initial(X,Y,_).
attribute(m(X,Y), background-color, white) :- subgrid(X,Y,S), S\2==0.

attribute(m(X,Y), pos_X, 35) :- pos(X,Y). % measured from the left of the parent element
attribute(m(X,Y), pos_Y, 42) :- pos(X,Y). % measured from the top of the parent element
attribute(m(X,Y), pad_X, 5)  :- pos(X,Y).
attribute(m(X,Y), pad_Y, 3)  :- pos(X,Y).


% ------------------------------
% Interactivity part -> Function 

callback(m(X,Y), click, brave, assume(sudoku(X,Y,V))) :- sudoku(X,Y,V). 
% The function ''assume'' is assumed to be existant in the solver/engine/...
% Where do we know, which elements m(X,Y) should have? -> Attributes which are solved bravely?
% Value of dropdown... multiple (brave makes sense), vs. value of button... one (only cautious makes sense?)





