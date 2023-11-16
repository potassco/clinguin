
% Clingraph nodes
node(I) :- ast_node(I, _, _), ast_show(node, I).

elem(window, window, root).
when(window, load, context, (selected_node, X)):- _clinguin_context(selected_node, X).
    
    %%%%%%%%%%%%%%%%%%%%%%%%
    % Edition
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(form, container, window).
    attr(form, class, ("p-3";"bg-secondary";"bg-opacity-50";"rounded")).
    attr(form, order, 1).
    attr(form, width, "500px").
    attr(form, flex_direction, "row-reverse").
    attr(form, class, ("justify-content-end";"m-3")).


        elem(form_label, label, form).
        attr(form_label, label, "Edit node").
        attr(form_label, class, ("px-1";"fw-bold")).

        elem(form_label_node, label, form).
        attr(form_label_node, label, X):-_clinguin_context(selected_node, X).
        attr(form_label_node, class, ("px-2";"fw-bold")).

        elem(show_children, button, form ).
        attr(show_children, class, ("btn-light";"btn-sm";"m-2") ).
        attr(show_children, label, "Show children" ).
        attr(show_children, icon, "fa-eye" ).
        when(show_children, click, call, add_atom(show_children(_context_value(selected_node),true))).

        elem(hide_chidren, button, form ).
        attr(hide_chidren, class, ("btn-light";"btn-sm";"m-2") ).
        attr(hide_chidren, label, "Hide children" ).
        attr(hide_chidren, icon, "fa-eye-slash" ).
        when(hide_chidren, click, call, remove_atom(show_children(_context_value(selected_node),true))).


    %%%%%%%%%%%%%%%%%%%%%%%%
    % Canvas
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(c, canvas, window).
    attr(c, order, 2).
    attr(c, image_type, clingraph_svg).

        %%%%%%%%%%%%%%%%%%%%%%%%
        % Clingraph nodes
        %%%%%%%%%%%%%%%%%%%%%%%%
        elem(n(X), svg_node, c) :- node(X).
        attr(n(X), clingraph_id, X) :- node(X).
        when(n(X), click, context, (selected_node, X)):- node(X).
        when(n(X), click, call, update):- node(X).

%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar
%%%%%%%%%%%%%%%%%%%%%%%%
elem(menu_bar, menu_bar, window).
attr(menu_bar, title, "AST").
attr(menu_bar, icon, "fa-diagram-project").
