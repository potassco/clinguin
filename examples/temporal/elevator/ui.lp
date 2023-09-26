#const height_value= 800.
#const width_value= 300.
#const color_elevator = "#C1E5AE".
#const color_request = "#E5C2AE".

elem(window, window, root).
attr(window, height, height_value).
attr(window, width, width_value).
%attr(window, child_layout, absstatic).
attr(window, child_layout, grid).

% Info section
elem(info, container, window).
%attr(info, pos_x, 140 ).
%attr(info, pos_y, 0 ).
attr(info, child_layout, grid).
attr(info, grid_column, 1).

elem(but, button, window) :- clinguin_browsing.

elem(info_find_goal, label, info).
attr(info_find_goal, grid_row, 0).
attr(info_find_goal, font_size, 20).
attr(info_find_goal, label, "✓"):- goal(T),query(T).
attr(info_find_goal, foreground_color,green):-goal(T),query(T).
attr(info_find_goal, label, "✕"):- not goal(T),query(T).
attr(info_find_goal, foreground_color,red):-not goal(T),query(T).

elem(info_find_l, button, info):-not goal(T),query(T).
attr(info_find_l, height, 70 ):-not goal(T),query(T).
attr(info_find_l, width, 120 ):-not goal(T),query(T).
attr(info_find_l, grid_row, 1):-not goal(T),query(T).
attr(info_find_l, label, "Find plan"):-not goal(T),query(T).
callback(info_find_l, click, find_plan):-not goal(T),query(T).

elem(info_steps_l, label, info).
attr(info_steps_l, grid_row, 4).
attr(info_steps_l, label, "History:").
attr(info_steps_l, font_size, 18).

elem(info_step_c(T),label,info):-_c(occ(A,T)).
elem(info_step_c(T),label,info):-occ(A,T), clinguin_browsing.
attr(info_step_c(T),grid_row,T+4):-occ(A,T).
attr(info_step_c(T),height,30):-occ(A,T).
attr(info_step_c(T),width,200):-occ(A,T).
attr(info_step_c(T),label,A):-occ(A,T).


% Elevator section
elem(elevator, container, window).
attr(elevator, child_layout, grid).
attr(elecator, grid_column, 0).

elem(elevator_row(F), container, elevator):-floor(F).
attr(elevator_row(F), grid_column, 0):-floor(F).
attr(elevator_row(F), grid_row, N-(F-1)):-floor(F),n_floors(N).
attr(elevator_row(F), child_layout, grid):-floor(F).

on_floor(F,T):-floor(F), holds(on(F),T-1), query(T).
call_floor(F,T):-floor(F), holds(called(F),T-1), query(T).

elem(elevator_floor(F), dropdown_menu, elevator_row(F)):-floor(F).
attr(elevator_floor(F), height, 70):-floor(F).
attr(elevator_floor(F), width, 70):-floor(F).
attr(elevator_floor(F), grid_column, 0):-floor(F).
attr(elevator_floor(F), grid_row, 0):-floor(F).

attr(elevator_floor(F), background_color, color_elevator):- on_floor(F,T).

elem(elevator_occ_mi(F,A), dropdown_menu_item, elevator_floor(F)):-
    on_floor(F,T),
    _b(occ(A,T)).
attr(elevator_occ_mi(F,A), label, A):-
    on_floor(F,T),
    _b(occ(A,T)).
callback(elevator_occ_mi(F,A), click, assume_and_step(occ(A,T))):-
    on_floor(F,T),
    _b(occ(A,T)).


elem(elevator_call(F), label, elevator_row(F)):-floor(F).
attr(elevator_call(F), height, 70):-floor(F).
attr(elevator_call(F), width, 70):-floor(F).
attr(elevator_call(F), grid_column, 1):-floor(F).
attr(elevator_call(F), grid_row, 0):-floor(F).

attr(elevator_call(F), background_color, color_request):- floor(F), call_floor(F,T).
attr(elevator_call(F), foreground_color, red):- floor(F), call_floor(F,T).

attr(elevator_call(F), label, "⬆︎⬇︎"):-floor(F).

% TODO - Wasn't able to get it working with externals
callback(elevator_call(F), click, add_atom(holds(called(F),T-1))):-query(T),floor(F),not call_floor(F,_).

