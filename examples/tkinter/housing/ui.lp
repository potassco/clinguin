#const height_value= 800.
#const height_names= 250.
#const width_value= 400.
#const color_considered = "#C1E5AE".
#const color_considered_on_hover = "#6cc13e".
#const color_not_considered = "#E5C2AE".
#const color_not_considered_on_hover = "#c16e3e".

% Window
elem(window, window, root).
attr(window, height, height_value).
attr(window, width, width_value).
attr(window, background_color, white).
attr(window, resizable_x, 1).
attr(window, resizable_y, 1).
attr(window, child_layout, absstatic).

elem(menu_bar, menu_bar, window).
elem(menu_bar_section, menu_bar_section, menu_bar).
attr(menu_bar_section, label, "Options").
elem(menu_bar_section_clear, menu_bar_section_item, menu_bar_section).
attr(menu_bar_section_clear, label, "Clear").
attr(menu_bar_section_clear, accelerator, "Cmd+C").
when(menu_bar_section_clear, click, call, clear_assumptions).
elem(menu_bar_section_next, menu_bar_section_item, menu_bar_section).
attr(menu_bar_section_next, label, "Next").
attr(menu_bar_section_next, accelerator, "Cmd+N").
when(menu_bar_section_next, click, call, next_solution).
elem(menu_bar_section_select, menu_bar_section_item, menu_bar_section).
attr(menu_bar_section_select, label, "Select").
attr(menu_bar_section_select, accelerator, "Cmd+S").
when(menu_bar_section_select, click, call, select).
elem(menu_bar_section_next_opt, menu_bar_section_item, menu_bar_section).
attr(menu_bar_section_next_opt, label, "Next Optimal").
attr(menu_bar_section_next_opt, accelerator, "Cmd+O").
when(menu_bar_section_next_opt, click, call, next_solution(optN)).


% Top container
elem(upper_container, container, window).
attr(upper_container, height, height_names).
attr(upper_container, width, width_value).
attr(upper_container, child_layout, grid).

% Top container titles
in_house_column_label(add_person_container,"People not considered";
                remove_person_container,"People considered").
in_house_column(C):-in_house_column_label(C,_).

elem((C,title), label, upper_container):-in_house_column(C).
attr((C,title), grid_row, 0):-in_house_column(C).
attr((C,title), height, 20):-in_house_column(C).
attr((C,title), width, width_value/2):-in_house_column(C).

attr((C,title), label, L):-in_house_column_label(C,L).
attr((C,title), font_size, 18):-in_house_column(C).

attr((remove_person_container,title), grid_column, 1).
attr((add_person_container,title), grid_column, 0).
attr((remove_person_container,title), background_color, color_considered ).
attr((add_person_container,title), background_color, color_not_considered ).

% Add and remove comulmns
elem(C, container, upper_container):- in_house_column(C) .
attr(C, grid_row, 1):-in_house_column(C).
attr(C, height, height_names-20):-in_house_column(C).
attr(C, width, width_value/2):-in_house_column(C).
attr(C, child_layout, flex):-in_house_column(C).
attr(remove_person_container, grid_column, 1).
attr(add_person_container, grid_column, 0).

% People to add to the house
can_add(P):-person(P), not in_house(P).

elem(person_add(P), label, add_person_container):- can_add(P).
attr(person_add(P), label, P) :- can_add(P).
attr(person_add(P), background_color, color_not_considered) :- can_add(P).
when(person_add(P), click, call, set_external(in_house(P),true)):- can_add(P), not setting_rooms.
attr(person_add(P), on_hover, true) :- can_add(P).
attr(person_add(P), on_hover_background_color, color_not_considered_on_hover) :- can_add(P).

% People to remove from the house
can_remove(P):- in_house(P).
elem(person_remove(P), label, remove_person_container):- can_remove(P).
attr(person_remove(P), label, P) :- can_remove(P).
attr(person_remove(P), background_color, color_considered) :- can_remove(P).
when(person_remove(P), click, call, set_external(in_house(P),false)):-can_remove(P), not setting_rooms.
attr(person_remove(P), on_hover, true) :- can_remove(P).
attr(person_remove(P), on_hover_background_color, color_considered_on_hover) :- can_remove(P).

% Next

elem(button_next, button, window) :- not setting_rooms.
attr(button_next, height, 40) :- not setting_rooms.
attr(button_next, width, width_value) :- not setting_rooms.
attr(button_next, pos_x, 0) :- not setting_rooms.
attr(button_next, pos_y, height_names) :- not setting_rooms.
attr(button_next, label, "Define rooms") :- not setting_rooms.
when(button_next, click, call, set_external(setting_rooms,true)) :- not setting_rooms.

room_assigned :- _c(assign(_,_)).

elem(define_people_button, button, window) :- setting_rooms, not room_assigned.
attr(define_people_button, height, 40) :- setting_rooms, not room_assigned.
attr(define_people_button, width, width_value) :- setting_rooms, not room_assigned.
attr(define_people_button, pos_x, 0) :- setting_rooms, not room_assigned.
attr(define_people_button, pos_y, height_names) :- setting_rooms, not room_assigned.
attr(define_people_button, label, "Define People") :- setting_rooms, not room_assigned.
when(define_people_button, click, call, set_external(setting_rooms,false)) :- setting_rooms, not room_assigned.

elem(clear_rooms_button, button, window) :- setting_rooms, room_assigned.
attr(clear_rooms_button, height, 40) :- setting_rooms, room_assigned.
attr(clear_rooms_button, width, width_value) :- setting_rooms, room_assigned.
attr(clear_rooms_button, pos_x, 0) :- setting_rooms, room_assigned.
attr(clear_rooms_button, pos_y, height_names) :- setting_rooms, room_assigned.
attr(clear_rooms_button, label, "Clear Room Assignment") :- setting_rooms, room_assigned.
when(clear_rooms_button, click, call, clear_assumptions) :- setting_rooms, room_assigned.


% Rooms container
elem(rooms_main_container, container, window):-setting_rooms.
attr(rooms_main_container, height, height_value - height_names - 40).
attr(rooms_main_container, width, width_value).
attr(rooms_main_container, pos_x, 0).
attr(rooms_main_container, pos_y, height_names+40).
attr(rooms_main_container, child_layout, grid).

% Room container
elem(room(I), container, rooms_main_container) :- room(I,_),setting_rooms.
attr(room(I), height, 200) :- room(I,_).
attr(room(I), width, 200) :- room(I,_).
attr(room(I), grid_column, (I-1)\2) :- room(I,_).
attr(room(I), grid_row, (I-1)/2) :- room(I,_).
attr(room(I), child_layout, absstatic) :- room(I,_).

% Room title
elem(room_title(I), label, room(I)) :- room(I,_),setting_rooms.
attr(room_title(I), height, 20) :- room(I,_).
attr(room_title(I), width, 190) :- room(I,_).
attr(room_title(I), label, T) :- room(I,T).

% Room beds dropdowns
elem(room_dropdown(B,I), dropdown_menu, room(I)) :- bed(B,I),setting_rooms.
attr(room_dropdown(B,I), selected, P) :- _c(assign(bed(B,I),P)).
attr(room_dropdown(B,I), height, 30) :- bed(B,I).
attr(room_dropdown(B,I), selected, P) :- assign(bed(B,I),P), _clinguin_browsing.
attr(room_dropdown(B,I), width, 100) :- bed(B,I).
attr(room_dropdown(B,I), pos_y, B*40):- bed(B,I).
when(room_dropdown(B,I), clear, call, remove_assumption_signature(assign(bed(B,I),any))) :- bed(B,I).

elem(mi(B,I,P), dropdown_menu_item, room_dropdown(B,I)) :- _b(assign(bed(B,I),P)),setting_rooms.
attr(mi(B,I,P), label, P) :- _b(assign(bed(B,I),P)).
when(mi(B,I,P), click, call, add_assumption(assign(bed(B,I),P))) :- _b(assign(bed(B,I),P)).


