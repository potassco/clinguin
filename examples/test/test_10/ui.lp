elem(w, window, root).
attr(w, height, 800).
attr(w, width, 600).
attr(w, child_layout, flex).

elem(c1, container, w).
attr(c1, background_color, "#ff0000").
attr(c1, width, 200).
attr(c1, height, 200).
attr(c1, flex_direction, "row_reverse").

elem(c2, container, w).
attr(c2, background_color, "#0000ff").
attr(c2, width, 200).
attr(c2, height, 200).
attr(c2, flex_direction, "row_reverse").

elem(c3, container, w).
attr(c3, background_color, "#00ff00").
attr(c3, width, 200).
attr(c3, height, 200).
attr(c3, flex_direction, "row_reverse").

elem(c4, container, w).
attr(c4, background_color, "#ffff00").
attr(c4, width, 200).
attr(c4, height, 200).
attr(c4, flex_direction, "column").

elem(c5, container, w).
attr(c5, background_color, "#00ffff").
attr(c5, width, 200).
attr(c5, height, 200).
attr(c5, flex_direction, "column").

elem(c6, container, w).
attr(c6, background_color, "#ff00ff").
attr(c6, width, 200).
attr(c6, height, 200).
attr(c6, flex_direction, "column_reverse").



