
element(window, window, root).
#const grid_height_value = 450.
#const grid_width_value = 450.
#const dim = 3.
#const red="#CE474F".

val(1..dim*dim).

%---------------------------------------------------------------------------------------
% Window
%---------------------------------------------------------------------------------------

attribute(window, height, grid_height_value).
attribute(window, width, grid_width_value).
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
cell_color(X,Y,red):-muc_cell(X,Y).

menu(X,Y):-pos(X,Y), not initial(X,Y,_).
element(c(X,Y), label, window) :- initial(X,Y,V).
element(c(X,Y), dropdown_menu, window) :- menu(X,Y).

attribute(c(X,Y), grid_column, X-1) :- pos(X,Y).
attribute(c(X,Y), grid_row, Y-1) :- pos(X,Y).
attribute(c(X,Y), background_color,COLOR):- cell_color(X,Y,COLOR).
attribute(c(X,Y), height, grid_height_value/(dim*dim)) :- pos(X,Y).
attribute(c(X,Y), width, grid_width_value/(dim*dim)) :- pos(X,Y).

attribute(c(X,Y), background_color, COLOR) :- initial(X,Y,V), cell_color(X,Y,COLOR).
attribute(c(X,Y), label, V) :- initial(X,Y,V).
attribute(c(X,Y), font_size, 16) :- initial(X,Y,V).

% Option Menu
attribute(c(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
attribute(c(X,Y), selected, V) :- menu(X,Y), sudoku(X,Y,V).
attribute(c(X,Y), selected, V) :- menu(X,Y), _muc(sudoku(X,Y,V)).

callback(c(X,Y), clear, remove_assumption_signature(sudoku(X,Y,any),3)) :- menu(X,Y).

% Option menu Item
element(mi(X,Y,V), dropdown_menu_item, c(X,Y)) :- menu(X,Y), val(V).
attribute(mi(X,Y,V), label, @concat(V,"  ✕")) :- menu(X,Y), val(V), not _b(sudoku(X,Y,V)).
attribute(mi(X,Y,V), label, V) :- menu(X,Y), val(V), _b(sudoku(X,Y,V)).
callback(mi(X,Y,V), click, add_assumption(sudoku(X,Y,V))) :- menu(X,Y), val(V).

%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

element(m, menu_bar, window).
element(ms, menu_bar_section, m).
attribute(ms, label, "Options").
element(ms_clear, menu_bar_section_item, ms).
attribute(ms_clear, label, "Clear").
callback(ms_clear, click, clear_assumptions).
element(ms_next, menu_bar_section_item, ms).
attribute(ms_next, label, "Next").
callback(ms_next, click, next_solution).

%---------------------------------------------------------------------------------------
% Messages
%---------------------------------------------------------------------------------------

element(message, message, window) :- no_more_solutions.
attribute(message, title, "Finished") :- no_more_solutions.
attribute(message, message, "No more solutions available.") :- no_more_solutions.

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