
element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, background_color, white).

element(c, dropdown_menu, w).
attribute(c, width, 100).
attribute(c, height, 50).

attribute(c, on_hover, true).
attribute(c, on_hover_background_color, blue).

attribute(c, selected, mi(X)) :- _b(p(X)).

element(mi(X), dropdown_menu_item, c) :- _b(p(X)).
attribute(mi(X), label, X) :- _b(p(X)).
callback(mi(X), click, add_assumption(p(X))) :- _b(p(X)).

element(c2, container, w).
attribute(c2, width, 100).
attribute(c2, height, 50).
attribute(c2, border_width, 20).
attribute(c2, border_color, pink).
attribute(c2, background_color, red).




