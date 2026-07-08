icons(pizza, "Pizza").
icons(sushi, "Shell").
icons(burgers, "Hamburger").
icons(salad, "Salad").
order(burgers, 1).
order(sushi, 2).
order(pizza, 3).

elem(w, window, root).
attr(w, class, ("min-h-screen"; "flex"; "flex-col"; "bg-muted")).


elem(header, container, w).
attr(header, class, ("flex"; "items-center"; "justify-between"; "px-6"; "py-4"; "bg-card"; "border-b"; "shadow-sm")).
attr(header, style, "order: 1").

    elem(header_left, container, header).
    attr(header_left, class, ("flex"; "items-center"; "gap-3")).
    attr(header_left, order, 1).
        elem(title_icon, icon, header_left).
        attr(title_icon, icon, I):-chosen(F), icons(F,I).
        attr(title_icon, icon_size, "size-7"):-chosen(F), icons(F,I).
        attr(title_icon, class, "text-primary"):-chosen(F), icons(F,I).
        attr(title_icon, order, 1).
        elem(title, text, header_left).
        attr(title, text, @format("We are eating {}!", F)):-chosen(F).
        attr(title, class, ("text-2xl"; "font-bold"; "text-primary")).
        attr(title, order, 2).

    elem(happy, text, header_left).
    attr(happy, order, 3).
    attr(happy, class, ("text-xs";"text-gray")).
    attr(happy, text, @concat("This makes ", N, " participants are happy")):-number_happy(N).

elem(header_right, container, header).
attr(header_right, class, ("flex"; "items-center"; "gap-3")).
attr(header_right, order, 2).

    elem(toggle, theme_toggle, header_right).
    attr(toggle, order, 3).
    attr(toggle, icon_dark, "Sun").
    attr(toggle, icon_light, "Moon").
    attr(toggle, variant, "outline").
    attr(toggle, class, ("p-2"; "rounded-full")).

    elem(next, button, header_right).
    attr(next, order, 2).
    attr(next, class, ("p-2"; "rounded-full")).
    attr(next, text, "Next option").
    when(next, click, call, next_solution("optN")).
        elem(nexti, icon, next).
        attr(nexti, icon, "FastForward").

    elem(stop, button, header_right):- _clinguin_browsing.
    attr(stop, order, 1):- _clinguin_browsing.
    attr(stop, variant, destructive):- _clinguin_browsing.
    attr(stop, class, ("p-2"; "rounded-full")):- _clinguin_browsing.
    attr(stop, text, "Exit browsing"):- _clinguin_browsing.
    when(stop, click, call, stop_browsing):- _clinguin_browsing.
        elem(stopi, icon, stop):- _clinguin_browsing.
        attr(stopi, icon, "Pause"):- _clinguin_browsing.



elem(eating_options, container, w):-food(F).
attr(eating_options, class, ("flex"; "flex-row"; "gap-4";"mt-4";"mx-2";"h-full")).
attr(eating_options, order, 2).


elem(container(F), container, eating_options):-food(F).
attr(container(F), class, ("p-2";  "rounded-lg"; "border";"w-50";"flex-col";"flex";"h-full")):-food(F).
attr(container(F), order, O):-food(F), order(F,O).


    elem(title(F), text, container(F)):-food(F).
    attr(title(F), order, 1):-food(F).
    attr(title(F), text, F):-food(F).
    attr(title(F), class, ("text-xl"; "font-bold"; "text-primary";"m-2")):-food(F).
    elem(title(icon,F), icon, title(F)):-food(F).
    attr(title(icon,F), icon, I):-food(F), icons(F,I).


    elem(add_preference_dd(F), dropdown_menu, container(F)):-food(F).
    attr(add_preference_dd(F), order, 2):-food(F).
    attr(add_preference_dd(F), label, "Set as preference"):-food(F).
    attr(add_preference_dd(F), class, ("border"; "rounded-md"; "p-3"; "text-sm"; "font-medium";"m-2")):-food(F).


    elem(add_preference_ddc(F), dropdown_menu_content, add_preference_dd(F)):-food(F).

        elem(add_preference_ddc(first,F), dropdown_menu_group, add_preference_ddc(F)):-food(F).
        attr(add_preference_ddc(first,F), label, "First choice"):-food(F).
        attr(add_preference_ddc(first,F), order, 1):-food(F).
        elem(add_preference_ddc(second,F), dropdown_menu_group, add_preference_ddc(F)):-food(F).
        attr(add_preference_ddc(second,F), label, "Second choice"):-food(F).
        attr(add_preference_ddc(second,F), order, 2):-food(F).

        opt(first;second).
        elem(add_preference_ddi(T,P,F), dropdown_menu_item, add_preference_ddc(T,F)):-food(F), person(P), opt(T).
        attr(add_preference_ddi(T,P,F), text, P):-food(F), person(P), opt(T).
        attr(add_preference_ddi(T,P,F), disabled, true):-food(F), person(P), opt(T), not _any(preference(T,P,F)).
        attr(add_preference_ddi(T,P,F), variant, destructive):-food(F), _clinguin_assume(preference(T,P,F),true).
        when(add_preference_ddi(T,P,F), click, call, add_assumption(preference(T,P,F),true)):-food(F), _any(preference(T,P,F)), not _clinguin_assume(preference(T,P,F),true).
        when(add_preference_ddi(T,P,F), click, call, remove_assumption(preference(T,P,F))):-food(F), _clinguin_assume(preference(T,P,F),true).

            elem(add_preference_ddi(icon,T,P,F), icon, add_preference_ddi(T,P,F)):-food(F), person(P), opt(T).
            attr(add_preference_ddi(icon,first,P,F), icon, "Sparkles"):-food(F),person(P), not _clinguin_assume(preference(first,P,F),true).
            attr(add_preference_ddi(icon,second,P,F), icon, "Sparkle"):-food(F), person(P), not _clinguin_assume(preference(second,P,F),true).
            attr(add_preference_ddi(icon,T,P,F), icon, "Trash"):-food(F), _clinguin_assume(preference(T,P,F),true).


    elem(people(F), container, container(F)):-food(F).
    attr(people(F), order, 3):-food(F).
    attr(people(F), class, ("flex"; "flex-col"; "m-2")):-food(F).

        elem(preference(P,F), button, people(F)):-_all(preference(T,P,F)).
        attr(preference(P,F), disable, true):-_all(preference(T,P,F)).
        attr(preference(P,F), text, P):-_all(preference(T,P,F)).
        attr(preference(P,F), class, ("mt-1")):-_all(preference(T,P,F)).
        attr(preference(P,F), variant, outline):-_all(preference(second,P,F)).
        when(preference(P,F), mouseenter, update, (preference(P,F),variant, destructive)):-_all(preference(_,P,F)).
        when(preference(P,F), mouseenter, update, (add_preference_ddi(icon,T,P,F), icon, "Trash")):-_all(preference(T,P,F)).
        when(preference(P,F), mouseleave, update, (preference(P,F),variant, outline)):-_all(preference(second,P,F)).
        when(preference(P,F), mouseleave, update, (preference(P,F),variant, default)):-_all(preference(first,P,F)).
        when(preference(P,F), click, call, remove_assumption(preference(T,P,F))):-_all(preference(T,P,F)).

            elem(preference(icon,P,F), icon, preference(P,F)):-_all(preference(_,P,F)).
            attr(preference(icon,P,F), icon, "Sparkles"):-_all(preference(first,P,F)).
            attr(preference(icon,P,F), icon, "Sparkle"):-_all(preference(second,P,F)).
        % attr(preference(P,F), variant, ("btn"; "btn-success")):-_all(preference(first,P,F)).

