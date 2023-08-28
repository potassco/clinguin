#const height_value= 800.
#const width_value= 300.
#const color_elevator = "#C1E5AE".
#const color_request = "#E5C2AE".

element(window, window, root).
attribute(window, height, height_value).
attribute(window, width, width_value).
%attribute(window, child_layout, absstatic).
attribute(window, child_layout, grid).

% Info section
element(info, container, window).
%attribute(info, pos_x, 140 ).
%attribute(info, pos_y, 0 ).
attribute(info, child_layout, grid).
attribute(info, grid_column, 1).

element(but, button, window) :- clinguin_browsing.

element(info_find_goal, label, info).
attribute(info_find_goal, grid_row, 0).
attribute(info_find_goal, font_size, 20).
attribute(info_find_goal, label, "✓"):- goal(T),query(T).
attribute(info_find_goal, foreground_color,green):-goal(T),query(T).
attribute(info_find_goal, label, "✕"):- not goal(T),query(T).
attribute(info_find_goal, foreground_color,red):-not goal(T),query(T).

element(info_find_l, button, info):-not goal(T),query(T).
attribute(info_find_l, height, 70 ):-not goal(T),query(T).
attribute(info_find_l, width, 120 ):-not goal(T),query(T).
attribute(info_find_l, grid_row, 1):-not goal(T),query(T).
attribute(info_find_l, label, "Find plan"):-not goal(T),query(T).
callback(info_find_l, click, find_plan):-not goal(T),query(T).

element(info_steps_l, label, info).
attribute(info_steps_l, grid_row, 4).
attribute(info_steps_l, label, "History:").
attribute(info_steps_l, font_size, 18).

element(info_step_c(T),label,info):-_c(occ(A,T)).
element(info_step_c(T),label,info):-occ(A,T), clinguin_browsing.
attribute(info_step_c(T),grid_row,T+4):-occ(A,T).
attribute(info_step_c(T),height,30):-occ(A,T).
attribute(info_step_c(T),width,200):-occ(A,T).
attribute(info_step_c(T),label,A):-occ(A,T).


% Elevator section
element(elevator, container, window).
attribute(elevator, child_layout, grid).
attribute(elecator, grid_column, 0).

element(elevator_row(F), container, elevator):-floor(F).
attribute(elevator_row(F), grid_column, 0):-floor(F).
attribute(elevator_row(F), grid_row, N-(F-1)):-floor(F),n_floors(N).
attribute(elevator_row(F), child_layout, grid):-floor(F).

on_floor(F,T):-floor(F), holds(on(F),T-1), query(T).
call_floor(F,T):-floor(F), holds(called(F),T-1), query(T).

element(elevator_floor(F), dropdown_menu, elevator_row(F)):-floor(F).
attribute(elevator_floor(F), height, 70):-floor(F).
attribute(elevator_floor(F), width, 70):-floor(F).
attribute(elevator_floor(F), grid_column, 0):-floor(F).
attribute(elevator_floor(F), grid_row, 0):-floor(F).

attribute(elevator_floor(F), background_color, color_elevator):- on_floor(F,T).

element(elevator_occ_mi(F,A), dropdown_menu_item, elevator_floor(F)):-
    on_floor(F,T),
    _b(occ(A,T)).
attribute(elevator_occ_mi(F,A), label, A):-
    on_floor(F,T),
    _b(occ(A,T)).
callback(elevator_occ_mi(F,A), click, assume_and_step(occ(A,T))):-
    on_floor(F,T),
    _b(occ(A,T)).


element(elevator_call(F), label, elevator_row(F)):-floor(F).
attribute(elevator_call(F), height, 70):-floor(F).
attribute(elevator_call(F), width, 70):-floor(F).
attribute(elevator_call(F), grid_column, 1):-floor(F).
attribute(elevator_call(F), grid_row, 0):-floor(F).

attribute(elevator_call(F), background_color, color_request):- floor(F), call_floor(F,T).
attribute(elevator_call(F), foreground_color, red):- floor(F), call_floor(F,T).

attribute(elevator_call(F), label, "⬆︎⬇︎"):-floor(F).

% TODO - Wasn't able to get it working with externals
callback(elevator_call(F), click, add_atom(holds(called(F),T-1))):-query(T),floor(F),not call_floor(F,_).

