%---------------------------------------------------------------------------------------
% Window
%---------------------------------------------------------------------------------------

element(window, window, root).
attribute(window, child_layout, grid).

%---------------------------------------------------------------------------------------
% Clingraph image
%---------------------------------------------------------------------------------------

element(canv, canvas, window).
attribute(canv, image, clingraph__default).
attribute(canv, width, 250).
attribute(canv, height, 250).
attribute(canv, resize, true).

%---------------------------------------------------------------------------------------
% Color selectors
%---------------------------------------------------------------------------------------

element(node(N), container, window):-node(N).
attribute(node(N), width, 200):-node(N).
attribute(node(N), height, 30):-node(N).
attribute(node(N), grid_row, N):-node(N).
attribute(node(N), child_layout, grid):-node(N).

% Node label
element(l(N), label, node(N)):-node(N).
attribute(l(N), grid_column, 0):-node(N).
attribute(l(N), label, N):-node(N).

% Node dropdown
element(dmc(N), dropdown_menu, node(N)):-node(N).
attribute(dmc(N), grid_column, 1):-node(N).
attribute(dmc(N), width, 100):-node(N).
attribute(dmc(N), height, 30):-node(N).
attribute(dmc(N), selected, C):-assign(N,C), clinguin_browsing.
attribute(dmc(N), selected, C):-_c(assign(N,C)).
callback(dmc(N), clear, remove_assumption_signature(assign(N,any))) :- node(N).

% Node dropdown item
element(dmi(N,C), dropdown_menu_item, dmc(N)):-_b(assign(N,C)).
attribute(dmi(N,C), label, C):-_b(assign(N,C)).
callback(dmi(N,C), click, add_assumption(assign(N,C))):-_b(assign(N,C)).

