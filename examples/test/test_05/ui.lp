elem(w, window, root).
attr(w, background_color, pink).
attr(w, child_layout, grid).

elem(c2, container, w).
attr(c2, border_width, 3).
attr(c2, background_color, "#707070").
attr(c2, grid_column, 0).

elem(l2, label, c2).
attr(l2, label, "This is a label").

elem(l3, label, c2).
attr(l3, label, "This is another label").

elem(c20, container, c2).
attr(c20, background_color, "#00ffff").
attr(c20, height, 20).
%attr(c20, width, 20).

elem(c3, container, w).
attr(c3, background_color, "#ffff00").
attr(c3, grid_column, 1).

elem(l33, label, c3).
attr(l33, label, "Label 3").
