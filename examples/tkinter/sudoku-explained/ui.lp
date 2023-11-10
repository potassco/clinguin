
#const height_value = 450.
#const width_value = 450.
#const dim = 3.
#const red="#CE474F".
#const orange="#CE8B47".

val(1..dim*dim).

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
muc_cell(X,Y):- _muc(initial(X,Y,_)).
muc_cell(X,Y):- _muc(sudoku(X,Y,_)).
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0, not muc_cell(X,Y).
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0, not muc_cell(X,Y).
cell_color(X,Y,red):-_muc(initial(X,Y,_)).
cell_color(X,Y,orange):-_muc(sudoku(X,Y,_)).

menu(X,Y):-pos(X,Y), not initial(X,Y,_).
elem(c(X,Y), container, window) :- pos(X,Y).
attr(c(X,Y), grid_column, X-1) :- pos(X,Y).
attr(c(X,Y), grid_row, Y-1) :- pos(X,Y).
attr(c(X,Y), background_color,COLOR):- cell_color(X,Y,COLOR).
attr(c(X,Y), height, height_value/(dim*dim)) :- pos(X,Y).
attr(c(X,Y), width, width_value/(dim*dim)) :- pos(X,Y).

% Label
elem(l(X,Y), label, c(X,Y)) :- initial(X,Y,V).
attr(l(X,Y), label, V) :- initial(X,Y,V).
attr(l(X,Y), font_size, 16) :- initial(X,Y,V).
attr(l(X,Y), background_color, COLOR) :- initial(X,Y,V), cell_color(X,Y,COLOR).

% Option Menu
elem(m(X,Y), dropdown_menu, c(X,Y)) :- menu(X,Y).
attr(m(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
attr(m(X,Y), selected, V) :- menu(X,Y), _clinguin_assume(sudoku(X,Y,V)).
attr(m(X,Y), selected, V) :- menu(X,Y), _muc(sudoku(X,Y,V)).
attr(m(X,Y), selected, V) :- sudoku(X,Y,V), _clinguin_browsing.
when(m(X,Y), clear, call, remove_assumption_signature(sudoku(X,Y,any))) :- menu(X,Y).

% Option menu Item
elem(mi(X,Y,V), dropdown_menu_item, m(X,Y)) :- menu(X,Y), val(V).
attr(mi(X,Y,V), label, @concat("",V,"  ✕")) :- menu(X,Y), val(V), not _b(sudoku(X,Y,V)).
attr(mi(X,Y,V), label, V) :- menu(X,Y), val(V), _b(sudoku(X,Y,V)).
when(mi(X,Y,V), click, call, add_assumption(sudoku(X,Y,V))) :- menu(X,Y), val(V).


% Menu Bar
elem(menu_bar, menu_bar, window).
elem(menu_bar_section, menu_bar_section, menu_bar).
attr(menu_bar_section, label, "Options").
elem(menu_bar_section_clear, menu_bar_section_item, menu_bar_section).
attr(menu_bar_section_clear, label, "Clear").
attr(menu_bar_section_clear, accelerator, "Cmd+C").
when(menu_bar_section_clear, click, call, clear_assumptions).
elem(menu_bar_section_next, menu_bar_section_item, menu_bar_section).
attr(menu_bar_section_next, label, "Next").
attr(menu_bar_section_next, accelerator, "Cmd+N").
when(menu_bar_section_next, click, call, next_solution).
elem(menu_bar_section_select, menu_bar_section_item, menu_bar_section).
attr(menu_bar_section_select, label, "Select").
attr(menu_bar_section_select, accelerator, "Cmd+S").
when(menu_bar_section_select, click, call, select).


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