
elem(window, window, root).

attr(window, background_color, black).
attr(window, resizable_x, 0).
attr(window, child_layout, flex).

elem(c(X), container, window) :- p(X).
attr(c(X), background_color, "#00ff00") :- p(X).
attr(c(X), child_layout, flex) :- p(X).

elem(mbutton(X), label, c(X)) :- q(X).
attr(mbutton(X), label, "TEST 02\n Hello Potsdam") :- q(X).
attr(mbutton(X), foreground_color, red):- q(X).
