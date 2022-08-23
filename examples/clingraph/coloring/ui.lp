element(window, window, root).

attribute(window, height, 50) :- h(X).
attribute(window, width, 50) :- w(X).
attribute(window, child_layout, grid).

element(canvas_c, container, window).
attribute(canvas_c, fit, true).
attribute(canvas_c, background_color, green).

element(canv, canvas, canvas_c).
attribute(canv, image, clingraph__default).
attribute(canv, width, 250).
attribute(canv, height, 250).
attribute(canv, resize, true).


element(bf, container, window).
attribute(bf, background_color, pink).
attribute(bf, grid_row, 1):-node(N).
attribute(bf, child_layout, grid).
attribute(bf, fit, true).


element(node(N), container, bf):-node(N).
attribute(node(N), width, 200):-node(N).
attribute(node(N), height, 30):-node(N).
attribute(node(N), grid_row, N):-node(N).
attribute(node(N), child_layout, grid):-node(N).


element(lc(N), container, node(N)):-node(N).
attribute(lc(N), grid_column, 0):-node(N).
attribute(lc(N), fit, true):-node(N).

element(l(N), label, lc(N)):-node(N).
attribute(l(N), label, N):-node(N).

element(dmc(N), container, node(N)):-node(N).
attribute(dmc(N), grid_column, 1):-node(N).
attribute(dmc(N), width, 100):-node(N).
attribute(dmc(N), height, 30):-node(N).
attribute(dmc(N), fit, false):-node(N).

element(dm(N), dropdown_menu, dmc(N)):-node(N).
attribute(dm(N), selected, C):-assign(N,C).

element(dmi(N,C), dropdown_menu_item, dm(N)):-_b(assign(N,C)).
attribute(dmi(N,C), label, C):-_b(assign(N,C)).
callback(dmi(N,C), click, add_assumption(assign(N,C))):-_b(assign(N,C)).
