element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, background_color, white).
attribute(w, child_layout, relstatic).

element(c, container, w).
attribute(c, width, 250).
attribute(c, height, 150).
attribute(c, border_width, 2).
attribute(c, on_hover, true).
attribute(c, on_hover_background_color, blue).
attribute(c, on_hover_border_color, red).
attribute(c, pos_x, 25).
attribute(c, pos_y, 0).
attribute(c, child_layout, absstatic).

element(cc, container, c).
attribute(cc, width, 100).
attribute(cc, height, 50).
attribute(cc, background_color, green).
attribute(cc, border_width, 2).
attribute(cc, pos_x, 0).
attribute(cc, pos_y, 0).

element(ccc, container, c).
attribute(ccc, width, 100).
attribute(ccc, height, 50).
attribute(ccc, background_color, yellow).
attribute(ccc, border_width, 2).
attribute(ccc, pos_x, 0).
attribute(ccc, pos_y, 50).

element(m, dropdown_menu, ccc).
attribute(m, background_color, black).
attribute(m, foreground_color, white).
attribute(m, on_hover, true).
attribute(m, on_hover_background_color, white).
attribute(m, on_hover_foreground_color, black).

element(mi(X), dropdown_menu_item, m) :- _b(p(X)).
attribute(mi(X), label, X) :- _b(p(X)).
callback(mi(X), click, add_assumption(p(X))) :- _b(p(X)).
attribute(m, selected, X) :- p(X).

element(c4, container, c).
attribute(c4, width, 146).
attribute(c4, height, 146).
attribute(c4, background_color, beige).
attribute(c4, pos_x, 100).
attribute(c4, pos_y, 0).
attribute(c4, child_layout, grid).

% Not implemented due to tkinter
%attribute(c4, padx, 10).
%attribute(c4, pady, 10).

element(c(X,Y), container, c4) :- pos(X,Y).
attribute(c(X,Y), width, 48) :- pos(X,Y).
attribute(c(X,Y), height, 48) :- pos(X,Y).
attribute(c(X,Y), grid_column, X) :- pos(X,Y).
attribute(c(X,Y), grid_row, Y) :- pos(X,Y).
attribute(c(X,Y), background_color, pink) :- pos(X,Y), (X + Y) \ 2 = 0.
attribute(c(X,Y), background_color, red) :- pos(X,Y), (X + Y) \ 2 = 1.

element(l1, label, w).
attribute(l1, background_color, blue).
attribute(l1, foreground_color, brown).
attribute(l1, label, "Clear!").
attribute(l1, on_hover, true).
attribute(l1, on_hover_background_color, gray).
attribute(l1, on_hover_foreground_color, beige).
attribute(l1, font_size, 15).
attribute(l1, width, 100).
attribute(l1, height, 50).
attribute(l1, pos_x, 40).
attribute(l1, pos_y, 50).
callback(l1, click, clear_assumptions).

element(b, button, w).
attribute(b, background_color, blue).
attribute(b, foreground_color, brown).
attribute(b, label, "Clear!").
attribute(b, on_hover, true).
attribute(b, on_hover_background_color, gray).
attribute(b, on_hover_foreground_color, beige).
attribute(b, font_size, 15).
attribute(b, width, 100).
attribute(b, height, 50).
attribute(b, pos_x, 40).
attribute(b, pos_y, 70).

callback(b, click, clear_assumptions).


