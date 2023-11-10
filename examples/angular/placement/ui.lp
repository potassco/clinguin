%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WINDOW
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
elem(window, window, root).
attr(window, child_layout, flex).
attr(window, flex_direction, row).


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % MODAL
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
            when(b1, click, call, (add_atom(person(_context_value(t1_content))),
                                    set_external(include(_context_value(t1_content)),true))).
            attr(b1, label, "Add").
            attr(b1, class, "m-1").
            attr(b1, class, "btn-secondary").
            attr(b1, icon, "fa-plus").


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % ALL PEOPLE
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    elem(people, container, window).
    attr(people, class, "w-25").
    attr(people, child_layout, "flex").
    attr(people, flex_direction, "row").

        elem(add_button, button, people).
        attr(add_button, icon, "fa-user-plus").
        attr(add_button, class, "btn-secondary").
        attr(add_button, class, "bg-opacity-50").
        attr(add_button, class, "border-info").
        attr(add_button, child_layout, flex).
        attr(add_button, flex_direction, column).
        when(add_button, click, update, (modal, visible, shown)).

        elem(list_people, container, people).
        attr(tables, class, "w-25").
        attr(tables, order, 1).
        attr(list_people, class, "rounded").
        attr(list_people, class, "bg-secondary").
        attr(list_people, class, "bg-opacity-50").
        attr(list_people, class, "p-4").
        attr(list_people, class, "align-items-start").

            elem(person_l(P), label, list_people):- person(P).
            attr(person_l(P), label, P):- person(P).
            attr(person_l(P), class, "text-capitalize"):- person(P).

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % PEOPLE INCLUDED
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    elem(included, container, window).
    attr(included, class, "bg-info").
    attr(included, class, "w-25").
    attr(included, class, "p-4").
    attr(included, class, "rounded").
    attr(included, order, 2).
    attr(included, child_layout, "flex").

        elem(included(P), container, included):- person(P).
        attr(included(P), flex_direction, row):- person(P).
        attr(included(P), class, "align-items-center"):- person(P).

            elem(included_l(P), container, included(P)):- person(P).
            attr(included_l(P), class, "w-75"):- person(P).
            attr(included_l(P), flex_direction, row):- person(P).
            
                elem(included_btn(P), button, included_l(P)):- person(P).
                attr(included_btn(P), class, "btn-sm"):- person(P).
                attr(included_btn(P), class, "rounded-circle"):- person(P).
                attr(included_btn(P), icon, "fa-circle-check"):- person(P), include(P).
                attr(included_btn(P), icon, "fa-circle-xmark"):- person(P), not include(P).
                attr(included_btn(P), class, "text-success"):- person(P), include(P).
                attr(included_btn(P), class, "text-danger"):- person(P), not include(P).
            
                elem(included_label(P), label, included_l(P)):- person(P).
                attr(included_label(P), label, P):- person(P).
                attr(included_label(P), class, "text-capitalize"):- person(P).

            elem(included_b(P), container, included(P)):- person(P).
            attr(included_b(P), flex_direction, row):- person(P).


                elem(included_btn_add(P), button, included_b(P)):- person(P).
                attr(included_btn_add(P), class, "btn-sm"):- person(P).
                attr(included_btn_add(P), class, "btn-outline-dark"):- person(P).
                attr(included_btn_add(P), class, "m-1"):- person(P).
                attr(included_btn_add(P), label, "Add"):- person(P), not include(P).
                attr(included_btn_add(P), label, "Remove"):- person(P), include(P).
                when(included_btn_add(P), click, call, set_external(include(P),true)) :- person(P), not include(P).
                when(included_btn_add(P), click, call, set_external(include(P),false)) :- person(P), include(P).



    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Table setup
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    elem(tables, container, window).
    attr(tables, order, 3).
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
                attr(table_label(T), class, "font-weight-bold"):-table(T,L).
                attr(table_label(T), "font-size", "20px"):-table(T,L).
                attr(table_label(T), class, "align-middle"):-table(T,L).

            elem(table_dropdowns(T), container, table(T)):-table(T,_).
            attr(table_dropdowns(T), order, 2):-table(T,_).
            attr(table_dropdowns(T), class, "m-2"):-table(T,_).

                elem(table_seat(S,T), dropdown_menu, table_dropdowns(T)):-seat(S,T).
                attr(table_seat(S,T), class, "btn-sm"):-seat(S,T).
                attr(table_seat(S,T), class, "btn-primary"):-seat(S,T).
                attr(table_seat(S,T), class, "m-1"):-seat(S,T).
                attr(table_seat(S,T), selected, P):- _c(assign(seat(S,T),P)).
                attr(table_seat(S,T), selected, P):- assign(seat(S,T),P), _clinguin_browsing.

                    elem(table_seat_remove(S,T), dropdown_menu_item, table_seat(S,T)):-seat(S,T).
                    attr(table_seat_remove(S,T), icon, "fa-ban"):-seat(S,T).
                    attr(table_seat_remove(S,T), class, "text-info"):-seat(S,T).
                    when(table_seat_remove(S,T), click, call, remove_assumption_signature(assign(seat(S,T),any))):-seat(S,T).

                    elem(table_seat_p(T,S,P), dropdown_menu_item, table_seat(S,T)):-_b(assign(seat(S,T),P)).
                    attr(table_seat_p(T,S,P), label, P):-_b(assign(seat(S,T),P)).
                    attr(table_seat_p(T,S,P), class, "text-capitalize"):- _b(assign(seat(S,T),P)).
                    when(table_seat_p(T,S,P), click, call, add_assumption(assign(seat(S,T),P))):- _b(assign(seat(S,T),P)).

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Menu bar
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
        attr(menu_bar_next_opt, label, "Next Optimal").
        attr(menu_bar_next_opt, icon, "fa-forward-fast").
        when(menu_bar_next_opt, click, call, next_solution(optN)).

        elem(menu_bar_next, button, menu_bar).
        attr(menu_bar_next, label, "Next").
        attr(menu_bar_next, icon, "fa-forward-step").
        when(menu_bar_next, click, call, next_solution).
