% #const color_considered = "#C1E5AE".
% #const color_considered_on_hover = "#6cc13e".
% #const color_not_considered = "#E5C2AE".
% #const color_not_considered_on_hover = "#c16e3e".
#const width_value= 400.


% Window
element(window, window, root).
attribute(window, width, width_value).
attribute(window, child_layout, flex).
attribute(window, flex_direction, column).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MODAL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

element(modal, modal, window).
attribute(modal, title, "Add person").

element(c1, container, modal).
attribute(c1, child_layout, flex).
attribute(c1, flex_direction, row_reverse).

element(t1, textfield, c1).
attribute(t1, placeholder, "Enter the name of the person").
attribute(t1, width, 250).
do(t1, input, context, (t1_content, _value)).

element(b1, button, c1).
do(b1, click, callback, add_atom(person(_value_context(t1_content)))).
attribute(b1, label, "Add").
attribute(b1, class, "btn-light").
attribute(b1, icon, "fa-plus").

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Error message
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

room_assigned :- _c(assign(_,_)).
adding_people_not_possible :- room_assigned.
adding_people_not_possible :- setting_rooms.

element(message_impossible_op,message,window):- adding_people_not_possible.
attribute(message_impossible_op,title,"Invalid Operation!"):- adding_people_not_possible.
attribute(message_impossible_op,message,"Adding people only possible while in room-defining mode"):- adding_people_not_possible.
attribute(message_impossible_op,type,error):- adding_people_not_possible.
attribute(message_impossible_op,visible,hidden) :- adding_people_not_possible.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% List of people
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

element(add_button, button, window).
attribute(add_button, icon, "fa-user-plus").
attribute(add_button, class, "btn-light").
attribute(add_button, class, "border-info").
do(add_button, click, update, (modal, visible, shown)) :- not room_assigned, not setting_rooms.
do(add_button, click, update, (message_impossible_op, visible, shown)) :- adding_people_not_possible.

% Top container
element(upper_container, container, window).
attribute(upper_container, order, 1).
attribute(upper_container, class, "rounded").
attribute(upper_container, class, "bg-light").
attribute(upper_container, width, width_value).
% attribute(upper_container, child_layout, grid).

% People to add to the house
can_add(P):-person(P), not in_house(P).
element(person_add(P), label, upper_container):- can_add(P).
attribute(person_add(P), label, P) :- can_add(P).
attribute(person_add(P), class, "text-danger") :- can_add(P).
do(person_add(P), click, callback, set_external(in_house(P),true)):- can_add(P), not setting_rooms.

% People to remove from the house
can_remove(P):- in_house(P).
element(person_remove(P), label, upper_container):- can_remove(P).
attribute(person_remove(P), label, P) :- can_remove(P).
attribute(person_remove(P), class, "text-success") :- can_remove(P).
do(person_remove(P), click, callback, set_external(in_house(P),false)):-can_remove(P), not setting_rooms.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Next step button
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Next
element(button_container, container, window).
attribute(button_container, order, 2).
attribute(button_container, height, 100).
attribute(button_container, width, width_value).
attribute(button_container, child_layout, flex).
attribute(button_container, "alignItems", center).
attribute(button_container, "justifyContent", center).


element(button_next, button, button_container).
attribute(button_next, class, "btn-secondary").
attribute(button_next, height, 40).
attribute(button_next, width, width_value).
attribute(button_next, icon, "fa-arrow-down-up-across-line").
attribute(button_next, label, "Define rooms") :- not setting_rooms.
attribute(button_next, label, "Define people") :- setting_rooms.

% do(button_next, click, callback, clear_assumptions) :- setting_rooms, room_assigned.
do(button_next, click, callback, set_external(setting_rooms,true)) :- not setting_rooms.
do(button_next, click, callback, set_external(setting_rooms,false)) :- setting_rooms.



% Rooms container
element(rooms_main_container, container, window):-setting_rooms.
attribute(rooms_main_container, order, 3).
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
attribute(room_title(I), class, "text-uppercase") :- room(I,_).
attribute(room_title(I), width, 190) :- room(I,_).
attribute(room_title(I), label, T) :- room(I,T).

% Room beds dropdowns
element(room_dropdown(B,I), dropdown_menu, room(I)) :- bed(B,I),setting_rooms.
attribute(room_dropdown(B,I), class, "btn-sm") :- bed(B,I),setting_rooms.
attribute(room_dropdown(B,I), selected, P) :- _c(assign(bed(B,I),P)).
% attribute(room_dropdown(B,I), height, 30) :- bed(B,I).
attribute(room_dropdown(B,I), selected, P) :- assign(bed(B,I),P), _clinguin_browsing.
% attribute(room_dropdown(B,I), width, 100) :- bed(B,I).
attribute(room_dropdown(B,I), pos_y, B*40):- bed(B,I).
do(room_dropdown(B,I), clear, callback, remove_assumption_signature(assign(bed(B,I),any))) :- bed(B,I).

element(mi(B,I,P), dropdown_menu_item, room_dropdown(B,I)) :- _b(assign(bed(B,I),P)),setting_rooms.
attribute(mi(B,I,P), label, P) :- _b(assign(bed(B,I),P)).
do(mi(B,I,P), click, callback, add_assumption(assign(bed(B,I),P))) :- _b(assign(bed(B,I),P)).







element(menu_bar, menu_bar, window).
element(menu_bar_clear, button, menu_bar).
attribute(menu_bar_clear, label, "Clear").
attribute(menu_bar_clear, icon, "fa-trash").
attribute(menu_bar_clear, class, "btn-outline-danger").
do(menu_bar_clear, click, callback, clear_assumptions).


element(menu_bar_select, button, menu_bar).
attribute(menu_bar_select, label, "Select solution").
attribute(menu_bar_select, class, "btn-outline-secondary").
% attribute(menu_bar_select, class, "btn-outline-warning").
attribute(menu_bar_select, icon, "fa-hand-pointer").
attribute(menu_bar_select, icon, "fa-duotone").
do(menu_bar_select, click, callback, select).

element(menu_bar_next_opt, button, menu_bar).
attribute(menu_bar_next_opt, label, "Next Optimal").
attribute(menu_bar_next_opt, icon, "fa-forward-fast").
% attribute(menu_bar_next_opt, class, "btn-outline-success").
attribute(menu_bar_next_opt, class, "btn-outline-secondary").
do(menu_bar_next_opt, click, callback, next_solution(optN)).

element(menu_bar_next, button, menu_bar).
attribute(menu_bar_next, label, "Next").
attribute(menu_bar_next, icon, "fa-forward-step").
attribute(menu_bar_next, class, "btn-outline-primary").
do(menu_bar_next, click, callback, next_solution).

