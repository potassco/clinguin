elem(w, window, root).
attr(w, height, 500).
attr(w, width, 500).
attr(w, background_color, white).
attr(w, child_layout, relstatic).

% ---------------- MENU BAR -----------------------------
elem(m, menu_bar, w).

elem(ms1, menu_bar_section, m).
attr(ms1, label, "Test2").

elem(ms1i1, menu_bar_section_item, ms1).
attr(ms1i1, label, "Item X").
elem(ms1i2, menu_bar_section_item, ms1).
attr(ms1i2, label, "Item Y").
when(ms1i2, click, callback, clear_assumptions).

elem(ms2, menu_bar_section, m).
elem(ms2i2, menu_bar_section_item, ms2).

% ------------------- TOP elem(S) ----------------------------------

elem(b, button, w).
attr(b, background_color, blue).
attr(b, foreground_color, brown).
attr(b, label, "Clear!").
attr(b, on_hover, true).
attr(b, on_hover_background_color, gray).
attr(b, on_hover_foreground_color, beige).
attr(b, font_size, 15).

attr(b, pos_x, 25).
attr(b, pos_y, 0).
%attr(b, width, 250).
%attr(b, height, 150).

attr(c, border_width, 2).


when(b, click, callback, clear_assumptions).

% --------------------- BELOW elem(S) --------------------------------------

elem(c2, container, w).
attr(c2, width, 180).
attr(c2, height, 180).
attr(c2, border_width, 2).
attr(c2, on_hover, true).
attr(c2, on_hover_background_color, blue).
attr(c2, on_hover_border_color, red).
attr(c2, pos_x, 25).
attr(c2, pos_y, 50).
attr(c2, child_layout, grid).

elem(c20, container, c2).
attr(c20, width, 120).
attr(c20, height, 60).
attr(c20, background_color, "#ff0000").
attr(c20, grid_column, 0).
attr(c20, grid_row, 0).
attr(c20, grid_column_span, 2).
attr(c20, grid_row_span, 1).

elem(c21, container, c2).
attr(c21, width, 60).
attr(c21, height, 120).
attr(c21, background_color, "#00ff00").
attr(c21, grid_column, 2).
attr(c21, grid_row, 0).
attr(c21, grid_column_span, 1).
attr(c21, grid_row_span, 2).

elem(c22, container, c2).
attr(c22, width, 60).
attr(c22, height, 120).
attr(c22, background_color, "#0000ff").
attr(c22, grid_column, 0).
attr(c22, grid_row, 1).
attr(c22, grid_column_span, 1).
attr(c22, grid_row_span, 2).

elem(c23, container, c2).
attr(c23, width, 120).
attr(c23, height, 60).
attr(c23, background_color, "#999999").
attr(c23, grid_column, 1).
attr(c23, grid_row, 2).
attr(c23, grid_column_span, 2).
attr(c23, grid_row_span, 1).

elem(c24, container, c2).
attr(c24, width, 60).
attr(c24, height, 60).
attr(c24, background_color, "#000000").
attr(c24, grid_column, 1).
attr(c24, grid_row, 1).
attr(c24, grid_column_span, 1).
attr(c24, grid_row_span, 1).












