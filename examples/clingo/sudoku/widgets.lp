
element(window, window, root).
#const height_value= 550.
#const width_value= 550.
#const grid_height_value = 450.
#const grid_width_value = 450.
#const dim = 3.

%---------------------------------------------------------------------------------------
% Window
%---------------------------------------------------------------------------------------

attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, background_color, white).
attribute(window, resizable_x, 0).
attribute(window, resizable_y, 0).
attribute(window, child_layout, grid).

%---------------------------------------------------------------------------------------
% Sudoku-Grid
%---------------------------------------------------------------------------------------

element(uc, container, window).
attribute(uc, grid_column, 0).
attribute(uc, grid_row, 0).
attribute(uc, height, grid_height_value).
attribute(uc, width, grid_width_value).
attribute(uc, child_layout, grid).

% Grid cells
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0.
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0.

menu(X,Y):-pos(X,Y), not initial(X,Y,_).

element(c(X,Y), label, uc) :- initial(X,Y,V).
element(c(X,Y), dropdown_menu, uc) :- menu(X,Y).

attribute(c(X,Y), grid_column, X-1) :- pos(X,Y).
attribute(c(X,Y), grid_row, Y-1) :- pos(X,Y).
attribute(c(X,Y),background_color,COLOR):- cell_color(X,Y,COLOR).
attribute(c(X,Y), height, grid_height_value/(dim*dim)) :- pos(X,Y).
attribute(c(X,Y), width, grid_width_value/(dim*dim)) :- pos(X,Y).

attribute(c(X,Y), background_color, COLOR) :- initial(X,Y,V), cell_color(X,Y,COLOR).
attribute(c(X,Y), label, V) :- initial(X,Y,V).
attribute(c(X,Y), font_size, 16) :- initial(X,Y,V).

% Option Menu
attribute(c(X,Y), background_color, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
attribute(c(X,Y), selected, V) :- menu(X,Y), sudoku(X,Y,V).

% Option menu Item
element(mi(X,Y,V), dropdown_menu_item, c(X,Y)) :- menu(X,Y), _b(sudoku(X,Y,V)).
attribute(mi(X,Y,V), label, V) :- menu(X,Y), _b(sudoku(X,Y,V)).
callback(mi(X,Y,V), click, add_assumption(sudoku(X,Y,V))) :- menu(X,Y), _b(sudoku(X,Y,V)).

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
% Footer Buttons
%---------------------------------------------------------------------------------------

element(buttonsc_c, container, window).
attribute(buttonsc_c, grid_column, 0).
attribute(buttonsc_c, grid_row, 1).
attribute(buttonsc_c, height, height_value - grid_height_value).
attribute(buttonsc_c, width, width_value).
attribute(buttonsc_c, background_color, white).
attribute(buttonsc_c, child_layout, absstatic).

element(buttonsc, container, buttonsc_c).
attribute(buttonsc, pos_x, 200).
attribute(buttonsc, pos_y, 5).
attribute(buttonsc, height, 300).
attribute(buttonsc, width, 150).
attribute(buttonsc, background_color, white).
attribute(buttonsc, child_layout, grid).

element(clear_label, label, buttonsc).
attribute(clear_label, height,45).
attribute(clear_label, width,150).
attribute(clear_label, grid_column, 0).
attribute(clear_label, grid_row, 0).
attribute(clear_label, label, "Clear").
attribute(clear_label, background_color, "#ff4e4e").
attribute(clear_label, on_hover, true).
attribute(clear_label, on_hover_background_color, "#a00000").
attribute(clear_label, on_hover_foreground_color, "#111111"). 
callback(clear_label, click, clear_assumptions). 

element(next_label, label, buttonsc).
attribute(next_label, grid_column, 0).
attribute(next_label, grid_row, 1).
attribute(next_label, height,45).
attribute(next_label, width,150).
attribute(next_label, label, "Next Solution").
attribute(next_label, background_color, "#4eff4e").
attribute(next_label, on_hover, true).
attribute(next_label, on_hover_background_color, "#00a000").
attribute(next_label, on_hover_foreground_color, "#111111"). 
attribute(next_label, font_family, "Helvetica").
attribute(next_label, font_weight, "bold").
attribute(next_label, font_size, 16).
callback(next_label, click, nextSolution). 

%---------------------------------------------------------------------------------------
% Messages
%---------------------------------------------------------------------------------------

element(message, message, window) :- no_more_solutions.
attribute(message, title, "Finished") :- no_more_solutions.
attribute(message, message, "No more solutions available.") :- no_more_solutions.

