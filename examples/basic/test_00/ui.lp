
elem(window, window, root).

h(500).
w(500).

attr(window, height, X) :- h(X).
attr(window, width, X) :- w(X).
attr(window, background_color, black).
attr(window, resizable_x, 0).
attr(window, child_layout, grid).

amount(5).
p(0..(R*R-1)) :- amount(R).

elem(c(X), container, window) :- p(X).
attr(c(X), grid_column, X\R) :- p(X), amount(R).
attr(c(X), grid_row, X/R) :- p(X), amount(R).
attr(c(X), background_color, gray) :- p(X), X\2 == 1.
attr(c(X), background_color, black) :- p(X), X\2 == 0.
attr(c(X), height, H/R) :- p(X), h(H), amount(R).
attr(c(X), width, W/R) :- p(X), w(W), amount(R).
attr(c(X), child_layout, grid) :- p(X).


amount2(3).
q(X,0..(R*R-1)) :- p(X), amount2(R).

elem(c(X,Y), container, c(X)) :- q(X,Y).
attr(c(X,Y), grid_column, Y\R) :- q(X,Y), amount2(R).
attr(c(X,Y), grid_row, Y/R) :- q(X,Y), amount2(R).
attr(c(X,Y), background_color, blue) :- q(X,Y), Y\2 == 1, X\2 == 0.
attr(c(X,Y), background_color, red) :- q(X,Y), Y\2 == 0, X\2 == 0.
attr(c(X,Y), background_color, gray) :- q(X,Y), Y\2 == 1, X\2 == 1.
attr(c(X,Y), background_color, white) :- q(X,Y), Y\2 == 0, X\2 == 1.
attr(c(X,Y), height, H/(R1 * R2)) :- q(X,Y), h(H), amount(R1), amount2(R2).
attr(c(X,Y), width, W/(R1 * R2)) :- q(X,Y), w(W), amount(R1), amount2(R2).



