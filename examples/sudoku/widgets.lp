
_brave_element_type(dropdownmenuitem).

element(window, window, root).
#const height_value= 550.
#const width_value= 550.
#const grid_height_value = 450.
#const grid_width_value = 450.

%---------------------------------------------------------------------------------------
% Window
%---------------------------------------------------------------------------------------

attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, backgroundcolor, white).
attribute(window, resizablex, 0).
attribute(window, resizabley, 0).
attribute(window, childorg, grid).

%---------------------------------------------------------------------------------------
% Sudoku-Grid
%---------------------------------------------------------------------------------------

element(uc, container, window).
attribute(uc, gridcolumn, 0).
attribute(uc, gridrow, 0).
attribute(uc, height, grid_height_value).
attribute(uc, width, grid_width_value).
attribute(uc, childorg, grid).

% Grid cells
cell_color(X,Y,gray):-subgrid(X,Y,S), S\2==0.
cell_color(X,Y,white):-subgrid(X,Y,S), S\2!=0.
element(c(X,Y), container, uc) :- pos(X,Y).
attribute(c(X,Y), gridcolumn, X-1) :- pos(X,Y).
attribute(c(X,Y), gridrow, Y-1) :- pos(X,Y).
attribute(c(X,Y),backgroundcolor,COLOR):- cell_color(X,Y,COLOR).
attribute(c(X,Y),bordercolor,black):- pos(X,Y).
% attribute(c(X,Y),borderwidth,"0.5"):- pos(X,Y).
attribute(c(X,Y), height, grid_height_value/(dim*dim)) :- pos(X,Y).
attribute(c(X,Y), width, grid_width_value/(dim*dim)) :- pos(X,Y).

element(l(X,Y), label, c(X,Y)) :- initial(X,Y,V).
attribute(l(X,Y), backgroundcolor, COLOR) :- initial(X,Y,V), cell_color(X,Y,COLOR).
attribute(l(X,Y), label, V) :- initial(X,Y,V).
attribute(l(X,Y), fontsize, 16) :- initial(X,Y,V).

% Option Menu
menu(X,Y):-pos(X,Y), not initial(X,Y,_).
element(m(X,Y), dropdownmenu, c(X,Y)) :- menu(X,Y).
attribute(m(X,Y), backgroundcolor, COLOR) :- menu(X,Y), cell_color(X,Y,COLOR).
attribute(m(X,Y), selected, V) :- menu(X,Y), sudoku(X,Y,V).
element(mi(X,Y,V), dropdownmenuitem, m(X,Y)) :- menu(X,Y), sudoku(X,Y,V).
attribute(mi(X,Y,V), label, V) :- menu(X,Y), sudoku(X,Y,V).
callback(mi(X,Y,V), click, assume(sudoku(X,Y,V))) :- menu(X,Y), sudoku(X,Y,V).

%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

element(m, menubar, window).
element(ms, menubarsection, m).
attribute(ms, label, "Options").
element(ms_clear, menubarsectionitem, ms).
attribute(ms_clear, label, "Clear").
callback(ms_clear, click, clear).
element(ms_next, menubarsectionitem, ms).
attribute(ms_next, label, "Next").
callback(ms_next, click, nextSolution).

%---------------------------------------------------------------------------------------
% Footer Buttons
%---------------------------------------------------------------------------------------

element(buttonsc_c, container, window).
attribute(buttonsc_c, gridcolumn, 0).
attribute(buttonsc_c, gridrow, 1).
attribute(buttonsc_c, height, height_value - grid_height_value).
attribute(buttonsc_c, width, width_value).
attribute(buttonsc_c, backgroundcolor, white).
attribute(buttonsc_c, childorg, absstatic).

element(buttonsc, container, buttonsc_c).
attribute(buttonsc, posx, 200).
attribute(buttonsc, posy, 5).
attribute(buttonsc, height, 300).
attribute(buttonsc, width, 150).
attribute(buttonsc, backgroundcolor, white).
attribute(buttonsc, childorg, grid).

element(clear_container, container, buttonsc).
attribute(clear_container, backgroundcolor, red).
attribute(clear_container, height,45).
attribute(clear_container, width,150).
attribute(clear_container, gridcolumn, 0).
attribute(clear_container, gridrow, 0).

element(clear_label, label, clear_container).
attribute(clear_label, label, "Clear").
attribute(clear_label, backgroundcolor, "#ff4e4e").
attribute(clear_label, onhover, true).
attribute(clear_label, onhoverbackgroundcolor, "#a00000").
attribute(clear_label, onhoverforegroundcolor, "#111111"). 
callback(clear_label, click, clear). 

% attribute(ll, gridcolumn, 0).
% attribute(ll, gridrow, 0).

element(ln, container, buttonsc).
attribute(ln, backgroundcolor, blue).
attribute(ln, gridcolumn, 0).
attribute(ln, gridrow, 1).
attribute(ln, height,45).
attribute(ln, width,150).
callback(ln, click, nextSolution). 

element(next_label, label, ln).
attribute(next_label, label, "Next Solution").
attribute(next_label, backgroundcolor, "#4eff4e").
attribute(next_label, onhover, true).
attribute(next_label, onhoverbackgroundcolor, "#00a000").
attribute(next_label, onhoverforegroundcolor, "#111111"). 
callback(next_label, click, nextSolution). 

element(message, message, window) :- no_more_solutions.
attribute(message, title, "Finished") :- no_more_solutions.
attribute(message, message, "No more solutions available.") :- no_more_solutions.

