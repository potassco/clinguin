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
attribute(window, background_color, white).
attribute(window, child_layout, flex).
attribute(window, "flexDirection", column).

% ------------------------------------------------
element(button_container, container, window).
attribute(button_container, height, 100).
attribute(button_container, child_layout, flex).
attribute(button_container, "flexDirection", row).
attribute(button_container, "order", 1).

element(guess_button, button, button_container).
attribute(guess_button, label, "Make Guess").
do(guess_button, click, callback, transfer_context).


element(sudoku_grid, container, window).
attribute(sudoku_grid, child_layout, grid).
attribute(sudoku_grid, "order", 2).
attribute(sudoku_grid, height, height_value).
attribute(sudoku_grid, width, width_value).

%---------------------------------------------------------------------------------------
% Sudoku-Grid
%---------------------------------------------------------------------------------------

% Grid cells
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0.
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0.

element(c(X,Y), container, sudoku_grid) :- pos(X,Y).
attribute(c(X,Y), grid_column, X-1) :- pos(X,Y).
attribute(c(X,Y), grid_row, Y-1) :- pos(X,Y).
attribute(c(X,Y),background_color,COLOR):- cell_color(X,Y,COLOR).
%attribute(c(X,Y), height, height_value/(dim*dim)) :- pos(X,Y).
%attribute(c(X,Y), width, width_value/(dim*dim)) :- pos(X,Y).

% Label
element(l(X,Y), label, c(X,Y)) :- initial(X,Y,V).
%attribute(l(X,Y), "border","1px solid black") :- initial(X,Y,V).
attribute(l(X,Y), label, V) :- initial(X,Y,V).
attribute(l(X,Y), font_size, "16") :- initial(X,Y,V).
attribute(l(X,Y), background_color, COLOR) :- initial(X,Y,V),cell_color(X,Y,COLOR).

% Textfield
menu(X,Y):-pos(X,Y), not initial(X,Y,_).

element(t(X,Y), textfield, c(X,Y)) :- menu(X,Y), not _c(sudoku(X,Y,_)), not _clinguin_browsing.
do(t(X,Y), type, context, (t(X,Y),add_assumption(sudoku(X,Y,_value)))) :- menu(X,Y), not _c(sudoku(X,Y,_)), not _clinguin_browsing.

% Static 
% Maybe change this to label, etc. if time...
element(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y), _c(sudoku(X,Y,_)).
element(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y), _clinguin_browsing.

attribute(m(X,Y), font_size, "16") :- menu(X,Y).
attribute(m(X,Y), selected, @concat(V,"*")) :- menu(X,Y), _c(sudoku(X,Y,V)), not _clinguin_assume(sudoku(X,Y,V)).
attribute(m(X,Y), selected, V) :- menu(X,Y), _clinguin_assume(sudoku(X,Y,V)).
attribute(m(X,Y), selected, @concat(V,"+")) :- menu(X,Y), sudoku(X,Y,V), _clinguin_browsing, not _c(sudoku(X,Y,V)).
attribute(m(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
element(m, menu_bar, window).
element(ms, menu_bar_section, m).
attribute(m, title,"Sudoku").
attribute(ms, label, "Options").
element(ms_clear, menu_bar_section_item, ms).
attribute(ms_clear, label, "Clear").
attribute(ms_clear, accelerator, "Cmd+C").
do(ms_clear, click, callback, clear_assumptions).
element(ms_next, menu_bar_section_item, ms).
attribute(ms_next, label, "Next").
attribute(ms_next, accelerator, "Cmd+N").
do(ms_next, click, callback, next_solution).
element(ms_select, menu_bar_section_item, ms).
attribute(ms_select, label, "Select").
attribute(ms_select, accelerator, "Cmd+S").
do(ms_select, click, callback, select).


