
elem(w, window, root).
attr(w, background_color, white).
attr(w, child_layout, flex).

elem(c, dropdown_menu, w).
attr(c, width, 100).
attr(c, height, 50).
attr(c, selected, mi(X)) :- _all(p(X)).

elem(mi(X), dropdown_menu_item, c) :- _any(p(X)).
attr(mi(X), label, X) :- _any(p(X)).
when(mi(X), click, callback, add_assumption(p(X),true)) :- _any(p(X)).

elem(c2, container, w).
attr(c2, width, 100).
attr(c2, height, 50).
attr(c2, border_width, 20).
attr(c2, border_color, pink).
attr(c2, background_color, red).




