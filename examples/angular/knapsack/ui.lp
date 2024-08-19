elem(w, window, root).
attr(w, class, ("d-flex";"flex-row")).


%%%%%%%%%%%%%%%%%%%%%%%%
% Objects
%%%%%%%%%%%%%%%%%%%%%%%%

elem(objects, container, w).
attr(objects, class, ("p-2")).
attr(objects, width, 300).

    elem(object(O), container, objects):-object(O).
    attr(object(O), class, ("m-1";"p-1";"rounded";"d-flex";"flex-row";"justify-content-between";"bg-opacity-50";"border";"border-1";)):-object(O).
    attr(object(O), class, ("bg-info")):-object(O), not _any_opt(take(O)).
    attr(object(O), class, ("bg-success")):-object(O), _any_opt(take(O)), not taken(O).
    attr(object(O), class, ("bg-secondary")):- taken(O).
    attr(object(O), class, ("bg-danger")):-object(O), _clinguin_assume(take(O),false).
    attr(object(O), class, ("border-dark")):-object(O), _clinguin_assume(take(O),true).
    attr(object(O), class, ("border-white")):-object(O), not _clinguin_assume(take(O),true).

        elem(object_info(O), container, object(O)):-object(O).

            elem(object(label, O), label, object_info(O)):-object(O).
            attr(object(label, O), label, @stringify(O,true)):-object(O).
            attr(object(label, O), class, ("fw-bold";"h6")):-object(O).
            attr(object(label, O), class, ("fw-bold")):-object(O).


            elem(object(value, O), label, object_info(O)):-object(O).
            attr(object(value, O), label, @concat("Value: ", V)):-value(O,V).

            elem(object(weigth, O), label, object_info(O)):-object(O).
            attr(object(weigth, O), label, @concat("Weight: ", W)):-weight(O,W).

        elem(object_buttons(O), container, object(O)):-object(O).
        attr(object_buttons(O), class, ("align-items-end")):-object(O).

            elem(object_add(O), button, object_buttons(O)):-object(O).
            attr(object_add(O), class, ("m-1")):-object(O).
            attr(object_add(O), class, ("btn-primary")):-object(O).
            attr(object_add(O), class, ("disabled")):-object(O), not _any(take(O)).
            attr(object_add(O), icon, "fa-arrow-right"):-object(O), not _clinguin_assume(take(O), true).
            when(object_add(O), click, call, add_assumption(take(O),true)):-object(O), not _clinguin_assume(take(O), true).

            attr(object_add(O), icon, "fa-arrow-left"):-object(O),  _clinguin_assume(take(O), true).
            when(object_add(O), click, call, remove_assumption(take(O))):-object(O),  _clinguin_assume(take(O), true).

            elem(object_ignore(O), button, object_buttons(O)):-object(O).
            % attr(object_ignore(O), label, " Ignore"):-object(O).
            attr(object_ignore(O), class, ("btn";"btn-primary";"m-1")):-object(O).
            attr(object_ignore(O), class, ("disabled")):-object(O), taken(O).
            attr(object_ignore(O), icon, "fa-trash-can"):-object(O), not _clinguin_assume(take(O), false).
            when(object_ignore(O), click, call, add_assumption(take(O),false)):-object(O), not _clinguin_assume(take(O), false).

            attr(object_ignore(O), icon, "fa-check"):-object(O),  _clinguin_assume(take(O), false).
            when(object_ignore(O), click, call, remove_assumption(take(O))):-object(O),  _clinguin_assume(take(O), false).


%%%%%%%%%%%%%%%%%%%%%%%%
% Knapstack
%%%%%%%%%%%%%%%%%%%%%%%%

elem(knapsack, container, w).
attr(knapsack, class,("bg-primary";"bg-opacity-25";"m-3";"p-5";"rounded")).

    elem(taken_objects, container, knapsack).
    attr(taken_objects, class, ("p-2")).
    attr(taken_objects, order, 3).

        taken(O):- _all(take(O)).
        taken(O):- take(O), _clinguin_browsing.

        elem(taken(O), container, taken_objects):-object(O), taken(O).
        attr(taken(O), class, ("bg-secondary";"bg-opacity-50";"m-1";"p-1";"rounded";"border";"border-1";"border-dark")):-object(O), taken(O).

            elem(taken_label(O), label, taken(O)):-object(O), taken(O).
            attr(taken_label(O), label, @stringify(O,true)):-object(O), taken(O).
            attr(taken_label(O), class, "h6"):-object(O), taken(O).

    elem(knapsack_label, label, knapsack).
    attr(knapsack_label, label, "Knapsack").
    attr(knapsack_label, class, ("h4")).
    attr(knapsack_label, order, 1).

    elem(knapsack_weight, label, knapsack).
    attr(knapsack_weight, label, @format("Weigth: {}g",S)):- #sum{W,O: taken(O), weight(O, W)}=S.
    attr(knapsack_weight, class, ("h8";"fw-light")).
    attr(knapsack_weight, order, 2).

    elem(knapsack_value, label, knapsack).
    attr(knapsack_value, label, @format("Value: {}€",S)):- #sum{W,O: taken(O), value(O, W)}=S.
    attr(knapsack_value, class, ("h8";"fw-light")).
    attr(knapsack_value, order, 2).

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Progress bar of the remaining weight
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
	elem(limit_progress_container, container, knapsack).
	attr(limit_progress_container, class,("p-3"; "mt-auto")).
	attr(limit_progress_container, order, 4).

	% Calculate the percentage of weight used
	percentage_used(P) :- 
		#sum{W,O: taken(O), weight(O, W)} = S, 
		weight_limit(MAX), 
		P = (S * 100) / MAX.

	elem(limit_progress, progress_bar, limit_progress_container).
	attr(limit_progress, value, P) :- percentage_used(P).
	attr(limit_progress, class, "bg-success") :- percentage_used(P), P < 60.
	attr(limit_progress, class, "bg-warning") :- percentage_used(P), P >= 60, P < 100.
	attr(limit_progress, class, "bg-danger") :- percentage_used(P), P >= 100.
	attr(limit_progress, class, ("progress-bar"; "progress-bar-striped")).
	attr(limit_progress, height, 30).
	attr(limit_progress, width, 300).

	% The label inside the progress bar showing the remaining weight
	attr(limit_progress, label, @concat("Remaining weight: ", Remaining, "g")) :-
		#sum{W,O: taken(O), weight(O, W)} = S, 
		weight_limit(MAX), 
		Remaining = MAX - S.


%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar
%%%%%%%%%%%%%%%%%%%%%%%%

elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Knapsack").
attr(menu_bar, icon, "fa-suitcase").


    elem(menu_bar_clear, button, menu_bar).
    attr(menu_bar_clear, label, "Clear").
    attr(menu_bar_clear, icon, "fa-trash").
    attr(menu_bar_clear, class, "btn-outline-danger").
    attr(menu_bar_clear, class, "border-0").
    when(menu_bar_clear, click, call, clear_assumptions).

    elem(menu_bar_select, button, menu_bar).
    attr(menu_bar_select, label, "Select solution").
    attr(menu_bar_select, icon, "fa-hand-pointer").
    when(menu_bar_select, click, call, select).

    elem(menu_bar_next_opt, button, menu_bar).
    attr(menu_bar_next_opt, label, "Next").
    attr(menu_bar_next_opt, icon, "fa-forward-fast").
    when(menu_bar_next_opt, click, call, next_solution(optN)).
