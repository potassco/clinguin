elem(w, window, root).
attr(w, class, ("d-flex";"flex-row")).

category(taken;available;not_available).
elem(category(C), container, w):-category(C).
attr(category(C), class, ("p-2";"bg-opacity-25";"m-3";"rounded")):- category(C).
attr(category(C), width, 300):- category(C).
attr(category(not_available), order, 1).
attr(category(available), order, 2).
attr(category(taken), order, 3).

attr(category(available), class, ("bg-info")).
attr(category(taken), class, ("bg-secondary")).
attr(category(not_available), class, ("bg-danger")).


elem(category_label_c(C), container, category(C)):-category(C).
attr(category_label_c(C), order, 1):-category(C).
attr(category_label_c(C), class, ("justify-content-center";"align-items-center")):-category(C).

elem(category_objects_c(C), container, category(C)):-category(C).
attr(category_objects_c(C), order, 2):-category(C).


%%%%%%%%%%%%%%%%%%%%%%%%
% Labels
%%%%%%%%%%%%%%%%%%%%%%%%

elem(category_label(not_available), label, category_label_c(not_available)).
% attr(category_label(not_available), label, "Disliked").
attr(category_label(not_available), class, ("h6";"pb-5";"pt-3";"fa";"fa-thumbs-down")).

elem(category_label(available), label, category_label_c(available)).
% attr(category_label(available), label, "Remaining").
attr(category_label(available), class, ("h6";"pb-5";"pt-3";"fa";"fa-thumbs-up")).

elem(knapsack_label, button, category_label_c(taken)).
attr(knapsack_label, icon, ("fa-suitcase")).
attr(knapsack_label, class, ("align-center")).
% attr(knapsack_label, class, ("btn-lg")).
attr(knapsack_label, order, 1).


elem(knapsack_value, label, category_label_c(taken)).
attr(knapsack_value, label, @format("Value: {}€",S)):- #sum{W,O: object(O,taken), value(O, W)}=S.
attr(knapsack_value, class, ("h8";"fw-light")).
attr(knapsack_value, order, 2).


elem(weight_progress_bar, progress_bar, category_label_c(taken)).
attr(weight_progress_bar, order, 3).
attr(weight_progress_bar, value, S) :- #sum{W,O: object(O,taken), weight(O, W)} = S.
attr(weight_progress_bar, min, 0).
attr(weight_progress_bar, max, MAX) :- weight_limit(MAX).
attr(weight_progress_bar, height, 20).
attr(weight_progress_bar, width, 200).

attr(weight_progress_bar, out_label, @concat(Remaining, "g")) :-
    #sum{W,O: object(O,taken), weight(O, W)} = S,
    weight_limit(MAX),
    Remaining = MAX - S.
attr(weight_progress_bar, label, @concat(S, "g")) :-
    #sum{W,O: object(O,taken), weight(O, W)} = S.

%%%%%%%%%%%%%%%%%%%%%%%%
% Objects
%%%%%%%%%%%%%%%%%%%%%%%%


object(O, taken):- object(O), _clinguin_assume(take(O),true).
object(O, taken):- _clinguin_browsing, object(O), take(O).
object(O, not_available):- object(O), _clinguin_assume(take(O),false).
object(O, available):- object(O), not object(O, taken), not object(O, not_available).

elem(object(O), container, category_objects_c(C)):-object(O, C).
attr(object(O), class, ("m-1";"p-1";"bg-primary";"border-primary";"rounded";"d-flex";"flex-row";"justify-content-between";"bg-opacity-50";"border";"border-1")):-object(O).

% --- Drag and drop

attr(object(O), draggable_as, O):-object(O, _).
attr(object(O), drop_target, category(taken)):-object(O, _), _any(take(O)).
attr(object(O), drop_target, category(not_available)):-object(O).
attr(object(O), drop_target, category(available)):-object(O,T), T!=available.
when(category(taken), drop, call, (remove_assumption(take(_dragged)),add_assumption(take(_dragged),true))).
when(category(not_available), drop, call, (remove_assumption(take(_dragged)),add_assumption(take(_dragged),false))).
when(category(available), drop, call, remove_assumption(take(_dragged))).

    elem(object_info(O), container, object(O)):-object(O).
    attr(object_info(O), class, ("ps-4")):-object(O).

            elem(object(label, O), label, object_info(O)):-object(O).
            attr(object(label, O), label, @stringify(O,true)):-object(O).
            attr(object(label, O), class, ("fw-bold";"h6")):-object(O).
            attr(object(label, O), class, ("text-left")):-object(O).


            elem(object(value, O), label, object_info(O)):-object(O).
            attr(object(value, O), label, @concat("Value: ", V, "€")):-value(O,V).
            attr(object(value, O), class, ("h6";"fw-light")):-value(O,V).

            elem(object(weigth, O), label, object_info(O)):-object(O).
            attr(object(weigth, O), label, @concat("Weight: ", W,"g")):-weight(O,W).
            attr(object(weigth, O), class, ("fw-light")):-weight(O,W).

    elem(object_star(O), button, object(O)):-object(O,available), _any_opt(take(O)).
    attr(object_star(O), icon, "fa-medal"):-object(O,available), _any_opt(take(O)).
    attr(object_star(O), class, ("disabled";"border"; "border-0")):-object(O,available), _any_opt(take(O)).


        % ---- Unlock to drag an object
        % This allows an intermediate call that will remove assumptions to get available destination using the _any/2 predicate
        % Make sure the line `attr(object(O), draggable_as, O):-object(O, _).` above is removed


        % % Unlocked objects will appear in the original column
        % object(O, X):- object(O), _clinguin_context(unlocked(O),X).

        % % Unlocked objects are draggable and stand out
        % attr(object(O), filter, "opacity(0.8)"):-object(O), not _clinguin_context(unlocked(O),_).
        % attr(object(O), "box-shadow", "0 2px 2px 2px #00000070" ):- object(O), _clinguin_context(unlocked(O),_).
        % attr(object(O), draggable_as, O):-object(O, _), _clinguin_context(unlocked(O),_).

        % % Button to lock and unlock objects
        % elem(object_move(O), button, object(O)):-object(O,_).
        % attr(object_move(O), icon, "fa-lock"):-object(O,_), not _clinguin_context(unlocked(O),_).
        % attr(object_move(O), icon, "fa-lock-open"):-_clinguin_context(unlocked(O),_).
        % attr(object_move(O), class, ("btn-sm";"btn-outline-primary";"border"; "border-0")):-object(O,_).
        % % When unlocking the assumption is removed and the context is updated
        % when(object_move(O), click, call, remove_assumption(take(O))):-object(O, _), not _clinguin_context(unlocked(O),_).
        % when(object_move(O), click, context, (unlocked(O),X)):-object(O, X), not _clinguin_context(unlocked(O),_).

        % % Dummy event for locking an object
        % when(object_move(O), click, call, get):-_clinguin_context(unlocked(O),_).

        % % Any action, if something was unlocked then it is put back
        % when(O', E, call, get):- when(O', E, call, _), E!=drop, _clinguin_context(unlocked(O),available).
        % when(O', E, call, add_assumption(take(O),true)):- when(O', E, call, _), E!=drop, _clinguin_context(unlocked(O),taken).
        % when(O', E, call, add_assumption(take(O),false)):- when(O', E, call, _), E!=drop, _clinguin_context(unlocked(O),not_available).


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
