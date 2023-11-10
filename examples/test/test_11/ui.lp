elem(w, window, root).
attr(w, child_layout, flex).

elem(c1, container, w).
attr(c1, background_color, "#ff0000").
attr(c1, width, 500).
attr(c1, flex_direction, "column").

elem(l1, label, c1).
attr(l1, label, "Hallo Welt!").
attr(l1, background_color, "#00ff00").

elem(c2, container, w).
attr(c2, background_color, "#0000ff").
attr(c2, width, 100). % Note that flex will always span the available space, therefore this will be 500
attr(c2, height, 100).
attr(c2, flex_direction, "column").


