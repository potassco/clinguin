element(w, window, root).
attribute(w, background_color, pink).
attribute(w, child_layout, grid).

element(c2, container, w).
attribute(c2, border_width, 3).
attribute(c2, background_color, "#0f0f0f").
attribute(c2, grid_column, 0).

element(l2, label, c2).
attribute(l2, label, "This is a label").

element(l3, label, c2).
attribute(l3, label, "This is another label").

element(c20, container, c2).
attribute(c20, background_color, "#00ffff").
attribute(c20, height, 20).
attribute(c20, width, 20).

element(c3, container, w).
attribute(c3, background_color, "#ffff00").
attribute(c3, grid_column, 1).

element(l33, label, c3).
attribute(l33, label, "Label 3").
