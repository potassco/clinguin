
_brave_element_type(dropdownmenuitem).

element(window, window, root).
#const height_value= 550.
#const width_value= 550.
#const grid_height_value = 450.
#const grid_width_value = 450.

attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, backgroundcolor, white).
attribute(window, resizablex, 0).
attribute(window, resizabley, 0).
attribute(window, childorg, grid).

element(uc, container, window).
attribute(uc, gridcolumn, 0).
attribute(uc, gridrow, 0).
attribute(uc, height, grid_height_value).
attribute(uc, width, grid_width_value).
attribute(uc, childorg, grid).

% Menu bar
element(m, menubar, window).
element(ms, menubarsection, m).
attribute(ms, label, "Options").
element(ms_clear, menubarsectionitem, ms).
attribute(ms_clear, label, "Clear").
callback(ms_clear, click, clear).
element(ms_next, menubarsectionitem, ms).
attribute(ms_next, label, "Next").
callback(ms_next, click, nextSolution).

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

% Container for the buttons
element(buttonsc, container, window).
attribute(buttonsc, gridcolumn, 0).
attribute(buttonsc, gridrow, 1).
attribute(buttonsc, height, height_value- grid_height_value).
attribute(buttonsc, width, width_value).
attribute(buttonsc, childorg, grid).

% element(lc, container, window).
% attribute(lc, height, 70).
% attribute(lc, width, 250).
% % attribute(lc, posx, 150).
% % attribute(lc, posy, 475).
% attribute(lc, gridcolumn, 0).
% attribute(lc, gridrow, 1).
% attribute(lc, childorg, grid).

element(ll, label, buttonsc).
attribute(ll, label, "Clear").
attribute(ll, backgroundcolor, red).
% attribute(ll, onhover, true).
% attribute(ll, onhoverbackgroundcolor, blue).
% attribute(ll, onhoverforegroundcolor, white). 
callback(ll, click, clear). 
% attribute(ll, gridcolumn, 0).
% attribute(ll, gridrow, 0).
attribute(ll,height,3).
attribute(ll,width,20).

element(ln, label, buttonsc).
attribute(ln, label, "Next Solution").
attribute(ln, backgroundcolor, green).
callback(ln, click, nextSolution). 
% attribute(ln, gridcolumn, 1).
% attribute(ln, gridrow, 0).
attribute(ln,height,3).
attribute(ln, width,20).

% TODO adding this crashes after selecting an option on the grid?
element(message, message, window) :- no_more_solutions.
attribute(message, title, "Holi") :- no_more_solutions.
attribute(message, message, "ayuda") :- no_more_solutions.

% % #script (python)
% % from clingo import parse_term
% % def main(ctl):

% %     ctl.ground([("base", [])])
% %     ctl.assign_external(parse_term('show_all'),True)
% %     ctl.solve()


% % #end.
