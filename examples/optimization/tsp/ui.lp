element(window, window, root).

attribute(window, height, 500) :- h(X).
attribute(window, width, 500) :- w(X).
attribute(window, child_layout, grid).

element(canv, canvas, window).
attribute(canv, image, clingraph__default).
attribute(canv, width, 250).
attribute(canv, height, 250).
attribute(canv, resize, true).

element(c_r_u, container, window).
attribute(c_r_u, grid_column, 1).
attribute(c_r_u, width, 250).
attribute(c_r_u, height, 250).
attribute(c_r_u, background_color, pink).
attribute(c_r_u, child_layout, grid).

element(dma_c, container, c_r_u).
attribute(dma_c, child_layout, grid).
attribute(dma_c, height, 125).
attribute(dma_c, width, 250).

element(dma_l, label, dma_c).
attribute(dma_l, label, "Add").

element(dma, dropdown_menu, dma_c).
attribute(dma, grid_column, 1).

element(dma(V0,V1), dropdown_menu_item, dma) :- _bcd(selected(V0,V1)).
attribute(dma(V0,V1), label, e(V0,V1)) :- _bcd(selected(V0,V1)).
callback(dma(V0,V1), click, add_atom(selected(V0,V1))) :- _bcd(selected(V0,V1)).

element(dmd_c, container, c_r_u).
attribute(dmd_c, grid_row, 1).
attribute(dmd_c, height, 125).
attribute(dmd_c, width, 250).
attribute(dmd_c, child_layout, grid).

element(dmd_l, label, dmd_c).
attribute(dmd_l, label, "Remove").

element(dmd, dropdown_menu, dmd_c).
attribute(dmd, grid_column, 1).

element(dmd(V0,V1), dropdown_menu_item, dmd) :- _atom(selected(V0,V1)).
attribute(dmd(V0,V1), label, e(V0,V1)) :- _atom(selected(V0,V1)).
callback(dmd(V0,V1), click, remove_atom(selected(V0,V1))) :- _atom(selected(V0,V1)).

element(c2, container, window).
attribute(c2, grid_row, 1).
attribute(c2, width, 500).
attribute(c2, height, 250).
attribute(c2, background_color, black).
attribute(c2, grid_column_span, 2).
attribute(c2, child_layout, grid).

element(clear, button, c2).
attribute(clear, label, "Clear").
attribute(clear, height, 125).
attribute(clear, width, 150).
callback(clear, click, clear_atoms).

element(find_min, button, c2).
attribute(find_min, label, "Find Min.").
attribute(find_min, height, 125).
attribute(find_min, width, 150).
callback(find_min, click, find_minimum).
attribute(find_min, grid_row, 1).


element(cur_cost_l, label, c2).
attribute(cur_cost_l, label, "Current Cost:").
attribute(cur_cost_l, height, 120).
attribute(cur_cost_l, width, 350).
attribute(cur_cost_l, grid_row, 0).
attribute(cur_cost_l, grid_column, 1).

element(cur_cost_b, label, c2).
attribute(cur_cost_b, label, C) :- _cautious_cost(C).
attribute(cur_cost_b, height, 120).
attribute(cur_cost_b, width, 350).
attribute(cur_cost_b, grid_column, 1).
attribute(cur_cost_b, grid_row, 1).












