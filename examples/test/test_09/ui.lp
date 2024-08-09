elem(window, window, root).
attr(window, height, 400).
attr(window, width, 400).

elem(dpm, dropdown_menu, window).
attr(dpm, selected, V) :- _all(p(V)).

elem(dmp(V), dropdown_menu_item, dpm) :- _any(p(V)).
attr(dmp(V), label, V) :- _any(p(V)).
when(dmp(V), click, callback, add_assumption(p(V),true)) :- _any(p(V)).

elem(l, label, window).
attr(l, label, "Clear assumptions").
attr(l, font_weight, "italic").
attr(l, font_size, 20).
attr(l, background_color, "#ff4d4d").
attr(l, on_hover, "True").
attr(l, on_hover_background_color, "#990000").
when(l, click, callback, clear_assumptions).
