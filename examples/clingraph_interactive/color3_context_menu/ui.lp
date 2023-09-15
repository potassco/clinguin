element(window, window, root).
attribute(window, child_layout, flex).
attribute(window, flex_direction, column).
attribute(window, width, 300).

element(l, label, window).
attribute(l, label, "Right click on node to select color!").
attribute(l, order, 1).
attribute(l, "fontWeight", "bold").
attribute(l, "fontSize", "36px").

% A canvas, where images can be displayed.
element(c, canvas, window).
attribute(c, order, 2).

% Specifying a special type from the ''clingraph-backend'' (not yet there).
attribute(c, image_type, clingraph_svg).

%%%%%% Clingraph nodes from svg

% Creating nodes in the frontend - for svgs only
element(n(X), svg_node, c) :- _clingraph(node(X)).
% For interactivity/callbacks it is necessary to specify some sort of id, which (might) differ from the clinguin id.
attribute(n(X), id, X) :- _clingraph(node(X)).

%%%%%% Context Menu
element(context_menu(X), context_menu, window) :- _clingraph(node(X)).
element(bcm(X,C), button, context_menu(X)) :- _b(assign(X,C)).
attribute(bcm(X,C), label, C) :- _b(assign(X,C)).
do(bcm(X,C), click, callback, add_assumption(assign(X,C))) :- _b(assign(X,C)).
do(n(X), right_click, show_context_menu, context_menu(X)):- _clingraph(node(X)).


%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
element(m, menu_bar, window).
element(ms, menu_bar_section, m).
attribute(m, title,"Interactive 3-Color Example").
attribute(ms, label, "Options").
element(ms_clear, menu_bar_section_item, ms).
attribute(ms_clear, label, "Clear").
do(ms_clear, click, call, clear_assumptions).
element(ms_next, menu_bar_section_item, ms).
attribute(ms_next, label, "Next").
do(ms_next, click, call, next_solution).

