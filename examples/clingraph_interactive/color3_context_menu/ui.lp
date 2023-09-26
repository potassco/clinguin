elem(window, window, root).
attr(window, child_layout, flex).
attr(window, flex_direction, column).
attr(window, width, 300).

elem(l, label, window).
attr(l, label, "Right click on node to select color!").
attr(l, order, 1).
attr(l, "fontWeight", "bold").
attr(l, "fontSize", "36px").

% A canvas, where images can be displayed.
elem(c, canvas, window).
attr(c, order, 2).

% Specifying a special type from the ''clingraph-backend'' (not yet there).
attr(c, image_type, clingraph_svg).

%%%%%% Clingraph nodes from svg

% Creating nodes in the frontend - for svgs only
elem(n(X), svg_node, c) :- _clingraph(node(X)).
% For interactivity/callbacks it is necessary to specify some sort of id, which (might) differ from the clinguin id.
attr(n(X), id, X) :- _clingraph(node(X)).

%%%%%% Context Menu
elem(context_menu(X), context_menu, window) :- _clingraph(node(X)).
elem(bcm(X,C), button, context_menu(X)) :- _b(assign(X,C)).
attr(bcm(X,C), label, C) :- _b(assign(X,C)).
when(bcm(X,C), click, callback, add_assumption(assign(X,C))) :- _b(assign(X,C)).
when(n(X), right_click, show_context_menu, context_menu(X)):- _clingraph(node(X)).


%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
elem(m, menu_bar, window).
elem(ms, menu_bar_section, m).
attr(m, title,"Interactive 3-Color Example").
attr(ms, label, "Options").
elem(ms_clear, menu_bar_section_item, ms).
attr(ms_clear, label, "Clear").
when(ms_clear, click, call, clear_assumptions).
elem(ms_next, menu_bar_section_item, ms).
attr(ms_next, label, "Next").
when(ms_next, click, call, next_solution).

