
#const height_value = 450.
#const width_value = 450.
#const dim = 3.
#const red="#CE474F".
#const orange="#CE8B47".

val(1..dim*dim).

%---------------------------------------------------------------------------------------
% Window
%---------------------------------------------------------------------------------------
element(window, window, root).
attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, background_color, white).
attribute(window, resizable_x, 0).
attribute(window, resizable_y, 0).
attribute(window, child_layout, grid).

%---------------------------------------------------------------------------------------
% Sudoku-Grid
%---------------------------------------------------------------------------------------


% Grid cells
muc_cell(X,Y):- _muc(initial(X,Y,_)).
muc_cell(X,Y):- _muc(sudoku(X,Y,_)).
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0, not muc_cell(X,Y).
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0, not muc_cell(X,Y).
cell_color(X,Y,red):-_muc(initial(X,Y,_)).
cell_color(X,Y,orange):-_muc(sudoku(X,Y,_)).

menu(X,Y):-pos(X,Y), not initial(X,Y,_).
element(c(X,Y), container, window) :- pos(X,Y).
attribute(c(X,Y), grid_column, X-1) :- pos(X,Y).
attribute(c(X,Y), grid_row, Y-1) :- pos(X,Y).
attribute(c(X,Y), background_color,COLOR):- cell_color(X,Y,COLOR).
attribute(c(X,Y), height, height_value/(dim*dim)) :- pos(X,Y).
attribute(c(X,Y), width, width_value/(dim*dim)) :- pos(X,Y).

% Label
element(l(X,Y), label, c(X,Y)) :- initial(X,Y,V).
attribute(l(X,Y), label, V) :- initial(X,Y,V).
attribute(l(X,Y), font_size, 16) :- initial(X,Y,V).
attribute(l(X,Y), background_color, COLOR) :- initial(X,Y,V), cell_color(X,Y,COLOR).

% Option Menu
element(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y).
attribute(m(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
attribute(m(X,Y), selected, V) :- menu(X,Y), _assume(sudoku(X,Y,V)).
attribute(m(X,Y), selected, V) :- menu(X,Y), _muc(sudoku(X,Y,V)).
attribute(m(X,Y), selected, V) :- sudoku(X,Y,V), clinguin_browsing.
callback(m(X,Y), clear, remove_assumption_signature(sudoku(X,Y,any))) :- menu(X,Y).

% Option menu Item
element(mi(X,Y,V), dropdown_menu_item, m(X,Y)) :- menu(X,Y), val(V).
attribute(mi(X,Y,V), label, @concat(V,"  ✕")) :- menu(X,Y), val(V), not _b(sudoku(X,Y,V)).
attribute(mi(X,Y,V), label, V) :- menu(X,Y), val(V), _b(sudoku(X,Y,V)).
callback(mi(X,Y,V), click, add_assumption(sudoku(X,Y,V))) :- menu(X,Y), val(V).


#script(python)
from clingo import String
def concat(*args):
    """
    Concatenates the given symbols as a string
    Args:
        args: All symbols
    Returns:
        (clingo.Symbol.String) The string concatenating all symbols
    """
    return String(''.join([str(x).strip('"') for x in args]))
#end.