

elem(w, window, root).

elem(row(P), container, w):- person(P).
attr(row(P), class, ("d-flex";"flex-row";"align-items-center";"m-3";"p-2";"shadow")):- person(P).
attr(row(P), order, @to_int(P)):- person(P).

    elem(row(label,P), label, row(P)):-person(P).
    attr(row(label,P), label, @stringify(P,true)):-person(P).
    attr(row(label,P), order, 1):-person(P).
    attr(row(label,P), class, ("h3";"text-primary")):-person(P).

    elem(row(income,P), label, row(P)):-person(P).
    attr(row(income,P), label, @format("has income of {}", I)):-income(P,I).
    attr(row(income,P), order, 2):-income(P,I).
    attr(row(income,P), class, "text-primary"):-income(P,I).


    elem(row(lives,P), dropdown_menu, row(P)):-person(P).
    attr(row(lives,P), selected,  @stringify(C,true)):-lives(P,C).
    attr(row(lives,P), order, 3):-person(P).
    attr(row(lives,P), class, ("btn-outline-primary") ):-person(P), not _clinguin_assume(lives(P,_),_).
    attr(row(lives,P), class, ("btn-primary") ):-person(P), _clinguin_assume(lives(P,_),_).

        elem(row(lives_option,(P,C)), dropdown_menu_item, row(lives,P)):-_any(lives(P,C)).
        attr(row(lives_option,(P,C)), label, @stringify(C,true)):-_any(lives(P,C)).
        when(row(lives_option,(P,C)), click, call, add_assumption(lives(P,C),true)):-_any(lives(P,C)).

        elem(row(lives_option,(P,remove)), dropdown_menu_item, row(lives,P)):-lives(P,C).
        attr(row(lives_option,(P,remove)), icon, "fa-ban"):-lives(P,C).
        attr(row(lives_option,(P,remove)), class, "text-info"):-lives(P,C).
        when(row(lives_option,(P,remove)), click, call, remove_assumption_signature(lives(P,any))):-lives(P,C).


    elem(row(deduction,P), label, row(P)):-person(P).
    attr(row(deduction,P), label, @format("deduction= {}",D)):-person(P), _clinguin_assign(deduction(P), D), _clinguin_model(__def(deduction(P))).
    % attr(row(deduction,P), label, "deduction= ?"):-person(P), _clinguin_assign(deduction(P), D), not _clinguin_model(__def(deduction(P))).
    attr(row(deduction,P), order, 4):-person(P).
    attr(row(deduction,P), class, ("fst-italic")):-person(P).

    elem(row(tax,P), label, row(P)):-person(P).
    attr(row(tax,P), label, @format("tax = {}",D)):-person(P), _clinguin_assign(tax(P), D).
    attr(row(tax,P), order, 5):-person(P).
    attr(row(tax,P), class, ("fst-italic")):-person(P).


    attr(row(X,P), class, ("p-2")):-elem(row(X,P),_,_).
    attr(row(X,P), width, 200):-elem(row(X,P),_,_).

elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Tax").
attr(menu_bar, icon, "fa-landmark").

        elem(menu_bar_next, button, menu_bar).
        attr(menu_bar_next, label, "Next").
        attr(menu_bar_next, icon, "fa-forward-step").
        when(menu_bar_next, click, call, next_solution).

        elem(menu_bar_restart, button, menu_bar).
        attr(menu_bar_restart, label, "Restart").
        attr(menu_bar_restart, icon, "fa-arrows-rotate").
        attr(menu_bar_restart, class, "btn-outline-danger").
        attr(menu_bar_restart, class, "border-0").
        when(menu_bar_restart, click, call, restart).
