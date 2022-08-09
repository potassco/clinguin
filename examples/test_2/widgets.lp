_brave_element_type(dropdown_menu_item).

p(1) :- not p(2).
p(2) :- not p(1).

element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, background_color, black).

element(m, dropdown_menu, w).
attribute(m, height, 20).
attribute(m, width, 50).
attribute(m, selected, X) :- p(X).

element(mi(X), dropdown_menu_item, m) :- p(X).
attribute(mi(X), label, X) :- p(X).
callback(mi(X), click, assume(p(X))) :- p(X).






