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
attribute(window, childorg, absstatic).

element(m, menubar, window).

element(ms, menubarsection, m).
attribute(ms, label, "Options").

element(msi1, menubarsectionitem, ms).
attribute(msi1, label, "Clear").
callback(msi1, click, clear).

element(uc, container, window).
attribute(uc, childorg, grid).
attribute(uc, posx, 50).
attribute(uc, posy, 15).
attribute(uc, height, grid_height_value).
attribute(uc, width, grid_width_value).

c(X,Y) :- pos(X,Y).

element(c(X,Y), container, uc) :- c(X,Y).
attribute(c(X,Y), gridcolumn, X-1) :- c(X,Y).
attribute(c(X,Y), gridrow, Y-1) :- c(X,Y).
% attribute(c(X,Y),backgroundcolor,blue):- c(X,Y).
% attribute(c(X,Y),backgroundcolor,blue):- subgrid(X,Y,S).
attribute(c(X,Y),backgroundcolor,grey):- subgrid(X,Y,S), S\2==0.
attribute(c(X,Y),backgroundcolor,white):- subgrid(X,Y,S), S\2!=0.
attribute(c(X,Y), height, grid_height_value/(dim*dim)) :- c(X,Y).
attribute(c(X,Y), width, grid_width_value/(dim*dim)) :- c(X,Y).

element(m(X,Y), dropdownmenu, c(X,Y)) :- c(X,Y).
_brave(element(mi(X,Y,V), dropdownmenuitem, m(X,Y))) :- sudoku(X,Y,V).

_brave(callback(mi(X,Y,V), click, assume(sudoku(X,Y,V)))) :- sudoku(X,Y,V).
_brave(attribute(mi(X,Y,V), label, V)) :- sudoku(X,Y,V).

attribute(m(X,Y), selected, V) :- sudoku(X,Y,V).

element(lc, container, window).
attribute(lc, height, 70).
attribute(lc, width, 250).
attribute(lc, posx, 150).
attribute(lc, posy, 475).

element(ll, label, lc).
attribute(ll, label, "Clear assumptions").
attribute(ll, backgroundcolor, red).
attribute(ll, onhover, true).
attribute(ll, onhoverbackgroundcolor, blue).
attribute(ll, onhoverforegroundcolor, white). 
callback(ll, click, clear). 


