element(window, window, root).

#const height_value= 500.
#const width_value= 500.

attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, backgroundcolor, white).
attribute(window, resizablex, 0).
attribute(window, resizabley, 0).

c(X,Y) :- pos(X,Y).

element(c(X,Y), container, window) :- c(X,Y).
attribute(c(X,Y), gridx, X-1) :- c(X,Y).
attribute(c(X,Y), gridy, Y-1) :- c(X,Y).
% attribute(c(X,Y),backgroundcolor,blue):- c(X,Y).
% attribute(c(X,Y),backgroundcolor,blue):- subgrid(X,Y,S).
attribute(c(X,Y),backgroundcolor,grey):- subgrid(X,Y,S), S\2==0.
attribute(c(X,Y),backgroundcolor,white):- subgrid(X,Y,S), S\2!=0.
attribute(c(X,Y), height, height_value/(dim*dim)) :- c(X,Y).
attribute(c(X,Y), width, width_value/(dim*dim)) :- c(X,Y).

element(m(X,Y), dropdownmenu, c(X,Y)) :- c(X,Y).
element(mi(X,Y,V), dropdownmenuitem, m(X,Y)) :- sudoku(X,Y,V).

callback(mi(X,Y,V), click, assume(sudoku(X,Y,V))) :- sudoku(X,Y,V).

attribute(m(X,Y), selected, V) :- sudoku(X,Y,V).
attribute(mi(X,Y,V), label, V) :- sudoku(X,Y,V).




