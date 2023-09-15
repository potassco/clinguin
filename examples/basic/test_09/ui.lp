element(window, window, root).
attribute(window, height, 400).
attribute(window, width, 400).

element(dpm, dropdown_menu, window).
attribute(dpm, selected, V) :- _c(p(V)).

element(dmp(V), dropdown_menu_item, dpm) :- _b(p(V)).
attribute(dmp(V), label, V) :- _b(p(V)).
do(dmp(V), click, callback, add_assumption(p(V))) :- _b(p(V)).

element(l, label, window).
attribute(l, label, "Clear assumptions").
attribute(l, font_weight, "italic").
attribute(l, font_size, 20).
attribute(l, background_color, "#ff4d4d").
attribute(l, on_hover, "True").
attribute(l, on_hover_background_color, "#990000").
do(l, click, callback, clear_assumptions).
