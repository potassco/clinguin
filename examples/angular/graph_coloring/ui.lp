
elem(window, window, root).

    % ---------
    % Info message
    % ---------
    elem(l, message, window).
    attr(l, message, "Right click on node to select color!").
    attr(l, type, warning).
    attr(l, visible, hidden):- _clinguin_assume(_).

    % ---------
    % Context menu
    % ---------
    elem(context_menu(X), context_menu, window) :- node(X).
        elem(bcm(X,C), button, context_menu(X)) :- color(C), node(X), _b(assign(X,C)).
        attr(bcm(X,C), label, C) :- color(C), node(X).
        % attr(bcm(X,C), class, "disabled") :- color(C), node(X), not _b(assign(X,C)).
        when(bcm(X,C), click, callback, add_assumption(assign(X,C))) :- _b(assign(X,C)).

    % ---------
    % Clingraph image
    % ---------
    elem(c, canvas, window).
    attr(c, order, 2).
    attr(c, image_type, clingraph).

        elem(n(X), svg_node, c) :- node(X).
        attr(n(X), clingraph_id, X) :- node(X).
        when(n(X), right_click, update, (context_menu(X),visibility,visible)):- node(X).

    % ---------
    % Download modal
    % ---------
    elem(modal, modal, window).
    attr(modal, title, "Download").

        elem(c1, container, modal).
        % attr(c1, child_layout, "flex").
        attr(c1, flex_direction, "column").
        attr(c1, class, "align-items-end").

            elem(b1, button, c1).
            when(b1, click, call, download(_context_value_optional(show_download))).
            attr(b1, label, "Download").
            attr(b1, class, "m-1").
            attr(b1, class, "btn-success").
            attr(b1, icon, "fa-download").

            elem(t1, textfield, c1).
            attr(t1, placeholder, "Optinal ASP program with #show statements").
            attr(t1, width, 450).
            when(t1, input, context, (show_download, _value)).


% ---------
% Menu bar
% ---------
elem(menu_bar, menu_bar, window).
attr(menu_bar, title, "Graph coloring").
attr(menu_bar, icon, "fa-diagram-project").

    elem(menu_bar_clear, button, menu_bar).
    attr(menu_bar_clear, label, "Clear").
    attr(menu_bar_clear, icon, "fa-trash").
    attr(menu_bar_clear, class, ("btn-outline-danger";"border-0")).
    when(menu_bar_clear, click, callback, clear_assumptions).

    elem(menu_bar_download, button, menu_bar).
    attr(menu_bar_download, label, "Download").
    attr(menu_bar_download, icon, "fa-download").
    when(menu_bar_download, click, update, (modal, visible, shown)).


    elem(menu_bar_select, button, menu_bar).
    attr(menu_bar_select, label, "Select solution").
    attr(menu_bar_select, icon, "fa-hand-pointer").
    when(menu_bar_select, click, callback, select).

    elem(menu_bar_next, button, menu_bar).
    attr(menu_bar_next, label, "Next").
    attr(menu_bar_next, icon, "fa-forward-step").
    when(menu_bar_next, click, callback, next_solution).
