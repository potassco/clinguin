%%%%%%%%%%%%%%%%%%%%%%%%
% WINDOW
%%%%%%%%%%%%%%%%%%%%%%%%
elem(window, window, root).
attr(window, child_layout, flex).
attr(window, flex_direction, row).


    %%%%%%%%%%%%%%%%%%%%%%%%
    % MODAL
    %%%%%%%%%%%%%%%%%%%%%%%%

    elem(modal, modal, window).
    attr(modal, title, "Add person").

        elem(c1, container, modal).
        attr(c1, child_layout, flex).
        attr(c1, flex_direction, row_reverse).
        attr(c1, class, "align-items-center").

            elem(t1, textfield, c1).
            attr(t1, placeholder, "Enter the name of the person").
            attr(t1, width, 250).
            when(t1, input, context, (t1_content, _value)).

            elem(b1, button, c1).
            when(b1, click, call, (add_atom(person(_context_value(t1_content,str))),
                                    set_external(include(_context_value(t1_content,str)),true))).
            attr(b1, label, "Add").
            attr(b1, class, "m-1").
            attr(b1, class, "btn-secondary").
            attr(b1, icon, "fa-plus").


    %%%%%%%%%%%%%%%%%%%%%%%%
    % PEOPLE INCLUDED
    %%%%%%%%%%%%%%%%%%%%%%%%

    elem(included, container, window).
    attr(included, class, ("bg-secondary";"bg-opacity-50";"w-25";"p-4";"rounded";"d-flex";"flex-column";"justify-content-start")).
    attr(included, order, 1).

        elem(add_button, button, included).
        attr(add_button, icon, "fa-user-plus").
        attr(add_button, order, 1).
        attr(add_button, class, ("btn-secondary";"bg-opacity-50")).
        when(add_button, click, update, (modal, visibility, shown)).

        elem(people, container, included).
        attr(people, order, 2).

            elem(included(P), container, people):- person(P).

                elem(included_cb(P), checkbox, included(P)):- person(P).
                attr(included_cb(P), checked, true):- include(P).
                when(included_cb(P), click, call, set_external(include(P),true)) :- person(P), not include(P).
                when(included_cb(P), click, call, set_external(include(P),false)) :- person(P), include(P).
                attr(included_cb(P), label, P):- person(P).
                attr(included_cb(P), class, ("text-capitalize";"h6";"m-2")):- person(P).


                when(included_btn_add(P), click, call, set_external(include(P),true)) :- person(P), not include(P).
                when(included_btn_add(P), click, call, set_external(include(P),false)) :- person(P), include(P).


    elem(unassigned, collapse, included).
    attr(unassigned, order, 3).
    attr(unassigned, label, "People unassigned").
    attr(unassigned, icon, ("fa-list")).
    % attr(unassigned, collapsed, false).
    % attr(unassigned, expanded_icon, ("fa-home")).
    % attr(unassigned, class, ("text-danger")).
    % attr(unassigned, class, ("disabled")):- #false : person(P), include(P), not _all(assign(_,P)).

    elem(unassigned_content, container, unassigned).
    attr(unassigned_content, class, ("border";"m-1";"p-3";"rounded";"border-dark";"align-items-start")).

    elem(unassigned(P), label, unassigned_content):- person(P), include(P), not _all(assign(_,P)).
    attr(unassigned(P), label, @stringify(P,true)):- person(P), include(P), not _all(assign(_,P)).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Table setup
    %%%%%%%%%%%%%%%%%%%%%%%%


    elem(tables, container, window).
    attr(tables, order, 2).
    attr(tables, class, "w-50").


        elem(table(T), container, tables):-table(T,_).
        attr(table(T), flex_direction, "row"):-table(T,_).
        attr(table(T), class, "border"):-table(T,L).
        attr(table(T), class, "bg-primary"):-table(T,L).
        attr(table(T), class, "bg-opacity-50"):-table(T,L).
        attr(table(T), class, "rounded"):-table(T,L).
        attr(table(T), class, "m-2"):-table(T,L).
        attr(table(T), class, "p-4"):-table(T,L).

            elem(table_label_container(T), container, table(T)):-table(T,_).
            attr(table_label_container(T), order, 1):-table(T,_).
            attr(table_label_container(T), class, "align-self-center"):-table(T,_).

                elem(table_label(T), label, table_label_container(T)):-table(T,_).
                attr(table_label(T), label, L):-table(T,L).
                attr(table_label(T), class, ("font-weight-bold";"h5")):-table(T,L).
                attr(table_label(T), class, "align-middle"):-table(T,L).

            elem(table_dropdowns(T), container, table(T)):-table(T,_).
            attr(table_dropdowns(T), order, 2):-table(T,_).
            attr(table_dropdowns(T), class, "m-2"):-table(T,_).

                elem(table_seat(S,T), dropdown_menu, table_dropdowns(T)):-seat(S,T).
                attr(table_seat(S,T), class, ("btn-primary";"m-1";"btn-sm";"text-capitalize")):-seat(S,T).
                attr(table_seat(S,T), selected, P):- _all(assign(seat(S,T),P)).
                attr(table_seat(S,T), selected, P):- assign(seat(S,T),P), _clinguin_browsing.

                attr(table_seat(S,T), selected, P):- _all_opt(assign(seat(S,T),P)), not _all(assign(seat(S,T),P)).
                attr(table_seat(S,T), class, "text-success"):- _all_opt(assign(seat(S,T),P)), not _all(assign(seat(S,T),P)).
                attr(table_seat(S,T), class, "text-opacity-50"):- _all_opt(assign(seat(S,T),P)), not _all(assign(seat(S,T),P)).

                    elem(table_seat_remove(S,T), dropdown_menu_item, table_seat(S,T)):-seat(S,T).
                    attr(table_seat_remove(S,T), icon, "fa-ban"):-seat(S,T).
                    attr(table_seat_remove(S,T), class, "text-info"):-seat(S,T).
                    when(table_seat_remove(S,T), click, call, remove_assumption_signature(assign(seat(S,T),any))):-seat(S,T).

                    elem(table_seat_p(T,S,P), dropdown_menu_item, table_seat(S,T)):-seat(S,T), person(P).
                    when(table_seat_p(T,S,P), click, call, add_assumption(assign(seat(S,T),P),true)):- seat(S,T), person(P).
                    attr(table_seat_p(T,S,P), class, "text-capitalize"):- seat(S,T), person(P).
                    attr(table_seat_p(T,S,P), label, P):-seat(S,T), person(P).
                    attr(table_seat_p(T,S,P), class,( "text-danger";"disabled")):- not _any(assign(seat(S,T),P)), seat(S,T), person(P).
                    attr(table_seat_p(T,S,P), icon, "fa-face-frown"):- not _any(assign(seat(S,T),P)), seat(S,T), person(P).
                    attr(table_seat_p(T,S,P), class, "text-warning"):- _any(assign(seat(S,T),P)), not _any_opt(assign(seat(S,T),P)).
                    attr(table_seat_p(T,S,P), icon, "fa-face-meh"):- _any(assign(seat(S,T),P)), not _any_opt(assign(seat(S,T),P)).
                    attr(table_seat_p(T,S,P), class, "text-success"):- _any_opt(assign(seat(S,T),P)).
                    attr(table_seat_p(T,S,P), icon, "fa-face-smile"):- _any_opt(assign(seat(S,T),P)).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Menu bar
    %%%%%%%%%%%%%%%%%%%%%%%%

    elem(menu_bar, menu_bar, window).
    attr(menu_bar, title, "Smart placement").
    attr(menu_bar, icon, "fa-utensils").


        elem(menu_bar_restart, button, menu_bar).
        attr(menu_bar_restart, label, "Restart").
        attr(menu_bar_restart, icon, "fa-arrows-rotate").
        attr(menu_bar_restart, class, "btn-outline-danger").
        attr(menu_bar_restart, class, "border-0").
        when(menu_bar_restart, click, call, restart).

        elem(menu_bar_clear, button, menu_bar).
        attr(menu_bar_clear, label, "Clear").
        attr(menu_bar_clear, icon, "fa-trash").
        attr(menu_bar_clear, class, "btn-outline-danger").
        attr(menu_bar_clear, class, "border-0").
        when(menu_bar_clear, click, call, clear_assumptions).


        elem(menu_bar_download, button, menu_bar).
        attr(menu_bar_download, label, "Download").
        attr(menu_bar_download, icon, "fa-download").
        when(menu_bar_download, click, call, download).


        elem(menu_bar_select, button, menu_bar).
        attr(menu_bar_select, label, "Select solution").
        attr(menu_bar_select, icon, "fa-hand-pointer").
        when(menu_bar_select, click, call, select).

        elem(menu_bar_next_opt, button, menu_bar).
        attr(menu_bar_next_opt, label, "Next").
        attr(menu_bar_next_opt, icon, "fa-forward-fast").
        when(menu_bar_next_opt, click, call, next_solution(optN)).

        elem(m, message, window):-_clinguin_optimizing.
        attr(m, title, "Optimality information"):-_clinguin_optimizing.
        attr(m, message, "Optimal!"):- _clinguin_optimizing, _clinguin_optimal.
        attr(m, message, "Optimality not proven"):- _clinguin_optimizing, not _clinguin_optimal.
        attr(m, type, success):- _clinguin_optimizing, _clinguin_optimal.
        attr(m, type, warning):- _clinguin_optimizing, not _clinguin_optimal.
