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

elem(window, window, root).
attr(window, background_color, white).
attr(window, child_layout, flex).
attr(window, "flexDirection", column).

% ------------------------------------------------
elem(button_container, container, window).
attr(button_container, height, 100).
attr(button_container, child_layout, flex).
attr(button_container, "flexDirection", row).
attr(button_container, "order", 1).

elem(guess_button, button, button_container).
attr(guess_button, label, "Make Guess").
when(guess_button, click, callback, transfer_context).


elem(sudoku_grid, container, window).
attr(sudoku_grid, child_layout, grid).
attr(sudoku_grid, "order", 2).
attr(sudoku_grid, height, height_value).
attr(sudoku_grid, width, width_value).

%---------------------------------------------------------------------------------------
% Sudoku-Grid
%---------------------------------------------------------------------------------------

% Grid cells
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0.
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0.

elem(c(X,Y), container, sudoku_grid) :- pos(X,Y).
attr(c(X,Y), grid_column, X-1) :- pos(X,Y).
attr(c(X,Y), grid_row, Y-1) :- pos(X,Y).
attr(c(X,Y),background_color,COLOR):- cell_color(X,Y,COLOR).
%attr(c(X,Y), height, height_value/(dim*dim)) :- pos(X,Y).
%attr(c(X,Y), width, width_value/(dim*dim)) :- pos(X,Y).

% Label
elem(l(X,Y), label, c(X,Y)) :- initial(X,Y,V).
%attr(l(X,Y), "border","1px solid black") :- initial(X,Y,V).
attr(l(X,Y), label, V) :- initial(X,Y,V).
attr(l(X,Y), font_size, "16") :- initial(X,Y,V).
attr(l(X,Y), background_color, COLOR) :- initial(X,Y,V),cell_color(X,Y,COLOR).

% Textfield
menu(X,Y):-pos(X,Y), not initial(X,Y,_).

elem(t(X,Y), textfield, c(X,Y)) :- menu(X,Y), not _c(sudoku(X,Y,_)), not _clinguin_browsing.
when(t(X,Y), type, context, (t(X,Y),add_assumption(sudoku(X,Y,_value)))) :- menu(X,Y), not _c(sudoku(X,Y,_)), not _clinguin_browsing.

% Static 
% Maybe change this to label, etc. if time...
elem(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y), _c(sudoku(X,Y,_)).
elem(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y), _clinguin_browsing.

attr(m(X,Y), font_size, "16") :- menu(X,Y).
attr(m(X,Y), selected, @concat(V,"*")) :- menu(X,Y), _c(sudoku(X,Y,V)), not _clinguin_assume(sudoku(X,Y,V)).
attr(m(X,Y), selected, V) :- menu(X,Y), _clinguin_assume(sudoku(X,Y,V)).
attr(m(X,Y), selected, @concat(V,"+")) :- menu(X,Y), sudoku(X,Y,V), _clinguin_browsing, not _c(sudoku(X,Y,V)).
attr(m(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
elem(m, menu_bar, window).
elem(ms, menu_bar_section, m).
attr(m, title,"Sudoku").
attr(ms, label, "Options").
elem(ms_clear, menu_bar_section_item, ms).
attr(ms_clear, label, "Clear").
attr(ms_clear, accelerator, "Cmd+C").
when(ms_clear, click, callback, clear_assumptions).
elem(ms_next, menu_bar_section_item, ms).
attr(ms_next, label, "Next").
attr(ms_next, accelerator, "Cmd+N").
when(ms_next, click, callback, next_solution).
elem(ms_select, menu_bar_section_item, ms).
attr(ms_select, label, "Select").
attr(ms_select, accelerator, "Cmd+S").
when(ms_select, click, callback, select).


