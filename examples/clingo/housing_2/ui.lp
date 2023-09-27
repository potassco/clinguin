#const color_considered = "#C1E5AE".
#const color_considered_on_hover = "#6cc13e".
#const color_not_considered = "#E5C2AE".
#const color_not_considered_on_hover = "#c16e3e".
#const width_value= 400.


% Window
elem(window, window, root).
attr(window, width, width_value).
attr(window, background_color, white).
attr(window, resizable_x, 1).
attr(window, resizable_y, 1).
attr(window, child_layout, flex).
attr(window, flex_direction, column).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MODAL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(modal, modal, window).
attr(modal, title, "Edit People").

elem(c1, container, modal).
attr(c1, pos_x, 0).
attr(c1, pos_y, 0).
attr(c1, height, 200).
attr(c1, width, 500).
attr(c1, child_layout, flex).
attr(c1, flex_direction, row_reverse).

elem(t1, textfield, c1).
attr(t1, placeholder, "Please enter the name of the person.").
%attr(t1, input_type, number).
when(t1, type, context, (t1_content, _value)).

elem(b1, button, c1).
when(b1, click, callback, add_atom(person(_context_value(t1_content)))).
attr(b1, label, "Add Person").

elem(c2, container, modal).
attr(c2, pos_x, 0).
attr(c2, pos_y, 250).
attr(c2, height, 200).
attr(c2, width, 500).
attr(c2, child_layout, flex).
attr(c2, flex_direction, column).

elem(c3(X), container, c2) :- person(X).
attr(c3(X), child_layout, flex) :- person(X).
attr(c3(X), flex_direction, row) :- person(X).

elem(l(X), label, c3(X)) :- person(X).
attr(l(X), label, X) :- person(X).
attr(l(X), background_color, "#00ff00") :- person(X).

elem(b(X), button, c3(X)) :- person(X).
attr(b(X), label, "Remove Name") :- person(X).
when(b(X), click, callback, remove_atom(person(X))) :- person(X).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar is defined automatically called _default_menu_bar with one section _default_menu_bar_section
% These lines only add an extra option
elem(_default_menu_bar_section_next_opt, menu_bar_section_item, _default_menu_bar_section).
attr(_default_menu_bar_section_next_opt, label, "Next Optimal").
when(_default_menu_bar_section_next_opt, click, callback, next_solution(optN)).

elem(menu_bar_section_2, menu_bar_section, _default_menu_bar).
attr(menu_bar_section_2, label, "Edit Persons").
when(menu_bar_section_2, click, update, (modal, visible, shown)) :- not room_assigned, not setting_rooms.
when(menu_bar_section_2, click, update, (message_impossible_op, visible, shown)) :- adding_people_not_possible.

adding_people_not_possible :- room_assigned.
adding_people_not_possible :- setting_rooms.

elem(message_impossible_op,message,window):- adding_people_not_possible.
attr(message_impossible_op,title,"Invalid Operation!"):- adding_people_not_possible.
attr(message_impossible_op,message,"Adding people only possible while not in room-defining mode and no people asisgned."):- adding_people_not_possible.
attr(message_impossible_op,type,error):- adding_people_not_possible.
attr(message_impossible_op,visible,hidden) :- adding_people_not_possible.


% Top container
elem(upper_container, container, window).
attr(upper_container, "order", 1).
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

% Add and remove columns
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
when(person_add(P), click, callback, set_external(in_house(P),true)):- can_add(P), not setting_rooms.
attr(person_add(P), on_hover, true) :- can_add(P).
attr(person_add(P), on_hover_background_color, color_not_considered_on_hover) :- can_add(P).

% People to remove from the house
can_remove(P):- in_house(P).
elem(person_remove(P), label, remove_person_container):- can_remove(P).
attr(person_remove(P), label, P) :- can_remove(P).
attr(person_remove(P), background_color, color_considered) :- can_remove(P).
when(person_remove(P), click, callback, set_external(in_house(P),false)):-can_remove(P), not setting_rooms.
attr(person_remove(P), on_hover, true) :- can_remove(P).
attr(person_remove(P), on_hover_background_color, color_considered_on_hover) :- can_remove(P).

% Next

elem(button_container, container, window).
attr(button_container, "order", 2).
attr(button_container, height, 100).
attr(button_container, width, width_value).
attr(button_container, child_layout, flex).
attr(button_container, "alignItems", center).
attr(button_container, "justifyContent", center).


elem(button_next, button, button_container).
attr(button_next, height, 40).
attr(button_next, width, width_value).
attr(button_next, label, "Define rooms") :- not setting_rooms.
attr(button_next, label, "Define People") :- setting_rooms, not room_assigned.
attr(button_next, label, "Clear Room Assignment") :- setting_rooms, room_assigned.

when(button_next, click, callback, clear_assumptions) :- setting_rooms, room_assigned.
when(button_next, click, callback, set_external(setting_rooms,true)) :- not setting_rooms.
when(button_next, click, callback, set_external(setting_rooms,false)) :- setting_rooms, not room_assigned.

room_assigned :- _c(assign(_,_)).


% Rooms container
elem(rooms_main_container, container, window):-setting_rooms.
attr(rooms_main_container, "order", 3).
attr(rooms_main_container, width, width_value).
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
when(room_dropdown(B,I), clear, callback, remove_assumption_signature(assign(bed(B,I),any))) :- bed(B,I).

elem(mi(B,I,P), dropdown_menu_item, room_dropdown(B,I)) :- _b(assign(bed(B,I),P)),setting_rooms.
attr(mi(B,I,P), label, P) :- _b(assign(bed(B,I),P)).
when(mi(B,I,P), click, callback, add_assumption(assign(bed(B,I),P))) :- _b(assign(bed(B,I),P)).


