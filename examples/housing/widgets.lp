#show selected/1.

#const n_rooms = 2.

room(1..n_rooms).
person(max).
person(phil).
person(anna).
%person(sus).
%person(tobias).

1{selected(P):person(P)}1.


%{in_house(P):person(P)}.
%{in_house(P)} :- person(P).

1{assign(P,R): room(R), person(P)}1.
1{room_selected(P,I):person(P), room(I)}n_rooms.

warn_more_people :- C=#count{P : person(P), in_house(P)}, C > n_rooms.

element(window, window, root).
#const height_value= 550.
#const width_value= 550.
#const grid_height_value = 450.
#const grid_width_value = 450.

%-----------------------------------
% WARNING
%----------------------------------

element(message, message, window) :- warn_more_people.
attribute(message, title, "WARNING") :- warn_more_people.
attribute(message, message, "There are more people than available rooms specified.") :- warn_more_people.

%---------------------------------------------------------------------------------------
% Window
%---------------------------------------------------------------------------------------

attribute(window, height, height_value).
attribute(window, width, width_value).
attribute(window, background_color, white).
attribute(window, resizable_x, 0).
attribute(window, resizable_y, 0).
attribute(window, child_layout, absstatic).

element(upper_container, container, window).
attribute(upper_container, height, 150).
attribute(upper_container, width, width_value).
attribute(upper_container, background_color, pink).
attribute(upper_container, child_layout, grid).

%---------------------------------------------------------------------------------------
% RIGHT-UPPER
%---------------------------------------------------------------------------------------

element(right_upper_container, container, upper_container).
attribute(right_upper_container, height, 140).
attribute(right_upper_container, width, 275).
attribute(right_upper_container, background_color, blue).
attribute(right_upper_container, grid_column, 1).
attribute(right_upper_container, child_layout, absstatic).

element(right_upper_container_button, container, right_upper_container).
attribute(right_upper_container_button, height, 70).
attribute(right_upper_container_button, width, 100).
attribute(right_upper_container_button, pos_x, 20).
attribute(right_upper_container_button, pos_y, 35).
attribute(right_upper_container_button, background_color, pink).


element(right_upper_label_add(P), label, right_upper_container_button) :- selected(P), not in_house(P).
attribute(right_upper_label_add(P), label, "Add") :- selected(P), not in_house(P).
attribute(right_upper_label_add(P), on_hover, true) :- selected(P), not in_house(P).
attribute(right_upper_label_add(P), on_hover_background_color, "#000fff000") :- selected(P), not in_house(P).
callback(right_upper_label_add(P), click, addAtom(in_house(P))) :- selected(P), not in_house(P).

element(right_upper_label_rmv(P), label, right_upper_container_button) :- selected(P), in_house(P).
attribute(right_upper_label_rmv(P), label, "Remove") :- selected(P), in_house(P).
attribute(right_upper_label_rmv(P), on_hover, true) :- selected(P), in_house(P).
attribute(right_upper_label_rmv(P), on_hover_background_color, "#fff000000") :- selected(P), in_house(P).
callback(right_upper_label_rmv(P), click, removeAtom(in_house(P))) :- selected(P), in_house(P).


element(right_upper_container_dropdown, container, right_upper_container).
attribute(right_upper_container_dropdown, height, 70).
attribute(right_upper_container_dropdown, width, 100).
attribute(right_upper_container_dropdown, pos_x, 140).
attribute(right_upper_container_dropdown, pos_y, 35).
attribute(right_upper_container_dropdown, background_color, green).

% Option Menu
element(right_upper_dropdown, dropdown_menu, right_upper_container_dropdown).
attribute(right_upper_dropdown, selected, V) :- selected(V).

_brave(element(right_upper_dropdown_mi(P), dropdown_menu_item, right_upper_dropdown)) :- person(P).
_brave(attribute(right_upper_dropdown_mi(P), label, P)) :- person(P).
_brave(callback(right_upper_dropdown_mi(P), click, removeAssume(selected(P2), selected(P)))) :- person(P), selected(P2).



%----------------------------------------------------------------------------------------
% LEFT-UPPER
%---------------------------------------------------------------------------------------

element(left_upper_container, container, upper_container).
attribute(left_upper_container, height, 140).
attribute(left_upper_container, width, 275).
attribute(left_upper_container, background_color, green).
attribute(left_upper_container, grid_column, 0).
attribute(left_upper_container, child_layout, absstatic).

element(left_upper_container_label, container, left_upper_container).
attribute(left_upper_container_label, height, 70).
attribute(left_upper_container_label, width, 100).
attribute(left_upper_container_label, pos_x, 0).
attribute(left_upper_container_label, pos_y, 0).
attribute(left_upper_container_label, background_color, pink).
attribute(left_upper_container_label, child_layout, absstatic).

element(l_u_c_l_0, container, left_upper_container_label).
attribute(l_u_c_l_0, height, 70).
attribute(l_u_c_l_0, width, 50).

element(left_upper_label_0, label, l_u_c_l_0).
attribute(left_upper_label_0, label, "Rooms:").

element(l_u_c_l_1, container, left_upper_container_label).
attribute(l_u_c_l_1, height, 70).
attribute(l_u_c_l_1, width, 50).
attribute(l_u_c_l_1, pos_x, 50).
attribute(l_u_c_l_1, pos_y, 0).

element(left_upper_label_1, label, l_u_c_l_1).
attribute(left_upper_label_1, label, n_rooms).

element(l_u_c_l_1, container, left_upper_container_label).
attribute(l_u_c_l_1, height, 70).
attribute(l_u_c_l_1, width, 50).
attribute(l_u_c_l_1, pos_x, 50).
attribute(l_u_c_l_1, pos_y, 0).

element(left_upper_dropdown_container_2, container, left_upper_container).
attribute(left_upper_dropdown_container_2, height, 70).
attribute(left_upper_dropdown_container_2, width, 175).
attribute(left_upper_dropdown_container_2, pos_x, 0).
attribute(left_upper_dropdown_container_2, pos_y, 70).

element(left_upper_dropdown_label, label, left_upper_dropdown_container_2).
attribute(left_upper_dropdown_label, label, "Who is in the house?").


element(left_upper_dropdown_container, container, left_upper_container).
attribute(left_upper_dropdown_container, height, 70).
attribute(left_upper_dropdown_container, width, 100).
attribute(left_upper_dropdown_container, pos_x, 175).
attribute(left_upper_dropdown_container, pos_y, 70).

% Option Menu
element(left_upper_dropdown, dropdown_menu, left_upper_dropdown_container).
attribute(left_upper_dropdown, selected, "Who is in the house?").

element(left_upper_dropdown_mi(P), dropdown_menu_item, left_upper_dropdown) :- person(P), in_house(P).
attribute(left_upper_dropdown_mi(P), label, P) :- person(P), in_house(P).


%-------------------------------------------------------------------------------------------------
% ROOMS
%-------------------------------------------------------------------------------------------------

element(rooms_main_container, container, window).
attribute(rooms_main_container, height, height_value - 150).
attribute(rooms_main_container, width, width_value).
attribute(rooms_main_container, background_color, "#0ffffff00").
attribute(rooms_main_container, pos_x, 0).
attribute(rooms_main_container, pos_y, 150).
attribute(rooms_main_container, child_layout, grid).

element(room(I), container, rooms_main_container) :- room(I).
attribute(room(I), height, 200) :- room(I).
attribute(room(I), width, 200) :- room(I).
attribute(room(I), grid_column, I-1) :- room(I).
attribute(room(I), child_layout, relstatic) :- room(I).
attribute(room(I), border_width, 2) :- room(I).

element(room_title(I), container, room(I)) :- room(I).
attribute(room_title(I), height, 50) :- room(I).
attribute(room_title(I), width, 50) :- room(I).

element(room_title_t(I), label, room_title(I)) :- room(I).
attribute(room_title_t(I), label, "Room") :- room(I).

element(room_title_2(I), container, room(I)) :- room(I).
attribute(room_title_2(I), height, 50) :- room(I).
attribute(room_title_2(I), width, 50) :- room(I).
attribute(room_title_2(I), pos_x, 25) :- room(I).

element(room_title_t_2(I), label, room_title_2(I)) :- room(I).
attribute(room_title_t_2(I), label, I) :- room(I).

element(room_dropdown_c(I), container, room(I)) :- room(I).
attribute(room_dropdown_c(I), height, 50) :- room(I).
attribute(room_dropdown_c(I), width, 100) :- room(I).
attribute(room_dropdown_c(I), pos_y, 50) :- room(I).
attribute(room_dropdown_c(I), pos_x, 25) :- room(I).
attribute(room_dropdown_c(I), background_color, "#f0f0f0f0f") :- room(I).

% Option Menu
element(room_dropdown(I), dropdown_menu, room_dropdown_c(I)) :- room(I).
attribute(room_dropdown(I), selected, P) :- room_selected(P,I).

somewhere_selected(P) :- person(P), C=#count{P,R : room(R), not room_selected(P,R)}, C<n_rooms.

_brave(element(left_upper_dropdown_mi(I,P), dropdown_menu_item, room_dropdown(I))) :- room(I), assign(P,I), in_house(P), not somewhere_selected(P).
_brave(attribute(left_upper_dropdown_mi(I,P), label, P)) :- room(I), assign(P,I), in_house(P), not somewhere_selected(P).
_brave(callback(left_upper_dropdown_mi(I,P), click, assume(room_selected(P,I)))) :- room(I), assign(P,I), in_house(P), not somewhere_selected(P).

















