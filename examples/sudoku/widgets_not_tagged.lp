element(window, window, root).

#const height_value= 550.
#const width_value= 550.

#const grid_height_value = 450.
#const grid_width_value = 450.

attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, background_color, white).
attribute(window, resizable_x, 0).
attribute(window, resizable_y, 0).
attribute(window, child_layout, absstatic).

element(m, menubar, window).

element(ms, menubarsection, m).
attribute(ms, label, "Options").

element(msi1, menubarsectionitem, ms).
attribute(msi1, label, "Clear").
callback(msi1, click, clear).

element(uc, container, window).
attribute(uc, child_layout, grid).
attribute(uc, pos_x, 50).
attribute(uc, pos_y, 15).
attribute(uc, height, grid_height_value).
attribute(uc, width, grid_width_value).

c(X,Y) :- pos(X,Y).

element(c(X,Y), container, uc) :- c(X,Y).
attribute(c(X,Y), grid_column, X-1) :- c(X,Y).
attribute(c(X,Y), grid_row, Y-1) :- c(X,Y).
% attribute(c(X,Y),background_color,blue):- c(X,Y).
% attribute(c(X,Y),background_color,blue):- subgrid(X,Y,S).
attribute(c(X,Y),background_color,grey):- subgrid(X,Y,S), S\2==0.
attribute(c(X,Y),background_color,white):- subgrid(X,Y,S), S\2!=0.
attribute(c(X,Y), height, grid_height_value/(dim*dim)) :- c(X,Y).
attribute(c(X,Y), width, grid_width_value/(dim*dim)) :- c(X,Y).

element(m(X,Y), dropdownmenu, c(X,Y)) :- c(X,Y).
element(mi(X,Y,V), dropdownmenuitem, m(X,Y)) :- sudoku(X,Y,V).

callback(mi(X,Y,V), click, assume(sudoku(X,Y,V))) :- sudoku(X,Y,V).

attribute(m(X,Y), selected, V) :- sudoku(X,Y,V).
attribute(mi(X,Y,V), label, V) :- sudoku(X,Y,V).

element(lc, container, window).
attribute(lc, height, 70).
attribute(lc, width, 250).
attribute(lc, pos_x, 150).
attribute(lc, pos_y, 475).

element(ll, label, lc).
attribute(ll, label, "Clear assumptions").
attribute(ll, background_color, red).
attribute(ll, on_hover, true).
attribute(ll, on_hover_background_color, blue).
attribute(ll, on_hover_foreground_color, white). 
callback(ll, click, clear). 


