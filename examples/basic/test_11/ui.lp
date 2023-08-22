element(w, window, root).
attribute(w, child_layout, flex).

element(c1, container, w).
attribute(c1, background_color, "#ff0000").
attribute(c1, width, 500).
attribute(c1, flex_direction, "column").

element(l1, label, c1).
attribute(l1, label, "Hallo Welt!").
attribute(l1, background_color, "#00ff00").

element(c2, container, w).
attribute(c2, background_color, "#0000ff").
attribute(c2, width, 100). % Note that flex will always span the available space, therefore this will be 500
attribute(c2, height, 100).
attribute(c2, flex_direction, "column").


