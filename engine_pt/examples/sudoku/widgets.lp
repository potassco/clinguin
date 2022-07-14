element(window, window, root).

h(500).
w(500).

attribute(window, height, X) :- h(X).
attribute(window, width, X) :- w(X).
attribute(window, backgroundcolor, white).

c(X-1,Y-1) :- pos(X,Y).
initial2(X-1,Y-1,V) :- initial(X,Y,V).
sudoku2(X-1,Y-1,V) :- sudoku(X,Y,V).

element(c(X,Y), container, window) :- c(X,Y).
attribute(c(X,Y), gridx, X) :- c(X,Y).
attribute(c(X,Y), gridy, Y) :- c(X,Y).
attribute(c(X,Y), backgroundcolor, blue) :- c(X,Y), ((X/3) + (Y/3))\2 == 0, (X+Y)\2 == 0.
attribute(c(X,Y), backgroundcolor, red) :- c(X,Y), ((X/3) + (Y/3))\2 == 0, (X+Y)\2 == 1.
attribute(c(X,Y), backgroundcolor, gray) :- c(X,Y), ((X/3) + (Y/3))\2 == 1, (X+Y)\2 == 0.
attribute(c(X,Y), backgroundcolor, white) :- c(X,Y), ((X/3) + (Y/3))\2 == 1, (X+Y)\2 == 1.
attribute(c(X,Y), height, H/(dim*dim)) :- c(X,Y), h(H).
attribute(c(X,Y), width, W/(dim*dim)) :- c(X,Y), w(W).

element(m(X,Y), dropdownmenu, c(X,Y)) :- c(X,Y).
%element(mi(X,Y,V), dropdownmenuitem, m(X,Y)) :- initial2(X,Y,V).
element(mi(X,Y,V), dropdownmenuitem, m(X,Y)) :- sudoku2(X,Y,V).

callback(mi(X,Y,V), click, assume(sudoku(X+1,Y+1,V))) :- sudoku2(X,Y,V).

attribute(m(X,Y), selected, V) :- sudoku2(X,Y,V).
attribute(mi(X,Y,V), label, V) :- sudoku2(X,Y,V).




