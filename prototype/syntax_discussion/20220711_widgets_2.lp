% ------------------------------
% Window setup

element(window, window, root).
attribute(window, c, width, 900).
attribute(window, c, height, 900).
attribute(window, c, title, "Sudoku").
attribute(window, c, resizable_height, 0).
attribute(window, c, resizable_width, 0).

% NEW:
attribute(window, c, children-organisation, grid).

% ------------------------------
% Make frames to define grid

element(f(X,Y), container, window) :- pos(X,Y).

attribute(f(X,Y), c, background-color, white).
attribute(f(X,Y), c, grid_row, X) :- pos(X,Y).
attribute(f(X,Y), c, grid_column, Y) :- pos(X,Y).

attribute(f(X,Y), c, width, 100) :- pos(X,Y).
attribute(f(X,Y), c, height, 100) :- pos(X,Y).
attribute(f(X,Y), c, highlightbackground, black) :- pos(X,Y).
attribute(f(X,Y), c, highlightthickness, 1) :- pos(X,Y).

attribute(f(X,Y), c, children-organisation, canvas) :- pos(X,Y).

% ------------------------------
% Make menu buttons

element(m(X,Y), dropdown, f(X,Y)) :- pos(X,Y).

attribute(m(X,Y), c, font, "Arial 16") :- pos(X,Y).
attribute(m(X,Y), c, width, 30) :- pos(X,Y).
attribute(m(X,Y), c, height, 16) :- pos(X,Y).
attribute(m(X,Y), c, foreground-color, gray) :- pos(X,Y), initial(X,Y,_).
attribute(m(X,Y), c, background-color, white) :- subgrid(X,Y,S), S\2==0.

attribute(m(X,Y), c, pos_X, 35) :- pos(X,Y). % measured from the left of the parent element
attribute(m(X,Y), c, pos_Y, 42) :- pos(X,Y). % measured from the top of the parent element
attribute(m(X,Y), c, pad_X, 5)  :- pos(X,Y).
attribute(m(X,Y), c, pad_Y, 3)  :- pos(X,Y).


% ------------------------------
% Interactivity part (Brave reasoning)

attribute(m(X,Y), b, option, V) :- sudoku(X,Y,V). 
callback(m(X,Y), click, b, assume(sudoku(X,Y,V))) :- sudoku(X,Y,V). 
% The function ''assume'' is assumed to be existant in the solver/engine/...
% Where do we know, which elements m(X,Y) should have? -> Attributes which are solved bravely?

% Value of dropdown... multiple (brave makes sense), vs. value of button... one (only cautious makes sense?)





