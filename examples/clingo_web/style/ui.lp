element(window, window, root).
% attribute(window, child_layout, flex).
% attribute(window, flex_direction, column).

% ---------
% Menu bar
% ---------
element(menu_bar, menu_bar, window).
attribute(menu_bar, title, "My app").
attribute(menu_bar, icon, "fa-home").

element(menu_bar_clear, button, menu_bar).
attribute(menu_bar_clear, label, "Clear").
attribute(menu_bar_clear, icon, "fa-trash").
attribute(menu_bar_clear, class, "btn-outline-danger").
attribute(menu_bar_clear, class, "border-0").
do(menu_bar_clear, click, callback, clear_assumptions).


element(menu_bar_select, button, menu_bar).
attribute(menu_bar_select, label, "Select solution").
attribute(menu_bar_select, class, "btn-outline-dark").
attribute(menu_bar_select, class, "border-0").
attribute(menu_bar_select, icon, "fa-hand-pointer").
do(menu_bar_select, click, callback, select).

element(menu_bar_next_opt, button, menu_bar).
attribute(menu_bar_next_opt, label, "Next Optimal").
attribute(menu_bar_next_opt, icon, "fa-forward-fast").
attribute(menu_bar_next_opt, class, "btn-outline-dark").
attribute(menu_bar_next_opt, class, "border-0").
do(menu_bar_next_opt, click, callback, next_solution(optN)).

element(menu_bar_next, button, menu_bar).
attribute(menu_bar_next, label, "Next").
attribute(menu_bar_next, icon, "fa-forward-step").
attribute(menu_bar_next, class, "btn-outline-dark").
attribute(menu_bar_next, class, "border-0").
do(menu_bar_next, click, callback, next_solution).


% ---------
% Containers
% ---------

element(c1, container, window).
attribute(c1, child_layout, flex).
attribute(c1, flex_direction, row).
attribute(c1, class, "border").
attribute(c1, class, "border-3").
attribute(c1, class, "rounded").
attribute(c1, class, "border-primary").

element(c2, container, window).
attribute(c2, class, "border").
attribute(c2, class, "border-info").
attribute(c2, class, "bg-light").
attribute(c2, class, "m-1").
attribute(c2, class, "p-2").
attribute(c2, class, "rounded").
attribute(c2, child_layout, flex).
attribute(c2, flex_direction, row).

% ---------
% Buttons C1
% ---------
element(b1, button, c1).
attribute(b1, class, "btn-primary").
attribute(b1, class, "m-2").
attribute(b1, class, "btn-sm").
attribute(b1, label, "btn-primary").
element(b2, button, c1).
attribute(b2, class, "btn-secondary").
attribute(b2, class, "m-2").
attribute(b2, class, "btn-sm").
attribute(b2, label, "btn-secondary").
element(b3, button, c1).
attribute(b3, class, "btn-success").
attribute(b3, class, "m-2").
attribute(b3, class, "btn-sm").
attribute(b3, label, "btn-success").
element(b4, button, c1).
attribute(b4, class, "btn-danger").
attribute(b4, class, "m-2").
attribute(b4, class, "btn-sm").
attribute(b4, label, "btn-danger").
element(b5, button, c1).
attribute(b5, class, "btn-warning").
attribute(b5, class, "m-2").
attribute(b5, class, "btn-sm").
attribute(b5, label, "btn-warning").
element(b6, button, c1).
attribute(b6, class, "btn-info").
attribute(b6, class, "m-2").
attribute(b6, class, "btn-sm").
attribute(b6, label, "btn-info").
element(b7, button, c1).
attribute(b7, class, "btn-light").
attribute(b7, class, "m-2").
attribute(b7, class, "btn-sm").
attribute(b7, label, "btn-light").
element(b8, button, c1).
attribute(b8, class, "btn-dark").
attribute(b8, class, "m-2").
attribute(b8, class, "btn-sm").
attribute(b8, label, "btn-dark").

% ---------
% Buttons C2
% ---------
element(b1o, button, c2).
attribute(b1o, class, "btn-outline-primary").
attribute(b1o, label, "btn-outline-primary").
element(b2o, button, c2).
attribute(b2o, class, "btn-outline-secondary").
attribute(b2o, label, "btn-outline-secondary").
element(b3o, button, c2).
attribute(b3o, class, "btn-outline-success").
attribute(b3o, label, "btn-outline-success").
element(b4o, button, c2).
attribute(b4o, class, "btn-outline-danger").
attribute(b4o, label, "btn-outline-danger").
element(b5o, button, c2).
attribute(b5o, class, "btn-outline-warning").
attribute(b5o, label, "btn-outline-warning").
element(b6o, button, c2).
attribute(b6o, class, "btn-outline-info").
attribute(b6o, label, "btn-outline-info").
element(b7o, button, c2).
attribute(b7o, class, "btn-outline-light").
attribute(b7o, label, "btn-outline-light").
element(b8o, button, c2).
attribute(b8o, class, "btn-outline-dark").
attribute(b8o, label, "btn-outline-dark").



% ---------
% Labels C3
% ---------

element(c3, container, window).
attribute(c3, class, "border").
attribute(c3, class, "border-info").
attribute(c3, class, "text-primary").
attribute(c3, class, "p-2").
attribute(c3, class, "justify-content-end").
attribute(c3, class, "flex-row").


element(l1, label, c3).
attribute(l1, label, "This is some label taking the color from the container class").

element(l2, label, c3).
attribute(l2, label, "This label overwrites the color").
attribute(l2, class, "text-danger").
attribute(l2, class, "text-capitalize").


% ---------
% Dropdowns C4
% ---------

element(c6, container, window).
attribute(c6, class, "border").
attribute(c6, class, "border-dark").
attribute(c6, height, "200").
attribute(c6, child_layout, flex).
attribute(c6, flex_direction, row).

element(c4, container, c6).
attribute(c4, class, "bg-info").
attribute(c4, class, "w-75").
attribute(c4, class, "h-100").
attribute(c4, class, "align-items-start").
attribute(c4, class, "opacity-25").
% attribute(c4, flex_direction, "row").
element(c5, container, c6).
attribute(c5, class, "bg-success").
attribute(c5, class, "w-25").
attribute(c5, class, "h-100").
attribute(c5, class, "bg-opacity-50").

element(dd1, dropdown_menu, c4).
attribute(dd1, class, "btn-warning").
attribute(dd1, class, "m-4").
element(dd1_1, dropdown_menu_item, dd1).
attribute(dd1_1, label, "1").
element(dd1_2, dropdown_menu_item, dd1).
attribute(dd1_2, label, "2").

element(dd2, dropdown_menu, c4).
attribute(dd2, class, "btn-warning").
attribute(dd2, class, "m-4").
element(dd2_1, dropdown_menu_item, dd2).
attribute(dd2_1, label, "1").
element(dd2_2, dropdown_menu_item, dd2).
attribute(dd2_2, label, "2").


element(dd3, dropdown_menu, c5).
attribute(dd3, class, "btn-light").
attribute(dd3, selected, "Choose a value").
element(dd3_1, dropdown_menu_item, dd3).
attribute(dd3_1, label, "INVALID").
attribute(dd3_1, class, "text-danger").
attribute(dd3_1, order, 1).
element(dd3_2, dropdown_menu_item, dd3).
attribute(dd3_2, label, "Valid").
attribute(dd3_2, class, "text-uppercase").
attribute(dd3_2, class, "text-success").