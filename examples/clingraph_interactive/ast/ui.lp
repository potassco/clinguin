
element(window, window, root).

h(1000).
w(1000).

attribute(window, height, X) :- h(X).
attribute(window, width, X) :- w(X).
%attribute(window, background_color, black).
attribute(window, resizable_x, 0).
attribute(window, child_layout, grid).

element(cl1, label, window).
attribute(cl1, grid_row, 0).
attribute(cl1, label, "Welcome to the interactive AST viewer!").
attribute(cl1, font_size, 40).
attribute(cl1, "fontWeight", "bold").

element(ci1, clingraph_interactive, window).
attribute(ci1, image, clingraph__default).
attribute(ci1, grid_row, 1).

% ---------------- MENU BAR -----------------------------
element(m, menu_bar, window).

element(ms1, menu_bar_section, m).
attribute(ms1, label, "Overall Actions").

element(ms1i1, menu_bar_section_item, ms1).
attribute(ms1i1, label, "Expand All").
callback(ms1i1, click, "add_atom(show_all)").
element(ms1i2, menu_bar_section_item, ms1).
attribute(ms1i2, label, "Collapse All").
callback(ms1i2, click, "clear_atoms").