
% Clingraph nodes
node(X) :- group(X).
edge((X,Y)) :- parent(X,Y).

elem(window, window, root).
when(window, load, update, (n(X),opacity,"0.5")):-node(X).
when(window, load, update, (n(X),visibility,"hidden")):-node(X),not root(X),not _clinguin_context(X,open).
when(window, load, update, (e((X,Y)),visibility,"hidden")):-edge((X,Y)), not _clinguin_context(Y,open).
when(window, load, context, (X,open)):- _clinguin_context(X,open).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Info messages
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(l2, message, window).
    attr(l2, message, "Right click on node to add children").
    attr(l2, type, info).
    attr(l2, visible, hidden):- _clinguin_context(_,_).

    elem(l1, message, window).
    attr(l1, message, "Click on blue node to expland children").
    attr(l1, type, info).
    attr(l1, visible, hidden):- _clinguin_context(_,_).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % MODAL
    %%%%%%%%%%%%%%%%%%%%%%%%

    elem(modal, modal, window).
    attr(modal, title, "Add children").

        elem(c1, container, modal).
        attr(c1, child_layout, flex).
        attr(c1, flex_direction, row_reverse).
        attr(c1, class, "align-items-center").


            elem(b1, button, c1).
            when(b1, click, context, (_context_value(t1_content),open)).
            when(b1, click, call, (add_atom(parent(_context_value(selected_node),_context_value(t1_content))))).
            attr(b1, label, "Add").
            attr(b1, class, "m-1").
            attr(b1, class, "btn-sm").
            attr(b1, class, "btn-primary").
            attr(b1, icon, "fa-plus").

            elem(t1, textfield, c1).
            attr(t1, placeholder, "Group name").
            attr(t1, width, 250).
            when(t1, input, context, (t1_content, _value)).
        

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Context menu
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(context_menu(X), context_menu, window) :- node(X).
        elem(bcm(X), button, context_menu(X)) :- node(X).
        attr(bcm(X), label, "Add children") :- node(X).
        when(bcm(X), click, update, (modal,visible, shown)) :- node(X).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Canvas
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(c, canvas, window).
    attr(c, order, 2).
    attr(c, width, 200).
    attr(c, image_type, clingraph_svg).
        
        elem(e(E), svg_edge, c) :- edge(E).
        attr(e(E), clingraph_id, E) :- edge(E).

        elem(n(X), svg_node, c) :- node(X).
        attr(n(X), clingraph_id, X) :- node(X).
        when(n(X), right_click, context, (selected_node, X)):- node(X).
        when(n(X), right_click, update, (context_menu(X),visibility,visible)):- node(X).
        when(n(X), click, context, (selected_node, X)):- node(X).
        when(n(X), click, context, (Y, open)):- node(X), edge((X,Y)).
        when(n(X), click, update, (n(Y), visibility, visible)):- edge((X,Y)).
        when(n(X), click, update, (e((X,Y)), visibility, visible)):- edge((X,Y)).
        when(n(X), mouseenter, update, (n(X), opacity, "1")):- node(X).
        when(n(X), mouseleave, update, (n(X), opacity, "0.5")):- node(X).



    %%%%%%%%%%%%%%%%%%%%%%%%
    % Menu bar
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(menu_bar, menu_bar, window).
    attr(menu_bar, title, "Taxonomy tree").
    attr(menu_bar, icon, "fa-diagram-project").

        elem(menu_bar_download, button, menu_bar).
        attr(menu_bar_download, label, "Save").
        attr(menu_bar_download, icon, "fa-save").
        when(menu_bar_download, click, call, download("#show parent/2. #show root/1.","examples/angular/tree_browser/instance.lp")).