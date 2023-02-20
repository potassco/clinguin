#script(python)
from clingo.symbol import String
def concat(*args):
    return String(''.join([str(x).strip('"') for x in args]))
#end.
#const height_value = 450.
#const width_value = 450.
#const dim = 3.

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
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0.
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0.

element(c(X,Y), container, window) :- pos(X,Y).
attribute(c(X,Y), grid_column, X-1) :- pos(X,Y).
attribute(c(X,Y), grid_row, Y-1) :- pos(X,Y).
attribute(c(X,Y),background_color,COLOR):- cell_color(X,Y,COLOR).
attribute(c(X,Y), height, height_value/(dim*dim)) :- pos(X,Y).
attribute(c(X,Y), width, width_value/(dim*dim)) :- pos(X,Y).

% Label
element(l(X,Y), label, c(X,Y)) :- initial(X,Y,V).
attribute(l(X,Y), label, V) :- initial(X,Y,V).
attribute(l(X,Y), font_size, 16) :- initial(X,Y,V).
attribute(l(X,Y), background_color, COLOR) :- initial(X,Y,V),cell_color(X,Y,COLOR).

% Option Menu
menu(X,Y):-pos(X,Y), not initial(X,Y,_).
element(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y).
attribute(m(X,Y), selected, V) :- menu(X,Y), sudoku(X,Y,V).
attribute(m(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
callback(m(X,Y), clear, remove_assumption_signature(sudoku(X,Y,any))) :- menu(X,Y).

% Option menu Item
element(mi(X,Y,V), dropdown_menu_item, m(X,Y)) :- menu(X,Y), _b(sudoku(X,Y,V)).
attribute(mi(X,Y,V), label, @concat("S",V)) :- menu(X,Y), _b(sudoku(X,Y,V)).
callback(mi(X,Y,V), click, add_assumption(sudoku(X,Y,V))) :- menu(X,Y), _b(sudoku(X,Y,V)).

%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
element(m, menu_bar, window).
element(ms, menu_bar_section, m).
attribute(ms, label, "Options").
element(ms_clear, menu_bar_section_item, ms).
attribute(ms_clear, label, "Clear").
attribute(ms_clear, accelerator, "Cmd+C").
callback(ms_clear, click, clear_assumptions).
element(ms_next, menu_bar_section_item, ms).
attribute(ms_next, label, "Next").
attribute(ms_next, accelerator, "Cmd+N").
callback(ms_next, click, next_solution).


