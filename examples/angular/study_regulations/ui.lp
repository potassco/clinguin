semester(1..n).

elem(w, window, root).
attr(w, flex_direction, row).

    elem(s(I), container, w):-semester(I).
    attr(s(I), order, I):-semester(I).

    elem(s_t(I), container, s(I)):-semester(I).
    attr(s_t(I), order, 1):-semester(I).
    attr(s_t(I), class, ("bg-primary";"bg-opacity-50";"fw-bold";"p-2";"m-1")):-semester(I).

        elem(s_l(I), label, s_t(I)):-semester(I).
        attr(s_l(I), label, @concat("Semester ",I)):-semester(I).
        attr(s_l(I), order, 1):-semester(I).

        elem(s_dd(I), dropdown_menu, s_t(I)):-semester(I).
        attr(s_dd(I), order, 2):-semester(I).
        attr(s_dd(I), selected, "Assign module"):-semester(I).
        attr(s_dd(I), class, ("btn-sm";"btn-info")):-semester(I).

            elem(s_ddi(I,E), dropdown_menu_item, s_dd(I)):-_any(in(E,s(I))), not _all(in(E,s(I))).
            attr(s_ddi(I,E), label, E):-_any(in(E,s(I))), not _all(in(E,s(I))).
            when(s_ddi(I,E), click, call, add_assumption(in(E,s(I)),true)):-_any(in(E,s(I))), not _all(in(E,s(I))).

    elem(s_modules(I), container, s(I)):-semester(I).
    attr(s_modules(I), class, ("bg-white")):-semester(I).
    attr(s_modules(I), order, 2):-semester(I).

        shown_module(E,I):-_all(in(E,s(I))).
        shown_module(E,I):-in(E,s(I)),_clinguin_browsing.

        elem(s_module(I,E), container, s_modules(I)):-shown_module(E,I).
        attr(s_module(I,E), height, C*10):-shown_module(E,I), map(c,E,C).
        attr(s_module(I,E), class, ("bg-info";"bg-opacity-50";
                                    "d-flex";"flex-row";"justify-content-between";"align-items-center";
                                    "p-2";"m-1")):-shown_module(E,I).

            elem(s_module_l(I,E), label, s_module(I,E)):-shown_module(E,I).
            attr(s_module_l(I,E), label, E):-shown_module(E,I).

            elem(s_module_b(I,E), button, s_module(I,E)):-_clinguin_assume(in(E,s(I)),true).
            attr(s_module_b(I,E), icon, "fa-times"):-_clinguin_assume(in(E,s(I)),true).
            attr(s_module_b(I,E), class, ("btn-sm";"btn-outline")):-_clinguin_assume(in(E,s(I)),true).
            when(s_module_b(I,E), click, call, remove_assumption(in(E,s(I)))):-_clinguin_assume(in(E,s(I)),true).


elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Study Regulations").
attr(menu_bar, icon, "fa-graduation-cap").

elem(menu_bar_next, button, menu_bar).
attr(menu_bar_next, label, "Next").
attr(menu_bar_next, icon, "fa-forward-step").
when(menu_bar_next, click, call, next_solution).


