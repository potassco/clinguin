#const color_considered = "#C1E5AE".
#const color_considered_on_hover = "#6cc13e".
#const color_not_considered = "#E5C2AE".
#const color_not_considered_on_hover = "#c16e3e".
%#const height_value= 800.
%#const height_persons= 250.
#const width_value= 400.


% Window
element(window, window, root).
attribute(window, width, width_value).
attribute(window, background_color, white).
attribute(window, resizable_x, 1).
attribute(window, resizable_y, 1).
attribute(window, child_layout, flex).
attribute(window, flex_direction, column).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MODAL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

element(modal, modal, window).
attribute(modal, title, "Edit People").

element(c1, container, modal).
attribute(c1, pos_x, 0).
attribute(c1, pos_y, 0).
attribute(c1, height, 200).
attribute(c1, width, 500).
attribute(c1, child_layout, flex).
attribute(c1, flex_direction, row_reverse).

element(t1, textfield, c1).
attribute(t1, placeholder, "Please enter the name of the person.").
do(t1, type, context, (t1_content, _value)).

element(b1, button, c1).
do(b1, click, callback, add_atom(person(_value_context(t1_content)))).
attribute(b1, label, "Add Person").

element(c2, container, modal).
attribute(c2, pos_x, 0).
attribute(c2, pos_y, 250).
attribute(c2, height, 200).
attribute(c2, width, 500).
attribute(c2, child_layout, flex).
attribute(c2, flex_direction, column).

element(c3(X), container, c2) :- person(X).
attribute(c3(X), child_layout, flex) :- person(X).
attribute(c3(X), flex_direction, row) :- person(X).

element(l(X), label, c3(X)) :- person(X).
attribute(l(X), label, X) :- person(X).
attribute(l(X), background_color, "#00ff00") :- person(X).

element(b(X), button, c3(X)) :- person(X).
attribute(b(X), label, "Remove Name") :- person(X).
do(b(X), click, callback, remove_atom(person(X))) :- person(X).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar is defined automatically called _default_menu_bar with one section _default_menu_bar_section
% These lines only add an extra option
element(_default_menu_bar_section_next_opt, menu_bar_section_item, _default_menu_bar_section).
attribute(_default_menu_bar_section_next_opt, label, "Next Optimal").
do(_default_menu_bar_section_next_opt, click, callback, next_solution(optN)).

element(menu_bar_section_2, menu_bar_section, _default_menu_bar).
attribute(menu_bar_section_2, label, "Edit Persons").
do(menu_bar_section_2, click, update, (modal, visible, shown)) :- not room_assigned, not setting_rooms.
do(menu_bar_section_2, click, update, (message_impossible_op, visible, shown)) :- adding_people_not_possible.

adding_people_not_possible :- room_assigned.
adding_people_not_possible :- setting_rooms.

element(message_impossible_op,message,window):- adding_people_not_possible.
attribute(message_impossible_op,title,"Invalid Operation!"):- adding_people_not_possible.
attribute(message_impossible_op,message,"Adding people only possible while not in room-defining mode and no people asisgned."):- adding_people_not_possible.
attribute(message_impossible_op,type,error):- adding_people_not_possible.
attribute(message_impossible_op,visible,hidden) :- adding_people_not_possible.


% Top container
element(upper_container, container, window).
attribute(upper_container, "order", 1).
attribute(upper_container, width, width_value).
attribute(upper_container, child_layout, grid).

% Top container titles
in_house_column_label(add_person_container,"People not considered";
                remove_person_container,"People considered").
in_house_column(C):-in_house_column_label(C,_).

element((C,title), label, upper_container):-in_house_column(C).
attribute((C,title), grid_row, 0):-in_house_column(C).
attribute((C,title), height, 20):-in_house_column(C).
attribute((C,title), width, width_value/2):-in_house_column(C).

attribute((C,title), label, L):-in_house_column_label(C,L).
attribute((C,title), font_size, 18):-in_house_column(C).

attribute((remove_person_container,title), grid_column, 1).
attribute((add_person_container,title), grid_column, 0).
attribute((remove_person_container,title), background_color, color_considered ).
attribute((add_person_container,title), background_color, color_not_considered ).

% Add and remove columns
element(C, container, upper_container):- in_house_column(C) .
attribute(C, grid_row, 1):-in_house_column(C).
attribute(C, height, height_names-20):-in_house_column(C).
attribute(C, width, width_value/2):-in_house_column(C).
attribute(C, child_layout, flex):-in_house_column(C).
attribute(remove_person_container, grid_column, 1).
attribute(add_person_container, grid_column, 0).

% People to add to the house
can_add(P):-person(P), not in_house(P).

element(person_add(P), label, add_person_container):- can_add(P).
attribute(person_add(P), label, P) :- can_add(P).
attribute(person_add(P), background_color, color_not_considered) :- can_add(P).
do(person_add(P), click, callback, set_external(in_house(P),true)):- can_add(P), not setting_rooms.
attribute(person_add(P), on_hover, true) :- can_add(P).
attribute(person_add(P), on_hover_background_color, color_not_considered_on_hover) :- can_add(P).

% People to remove from the house
can_remove(P):- in_house(P).
element(person_remove(P), label, remove_person_container):- can_remove(P).
attribute(person_remove(P), label, P) :- can_remove(P).
attribute(person_remove(P), background_color, color_considered) :- can_remove(P).
do(person_remove(P), click, callback, set_external(in_house(P),false)):-can_remove(P), not setting_rooms.
attribute(person_remove(P), on_hover, true) :- can_remove(P).
attribute(person_remove(P), on_hover_background_color, color_considered_on_hover) :- can_remove(P).

% Next

element(button_container, container, window).
attribute(button_container, "order", 2).
attribute(button_container, height, 100).
attribute(button_container, width, width_value).
attribute(button_container, child_layout, flex).
attribute(button_container, "alignItems", center).
attribute(button_container, "justifyContent", center).


element(button_next, button, button_container).
attribute(button_next, height, 40).
attribute(button_next, width, width_value).
attribute(button_next, label, "Define rooms") :- not setting_rooms.
attribute(button_next, label, "Define People") :- setting_rooms, not room_assigned.
attribute(button_next, label, "Clear Room Assignment") :- setting_rooms, room_assigned.

do(button_next, click, callback, clear_assumptions) :- setting_rooms, room_assigned.
do(button_next, click, callback, set_external(setting_rooms,true)) :- not setting_rooms.
do(button_next, click, callback, set_external(setting_rooms,false)) :- setting_rooms, not room_assigned.

room_assigned :- _c(assign(_,_)).


% Rooms container
element(rooms_main_container, container, window):-setting_rooms.
attribute(rooms_main_container, "order", 3).
attribute(rooms_main_container, width, width_value).
attribute(rooms_main_container, child_layout, grid).

% Room container
element(room(I), container, rooms_main_container) :- room(I,_),setting_rooms.
attribute(room(I), height, 200) :- room(I,_).
attribute(room(I), width, 200) :- room(I,_).
attribute(room(I), grid_column, (I-1)\2) :- room(I,_).
attribute(room(I), grid_row, (I-1)/2) :- room(I,_).
attribute(room(I), child_layout, absstatic) :- room(I,_).

% Room title
element(room_title(I), label, room(I)) :- room(I,_),setting_rooms.
attribute(room_title(I), height, 20) :- room(I,_).
attribute(room_title(I), width, 190) :- room(I,_).
attribute(room_title(I), label, T) :- room(I,T).

% Room beds dropdowns
element(room_dropdown(B,I), dropdown_menu, room(I)) :- bed(B,I),setting_rooms.
attribute(room_dropdown(B,I), selected, P) :- _c(assign(bed(B,I),P)).
attribute(room_dropdown(B,I), height, 30) :- bed(B,I).
attribute(room_dropdown(B,I), selected, P) :- assign(bed(B,I),P), _clinguin_browsing.
attribute(room_dropdown(B,I), width, 100) :- bed(B,I).
attribute(room_dropdown(B,I), pos_y, B*40):- bed(B,I).
do(room_dropdown(B,I), clear, callback, remove_assumption_signature(assign(bed(B,I),any))) :- bed(B,I).

element(mi(B,I,P), dropdown_menu_item, room_dropdown(B,I)) :- _b(assign(bed(B,I),P)),setting_rooms.
attribute(mi(B,I,P), label, P) :- _b(assign(bed(B,I),P)).
do(mi(B,I,P), click, callback, add_assumption(assign(bed(B,I),P))) :- _b(assign(bed(B,I),P)).


