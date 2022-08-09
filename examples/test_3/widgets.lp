_brave_element_type(dropdownmenuitem).

p(1) :- not p(2).
p(2) :- not p(1).

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

element(m, dropdownmenu, ccc).
attribute(m, background_color, black).
attribute(m, foreground_color, white).
attribute(m, on_hover, true).
attribute(m, on_hover_background_color, white).
attribute(m, on_hover_foreground_color, black).

element(mi(X), dropdownmenuitem, m) :- p(X).
attribute(mi(X), label, X) :- p(X).
callback(mi(X), click, assume(p(X))) :- p(X).
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

t(1..3).
r(1..3).
pos(T,R) :- t(T), r(R).

element(c(X,Y), container, c4) :- pos(X,Y).
attribute(c(X,Y), width, 48) :- pos(X,Y).
attribute(c(X,Y), height, 48) :- pos(X,Y).
attribute(c(X,Y), grid_column, X) :- pos(X,Y).
attribute(c(X,Y), grid_row, Y) :- pos(X,Y).
attribute(c(X,Y), background_color, pink) :- pos(X,Y), (X + Y) \ 2 = 0.
attribute(c(X,Y), background_color, red) :- pos(X,Y), (X + Y) \ 2 = 1.

element(c2, container, w).
attribute(c2, width, 100).
attribute(c2, height, 50).
attribute(c2, border_width, 1).
attribute(c2, border_color, pink).
attribute(c2, background_color, white).
attribute(c2, pos_x, 40).
attribute(c2, pos_y, 50).
attribute(c2, on_hover, true).
attribute(c2, on_hover_background_color, gray).
callback(c2, click, clear).


element(l1, label, c2).
attribute(l1, background_color, blue).
attribute(l1, foreground_color, brown).
attribute(l1, label, "Clear!").
attribute(l1, on_hover, true).
attribute(l1, on_hover_background_color, gray).
attribute(l1, on_hover_foreground_color, beige).
attribute(l1, font_size, 15).
callback(l1, click, clear).

element(c3, container, w).
attribute(c3, width, 100).
attribute(c3, height, 50).
attribute(c3, border_width, 1).
attribute(c3, border_color, pink).
attribute(c3, background_color, white).
attribute(c3, pos_x, 40).
attribute(c3, pos_y, 80).
attribute(c3, on_hover, true).
attribute(c3, on_hover_background_color, gray).
callback(c3, click, clear).

element(b, button, c3).
attribute(b, background_color, blue).
attribute(b, foreground_color, brown).
attribute(b, label, "Clear!").
attribute(b, on_hover, true).
attribute(b, on_hover_background_color, gray).
attribute(b, on_hover_foreground_color, beige).
attribute(b, font_size, 15).
callback(b, click, clear).


