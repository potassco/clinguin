
element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, background_color, black).

element(m, dropdown_menu, w).
attribute(m, height, 20).
attribute(m, width, 50).
attribute(m, selected, X) :- p(X).

element(mi(X), dropdown_menu_item, m) :- _b(p(X)).
attribute(mi(X), label, X) :- _b(p(X)).
callback(mi(X), click, add_assumption(p(X))) :- _b(p(X)).






