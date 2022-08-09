element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, background_color, white).
attribute(w, child_layout, relstatic).

element(m, menubar, w).

element(ms1, menubarsection, m).
attribute(ms1, label, "File").

element(ms1i1, menubarsectionitem, ms1).
attribute(ms1i1, label, "Open").
element(ms1i2, menubarsectionitem, ms1).
attribute(ms1i2, label, "Close").
callback(ms1i2, click, clear).

element(ms2, menubarsection, m).
element(ms2i2, menubarsectionitem, ms2).

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

element(b, button, c).
attribute(b, background_color, blue).
attribute(b, foreground_color, brown).
attribute(b, label, "Clear!").
attribute(b, on_hover, true).
attribute(b, on_hover_background_color, gray).
attribute(b, on_hover_foreground_color, beige).
attribute(b, font_size, 15).
callback(b, click, clear).

element(c2, container, w).
attribute(c2, width, 180).
attribute(c2, height, 180).
attribute(c2, border_width, 2).
attribute(c2, on_hover, true).
attribute(c2, on_hover_background_color, blue).
attribute(c2, on_hover_border_color, red).
attribute(c2, pos_x, 25).
attribute(c2, pos_y, 50).
attribute(c2, child_layout, grid).

element(c20, container, c2).
attribute(c20, width, 120).
attribute(c20, height, 60).
attribute(c20, background_color, "#fff000000").
attribute(c20, grid_column, 0).
attribute(c20, grid_row, 0).
attribute(c20, grid_column_span, 2).
attribute(c20, grid_row_span, 1).

element(c21, container, c2).
attribute(c21, width, 60).
attribute(c21, height, 120).
attribute(c21, background_color, "#000fff000").
attribute(c21, grid_column, 2).
attribute(c21, grid_row, 0).
attribute(c21, grid_column_span, 1).
attribute(c21, grid_row_span, 2).

element(c22, container, c2).
attribute(c22, width, 60).
attribute(c22, height, 120).
attribute(c22, background_color, "#000000fff").
attribute(c22, grid_column, 0).
attribute(c22, grid_row, 1).
attribute(c22, grid_column_span, 1).
attribute(c22, grid_row_span, 2).

element(c23, container, c2).
attribute(c23, width, 120).
attribute(c23, height, 60).
attribute(c23, background_color, "#999999999").
attribute(c23, grid_column, 1).
attribute(c23, grid_row, 2).
attribute(c23, grid_column_span, 2).
attribute(c23, grid_row_span, 1).

element(c24, container, c2).
attribute(c24, width, 60).
attribute(c24, height, 60).
attribute(c24, background_color, "#000000000").
attribute(c24, grid_column, 1).
attribute(c24, grid_row, 1).
attribute(c24, grid_column_span, 1).
attribute(c24, grid_row_span, 1).












