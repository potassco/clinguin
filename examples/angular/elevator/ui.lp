time(0):-not query(_).
time(T):-query(T).


elem(w, window, root).
attr(w, child_layout, flex).
attr(w, flex_direction, row).
when(w, load, call, (ground(step,(1)),set_external(query(1),true))):- time(0), not query(_).

%%%%%%%%%%%%%%%%%%%%%%%%
% Container with elevator
%%%%%%%%%%%%%%%%%%%%%%%%
elem(elevator, container, w).
attr(elevator, class, ("bg-info";"m-2";"flex-column-reverse";"d-flex")).
    elem(elevator_row(F), container, elevator):-floor(F).
    attr(elevator_row(F), height, 80):-floor(F).
    attr(elevator_row(F), class, ("d-flex";"justify-content-center";"align-items-center";"m-1";"flex-row")):-floor(F).
    attr(elevator_row(F), order, F):-floor(F).
    attr(elevator_row(F), width, 80):-floor(F).
    attr(elevator_row(F), class, ("bg-primary";"bg-opacity-50")):-floor(F), holds(on(F),T-1), time(T).
    attr(elevator_row(F), class, ("bg-success";"bg-opacity-50")):-floor(F), holds(on(F),T-1), served(F,T-1), time(T).

    elem(elevator_button_move(F), container, elevator_row(F)):-holds(on(F),T-1).

        elem(elevator_button(serve), button, elevator_row(F)):- _any(occ(serve,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(serve), icon, "fa-angles-left"):- _any(occ(serve,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(serve), class, ("btn";"btn-outline-primary";"btn-sm";"border-0")):- _any(occ(serve,T)), holds(on(F),T-1), time(T).

        elem(elevator_button(down), button, elevator_button_move(F)):- _any(occ(down,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(down), order, 1):- _any(occ(down,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(down), icon, "fa-sort-down"):- _any(occ(down,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(down), class, ("btn";"btn-outline-primary";"btn-sm";"border-0")):- _any(occ(down,T)), holds(on(F),T-1), time(T).

        elem(elevator_button(up), button, elevator_button_move(F)):- _any(occ(up,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(up), order, 0):- _any(occ(up,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(up), icon, "fa-sort-up"):- _any(occ(up,T)), holds(on(F),T-1), time(T).
        attr(elevator_button(up), class, ("btn";"btn-outline-primary";"btn-sm";"border-0")):- _any(occ(up,T)), holds(on(F),T-1), time(T).


        when(elevator_button(A), click, call,
            (add_assumption(occ(A,T)),
            ground(step,(T+1)),
            set_external(query(T), false),
            set_external(query(T+1), true)
        )):- action(A), _any(occ(A,T)), time(T).

%%%%%%%%%%%%%%%%%%%%%%%%
% Container with floors
%%%%%%%%%%%%%%%%%%%%%%%%

elem(floors, container, w).
attr(floors, class, ("m-2";"flex-column-reverse";"d-flex")).
    elem(floor_row(F), container, floors):-floor(F).
    attr(floor_row(F), height, 80):-floor(F).
    attr(floor_row(F), class, ("d-flex";"justify-content-center";"align-items-center";"m-1";"border-1";"border-top";"border-bottom")):-floor(F).
    attr(floor_row(F), order, F):-floor(F).
    attr(floor_row(F), width, 80):-floor(F).

    elem(floor_button(F), button, floor_row(F)):-floor(F), time(T).
    attr(floor_button(F), icon, "fa-bell"):-floor(F), time(T).
    attr(floor_button(F), class, ("btn-success")):-floor(F), holds(called(F),T), time(T).
    attr(floor_button(F), class, ("btn-outline-success";"border-0";"opacity-50")):-floor(F), not holds(called(F),T), time(T).
    when(floor_button(F), click, call, set_external(call(F,T), true)):-floor(F), not holds(called(F),T), time(T).

%%%%%%%%%%%%%%%%%%%%%%%%
% Message
%%%%%%%%%%%%%%%%%%%%%%%%

elem(done, message, w):- goal(_).
attr(done, message, "No more pending requests"):- goal(_).
attr(done, title, "Done!"):- goal(_).
attr(done, type, "success"):- goal(_).


%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar
%%%%%%%%%%%%%%%%%%%%%%%%
elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Elevator").
attr(menu_bar, icon, "fa-elevator").


    next_step_operations((
        ground(step,(T+1)),
        set_external(query(T), false),
        set_external(query(T+1), true),
        set_external(check(T), false),
        set_external(check(T+1), true)
    )):-_clinguin_external(query(T),true).

    elem(menu_bar_next, button, menu_bar):- not goal(_).
    attr(menu_bar_next, label, "Solve incrementally"):- not goal(_).
    attr(menu_bar_next, icon, "fa-forward-step"):- not goal(_).
    when(menu_bar_next, click, call,O):-not goal(_), next_step_operations(O).
    when(w, load, call, O):- _clinguin_unsat, _clinguin_external(check(T),true), next_step_operations(O).
    when(w, load, call, (select("#show occ/2."),
        ground(step,(T+1)),
        set_external(query(T), false),
        set_external(query(T+1), true),
        set_external(check(T),false))
    ):- time(T), not _clinguin_unsat, _clinguin_external(check(T),true).
