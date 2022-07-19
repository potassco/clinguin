
element(window, window, root).

h(500).
w(500).

attribute(window, height, X) :- h(X).
attribute(window, width, X) :- w(X).
attribute(window, backgroundcolor, black).

amount(5).
p(0..(R*R-1)) :- amount(R).

element(c(X), container, window) :- p(X).
attribute(c(X), gridx, X\R) :- p(X), amount(R).
attribute(c(X), gridy, X/R) :- p(X), amount(R).
attribute(c(X), backgroundcolor, gray) :- p(X), X\2 == 1.
attribute(c(X), backgroundcolor, black) :- p(X), X\2 == 0.
attribute(c(X), height, H/R) :- p(X), h(H), amount(R).
attribute(c(X), width, W/R) :- p(X), w(W), amount(R).


amount2(3).
q(X,0..(R*R-1)) :- p(X), amount2(R).

element(c(X,Y), container, c(X)) :- q(X,Y).
attribute(c(X,Y), gridx, Y\R) :- q(X,Y), amount2(R).
attribute(c(X,Y), gridy, Y/R) :- q(X,Y), amount2(R).
attribute(c(X,Y), backgroundcolor, blue) :- q(X,Y), Y\2 == 1, X\2 == 0.
attribute(c(X,Y), backgroundcolor, red) :- q(X,Y), Y\2 == 0, X\2 == 0.
attribute(c(X,Y), backgroundcolor, gray) :- q(X,Y), Y\2 == 1, X\2 == 1.
attribute(c(X,Y), backgroundcolor, white) :- q(X,Y), Y\2 == 0, X\2 == 1.
attribute(c(X,Y), height, H/(R1 * R2)) :- q(X,Y), h(H), amount(R1), amount2(R2).
attribute(c(X,Y), width, W/(R1 * R2)) :- q(X,Y), w(W), amount(R1), amount2(R2).




