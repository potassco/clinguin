#const height_value= 800.
#const width_value= 300.
#const color_elevator = "#C1E5AE".
#const color_request = "#E5C2AE".
element(window, window, root).
attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, child_layout, absstatic).
attribute(window, fit, false).

% Info section
element(info, container, window).
attribute(info, height, N*70 ):-n_floors(N).
attribute(info, width, 200 ).
attribute(info, pos_x, 140 ).
attribute(info, pos_y, 0 ).
attribute(info, child_layout, grid).
attribute(info, fit, false).

element(info_find, container, info).
attribute(info_find, height, 70 ).
attribute(info_find, width, 120 ).
attribute(info_find, grid_row, 0).
attribute(info_find, fit, false).

element(info_find_goal, label, info_find).
attribute(info_find_goal, font_size, 20).
attribute(info_find_goal, label, "✓"):- goal(T),query(T).
attribute(info_find_goal, label, "✕"):- not goal(T),query(T).
attribute(info_find_goal, foreground_color,green).

element(info_next, container, info).
attribute(info_next, height, 70 ).
attribute(info_next, width, 120 ).
attribute(info_next, grid_row, 1).
% attribute(info_next, grid_column, 1).
attribute(info_next, fit, false).

element(info_find_l, button, info_next):-not goal(T),query(T).
attribute(info_find_l, label, "Find plan"):-not goal(T),query(T).
callback(info_find_l, click, findPlan):-not goal(T),query(T).

element(info_steps, container, info).
attribute(info_steps, height, 70 ).
attribute(info_steps, width, 200 ).
attribute(info_steps, grid_row, 4).
attribute(info_steps, fit, false).

element(info_steps_l, label, info_steps).
attribute(info_steps_l, label, "History:").
attribute(info_steps_l, font_size, 18).

element(info_step_c(T),container,info):-occ(A,T).
attribute(info_step_c(T),grid_row,T+4):-occ(A,T).
attribute(info_step_c(T),height,30):-occ(A,T).
attribute(info_step_c(T),width,200):-occ(A,T).
attribute(info_step_c(T), fit, false) :- occ(A,T).

element(info_step(T),label,info_step_c(T)):-occ(A,T).
attribute(info_step(T),label,A):-occ(A,T).



% Elevator section
element(elevator, container, window).
attribute(elevator, fit, false).
attribute(elevator, height, N*70 ):-n_floors(N).
attribute(elevator, width, 140 ):-n_floors(N).
attribute(elevator, child_layout, grid).

element(elevator_row(F), container, elevator):-floor(F).
attribute(elevator_row(F), fit, false) :- floor(F).
attribute(elevator_row(F), height, 70):-floor(F).
attribute(elevator_row(F), width, 140):-floor(F).
attribute(elevator_row(F), grid_column, 0):-floor(F).
attribute(elevator_row(F), grid_row, N-(F-1)):-floor(F),n_floors(N).
attribute(elevator_row(F), child_layout, grid):-floor(F).

element(elevator_call(F), container, elevator_row(F)):-floor(F).
attribute(elevator_call(F), fit, false) :- floor(F).
attribute(elevator_call(F), height, 70):-floor(F).
attribute(elevator_call(F), width, 70):-floor(F).
attribute(elevator_call(F), grid_column, 1):-floor(F).
attribute(elevator_call(F), grid_row, 0):-floor(F).

element(elevator_floor(F), container, elevator_row(F)):-floor(F).
attribute(elevator_floor(F), fit, false) :- floor(F).
attribute(elevator_floor(F), height, 70):-floor(F).
attribute(elevator_floor(F), width, 70):-floor(F).
attribute(elevator_floor(F), grid_column, 0):-floor(F).
attribute(elevator_floor(F), grid_row, 0):-floor(F).
attribute(elevator_floor(F), border_width, 2):-floor(F).


on_floor(F,T):-floor(F), holds(on(F),T-1), query(T).
call_floor(F,T):-floor(F), holds(called(F),T-1), query(T).

attribute(elevator_floor(F), background_color, color_elevator):- on_floor(F,T).

element(elevator_occ(F), dropdown_menu, elevator_floor(F)):- on_floor(F,T).

element(elevator_occ_mi(F,A), dropdown_menu_item, elevator_occ(F)):-
    on_floor(F,T),
    _b(occ(A,T)).

attribute(elevator_occ_mi(F,A), label, A):-
    on_floor(F,T),
    _b(occ(A,T)).

callback(elevator_occ_mi(F,A), click, assumeAndStep(occ(A,T))):-
    on_floor(F,T),
    _b(occ(A,T)).

attribute(elevator_call(F), background_color, color_request):- floor(F), call_floor(F,T).
element(elevator_call_b(F), button, elevator_call(F)):-floor(F),not call_floor(F,_).
attribute(elevator_call_b(F), label, "⬆︎⬇︎"):-floor(F),not call_floor(F,_).
callback(elevator_call_b(F), click, externalTrue(call(F,T-1))):-query(T),floor(F),not call_floor(F,_).
