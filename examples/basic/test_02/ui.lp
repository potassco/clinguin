
element(window, window, root).

attribute(window, background_color, black).
attribute(window, resizable_x, 0).
attribute(window, child_layout, flex).

element(c(X), container, window) :- p(X).
attribute(c(X), background_color, "#00ff00") :- p(X).
attribute(c(X), child_layout, flex) :- p(X).

element(mbutton(X), label, c(X)) :- q(X).
attribute(mbutton(X), label, "TEST 02\n Hello Potsdam") :- q(X).
attribute(mbutton(X), foreground_color, red):- q(X).
