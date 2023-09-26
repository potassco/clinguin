%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WINDOW
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
element(window, window, root).
attribute(window, child_layout, flex).
attribute(window, flex_direction, row).


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % MODAL
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    element(modal, modal, window).
    attribute(modal, title, "Add person").

        element(c1, container, modal).
        attribute(c1, child_layout, flex).
        attribute(c1, flex_direction, row_reverse).

            element(t1, textfield, c1).
            attribute(t1, placeholder, "Enter the name of the person").
            attribute(t1, width, 250).
            do(t1, input, context, (t1_content, _value)).

            element(b1, button, c1).
            do(b1, click, callback, add_atom(person(_value_context(t1_content)))).
            attribute(b1, label, "Add").
            attribute(b1, class, "m-1").
            attribute(b1, class, "btn-secondary").
            attribute(b1, icon, "fa-plus").


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % ALL PEOPLE
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    element(people, container, window).
    attribute(people, class, "w-25").
    attribute(people, child_layout, "flex").
    attribute(people, flex_direction, "row").

        element(add_button, button, people).
        attribute(add_button, icon, "fa-user-plus").
        attribute(add_button, class, "btn-secondary").
        attribute(add_button, class, "bg-opacity-50").
        attribute(add_button, class, "border-info").
        attribute(add_button, child_layout, flex).
        attribute(add_button, flex_direction, column).
        do(add_button, click, update, (modal, visible, shown)).

        element(list_people, container, people).
        attribute(tables, class, "w-25").
        attribute(tables, order, 1).
        attribute(list_people, class, "rounded").
        attribute(list_people, class, "bg-secondary").
        attribute(list_people, class, "bg-opacity-50").
        attribute(list_people, class, "p-4").
        attribute(list_people, class, "align-items-start").

            element(person_l(P), label, list_people):- person(P).
            attribute(person_l(P), label, P):- person(P).
            attribute(person_l(P), class, "text-capitalize"):- person(P).

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % PEOPLE INCLUDED
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    element(included, container, window).
    attribute(included, class, "bg-info").
    attribute(included, class, "w-25").
    attribute(included, class, "p-4").
    attribute(included, class, "rounded").
    attribute(included, order, 2).
    attribute(included, child_layout, "flex").

        element(included(P), container, included):- person(P).
        attribute(included(P), flex_direction, row):- person(P).
        attribute(included(P), class, "align-items-center"):- person(P).

            element(included_l(P), container, included(P)):- person(P).
            attribute(included_l(P), class, "w-75"):- person(P).
            attribute(included_l(P), flex_direction, row):- person(P).
            
                element(included_btn(P), button, included_l(P)):- person(P).
                attribute(included_btn(P), class, "btn-sm"):- person(P).
                attribute(included_btn(P), class, "rounded-circle"):- person(P).
                attribute(included_btn(P), icon, "fa-circle-check"):- person(P), include(P).
                attribute(included_btn(P), icon, "fa-circle-xmark"):- person(P), not include(P).
                attribute(included_btn(P), class, "text-success"):- person(P), include(P).
                attribute(included_btn(P), class, "text-danger"):- person(P), not include(P).
            
                element(included_label(P), label, included_l(P)):- person(P).
                attribute(included_label(P), label, P):- person(P).
                attribute(included_label(P), class, "text-capitalize"):- person(P).

            element(included_b(P), container, included(P)):- person(P).
            attribute(included_b(P), flex_direction, row):- person(P).


                element(included_btn_add(P), button, included_b(P)):- person(P).
                attribute(included_btn_add(P), class, "btn-sm"):- person(P).
                attribute(included_btn_add(P), class, "btn-outline-dark"):- person(P).
                attribute(included_btn_add(P), class, "m-1"):- person(P).
                attribute(included_btn_add(P), label, "Add"):- person(P), not include(P).
                attribute(included_btn_add(P), label, "Remove"):- person(P), include(P).
                do(included_btn_add(P), click, callback, set_external(include(P),true)) :- person(P), not include(P).
                do(included_btn_add(P), click, callback, set_external(include(P),false)) :- person(P), include(P).



    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Table setup
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    element(tables, container, window).
    attribute(tables, order, 3).
    attribute(tables, class, "w-50").


        element(table(T), container, tables):-table(T,_).
        attribute(table(T), flex_direction, "row"):-table(T,_).
        attribute(table(T), class, "border"):-table(T,L).
        attribute(table(T), class, "bg-primary"):-table(T,L).
        attribute(table(T), class, "bg-opacity-50"):-table(T,L).
        attribute(table(T), class, "rounded"):-table(T,L).
        attribute(table(T), class, "m-2"):-table(T,L).
        attribute(table(T), class, "p-4"):-table(T,L).

            element(table_label_container(T), container, table(T)):-table(T,_).
            attribute(table_label_container(T), order, 1):-table(T,_).
            attribute(table_label_container(T), class, "align-self-center"):-table(T,_).

                element(table_label(T), label, table_label_container(T)):-table(T,_).
                attribute(table_label(T), label, L):-table(T,L).
                attribute(table_label(T), class, "font-weight-bold"):-table(T,L).
                attribute(table_label(T), "font-size", "20px"):-table(T,L).
                attribute(table_label(T), class, "align-middle"):-table(T,L).

            element(table_dropdowns(T), container, table(T)):-table(T,_).
            attribute(table_dropdowns(T), order, 2):-table(T,_).
            attribute(table_dropdowns(T), class, "m-2"):-table(T,_).

                element(table_seat(S,T), dropdown_menu, table_dropdowns(T)):-seat(S,T).
                attribute(table_seat(S,T), class, "btn-sm"):-seat(S,T).
                attribute(table_seat(S,T), class, "btn-primary"):-seat(S,T).
                attribute(table_seat(S,T), class, "m-1"):-seat(S,T).
                attribute(table_seat(S,T), selected, P):- _c(assign(seat(S,T),P)).
                attribute(table_seat(S,T), selected, P):- assign(seat(S,T),P), _clinguin_browsing.

                    element(table_seat_remove(S,T), dropdown_menu_item, table_seat(S,T)):-seat(S,T).
                    attribute(table_seat_remove(S,T), icon, "fa-ban"):-seat(S,T).
                    attribute(table_seat_remove(S,T), class, "text-info"):-seat(S,T).
                    do(table_seat_remove(S,T), click, callback, remove_assumption_signature(assign(seat(S,T),any))):-seat(S,T).

                    element(table_seat_p(T,S,P), dropdown_menu_item, table_seat(S,T)):-_b(assign(seat(S,T),P)).
                    attribute(table_seat_p(T,S,P), label, P):-_b(assign(seat(S,T),P)).
                    attribute(table_seat_p(T,S,P), class, "text-capitalize"):- _b(assign(seat(S,T),P)).
                    do(table_seat_p(T,S,P), click, callback, add_assumption(assign(seat(S,T),P))):- _b(assign(seat(S,T),P)).

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Menu bar
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    element(menu_bar, menu_bar, window).
    attribute(menu_bar, title, "Smart placement").
    attribute(menu_bar, icon, "fa-utensils").

        element(menu_bar_clear, button, menu_bar).
        attribute(menu_bar_clear, label, "Clear").
        attribute(menu_bar_clear, icon, "fa-trash").
        attribute(menu_bar_clear, class, "btn-outline-danger").
        attribute(menu_bar_clear, class, "border-0").
        do(menu_bar_clear, click, callback, clear_assumptions).


        element(menu_bar_select, button, menu_bar).
        attribute(menu_bar_select, label, "Select solution").
        attribute(menu_bar_select, class, "btn-outline-dark").
        attribute(menu_bar_select, class, "border-0").
        attribute(menu_bar_select, icon, "fa-hand-pointer").
        do(menu_bar_select, click, callback, select).

        element(menu_bar_next_opt, button, menu_bar).
        attribute(menu_bar_next_opt, label, "Next Optimal").
        attribute(menu_bar_next_opt, icon, "fa-forward-fast").
        attribute(menu_bar_next_opt, class, "btn-outline-dark").
        attribute(menu_bar_next_opt, class, "border-0").
        do(menu_bar_next_opt, click, callback, next_solution(optN)).

        element(menu_bar_next, button, menu_bar).
        attribute(menu_bar_next, label, "Next").
        attribute(menu_bar_next, icon, "fa-forward-step").
        attribute(menu_bar_next, class, "btn-outline-dark").
        attribute(menu_bar_next, class, "border-0").
        do(menu_bar_next, click, callback, next_solution).
