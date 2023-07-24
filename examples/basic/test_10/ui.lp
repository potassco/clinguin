
element(window, window, root).

attribute(window, background_color, black).
attribute(window, resizable_x, 0).
attribute(window, child_layout, flex).

p(1).

element(c(X), container, window) :- p(X).
attribute(c(X), background_color, "#00ff00") :- p(X).
attribute(c(X), child_layout, flex) :- p(X).

element(mbutton(X), label, c(X)) :- p(X).
attribute(mbutton(X), label, "TEST 1\n Hello Potsdam") :- p(X).
attribute(mbutton(X), grid_column, 1):- p(X).
attribute(mbutton(X), foreground_color, red):- p(X).
%attribute(mbutton(X), width, 300) :- p(X).
%attribute(mbutton(X), height, 300) :- p(X).


