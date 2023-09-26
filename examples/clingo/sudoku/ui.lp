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
attr(window, height, height_value).
attr(window, width, width_value).
attr(window, background_color, white).
attr(window, resizable_x, 0).
attr(window, resizable_y, 0).
attr(window, child_layout, grid).

%---------------------------------------------------------------------------------------
% Sudoku-Grid
%---------------------------------------------------------------------------------------

% Grid cells
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0.
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0.

elem(c(X,Y), container, window) :- pos(X,Y).
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

% Option Menu
menu(X,Y):-pos(X,Y), not initial(X,Y,_).
elem(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y).
attr(m(X,Y), font_size, "16") :- menu(X,Y).
attr(m(X,Y), selected, @concat(V,"*")) :- menu(X,Y), _c(sudoku(X,Y,V)), not _clinguin_assume(sudoku(X,Y,V)).
attr(m(X,Y), selected, V) :- menu(X,Y), _clinguin_assume(sudoku(X,Y,V)).
attr(m(X,Y), selected, @concat(V,"+")) :- menu(X,Y), sudoku(X,Y,V), _clinguin_browsing, not _c(sudoku(X,Y,V)).


attr(m(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
callback(m(X,Y), clear, remove_assumption_signature(sudoku(X,Y,any))) :- menu(X,Y).

% Option menu Item
elem(mi(X,Y,V), dropdown_menu_item, m(X,Y)) :- menu(X,Y), _b(sudoku(X,Y,V)).
attr(mi(X,Y,V), font_size, "16") :- menu(X,Y), _b(sudoku(X,Y,V)).
attr(mi(X,Y,V), label, V) :- menu(X,Y), _b(sudoku(X,Y,V)).
callback(mi(X,Y,V), click, add_assumption(sudoku(X,Y,V))) :- menu(X,Y), _b(sudoku(X,Y,V)).
attr(mi(X,Y,V), foreground_color,"green") :- menu(X,Y), _b(sudoku(X,Y,V)).

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
callback(ms_clear, click, clear_assumptions).
elem(ms_next, menu_bar_section_item, ms).
attr(ms_next, label, "Next").
attr(ms_next, accelerator, "Cmd+N").
callback(ms_next, click, next_solution).
elem(ms_select, menu_bar_section_item, ms).
attr(ms_select, label, "Select").
attr(ms_select, accelerator, "Cmd+S").
callback(ms_select, click, select).


