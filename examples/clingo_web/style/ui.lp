elem(window, window, root).
% attr(window, child_layout, flex).
% attr(window, flex_direction, column).

% ---------
% Menu bar
% ---------
elem(menu_bar, menu_bar, window).
attr(menu_bar, title, "My app").
attr(menu_bar, icon, "fa-home").

elem(menu_bar_clear, button, menu_bar).
attr(menu_bar_clear, label, "Clear").
attr(menu_bar_clear, icon, "fa-trash").
attr(menu_bar_clear, class, "btn-outline-danger").
attr(menu_bar_clear, class, "border-0").
when(menu_bar_clear, click, callback, clear_assumptions).


elem(menu_bar_select, button, menu_bar).
attr(menu_bar_select, label, "Select solution").
attr(menu_bar_select, class, "btn-outline-dark").
attr(menu_bar_select, class, "border-0").
attr(menu_bar_select, icon, "fa-hand-pointer").
when(menu_bar_select, click, callback, select).

elem(menu_bar_next_opt, button, menu_bar).
attr(menu_bar_next_opt, label, "Next Optimal").
attr(menu_bar_next_opt, icon, "fa-forward-fast").
attr(menu_bar_next_opt, class, "btn-outline-dark").
attr(menu_bar_next_opt, class, "border-0").
when(menu_bar_next_opt, click, callback, next_solution(optN)).

elem(menu_bar_next, button, menu_bar).
attr(menu_bar_next, label, "Next").
attr(menu_bar_next, icon, "fa-forward-step").
attr(menu_bar_next, class, "btn-outline-dark").
attr(menu_bar_next, class, "border-0").
when(menu_bar_next, click, callback, next_solution).


% ---------
% Containers
% ---------

elem(c1, container, window).
attr(c1, child_layout, flex).
attr(c1, flex_direction, row).
attr(c1, class, "border").
attr(c1, class, "border-3").
attr(c1, class, "rounded").
attr(c1, class, "border-primary").

elem(c2, container, window).
attr(c2, class, "border").
attr(c2, class, "border-info").
attr(c2, class, "bg-light").
attr(c2, class, "m-1").
attr(c2, class, "p-2").
attr(c2, class, "rounded").
attr(c2, child_layout, flex).
attr(c2, flex_direction, row).

% ---------
% Buttons C1
% ---------
elem(b1, button, c1).
attr(b1, class, "btn-primary").
attr(b1, class, "m-2").
attr(b1, class, "btn-sm").
attr(b1, label, "btn-primary").
elem(b2, button, c1).
attr(b2, class, "btn-secondary").
attr(b2, class, "m-2").
attr(b2, class, "btn-sm").
attr(b2, label, "btn-secondary").
elem(b3, button, c1).
attr(b3, class, "btn-success").
attr(b3, class, "m-2").
attr(b3, class, "btn-sm").
attr(b3, label, "btn-success").
elem(b4, button, c1).
attr(b4, class, "btn-danger").
attr(b4, class, "m-2").
attr(b4, class, "btn-sm").
attr(b4, label, "btn-danger").
elem(b5, button, c1).
attr(b5, class, "btn-warning").
attr(b5, class, "m-2").
attr(b5, class, "btn-sm").
attr(b5, label, "btn-warning").
elem(b6, button, c1).
attr(b6, class, "btn-info").
attr(b6, class, "m-2").
attr(b6, class, "btn-sm").
attr(b6, label, "btn-info").
elem(b7, button, c1).
attr(b7, class, "btn-light").
attr(b7, class, "m-2").
attr(b7, class, "btn-sm").
attr(b7, label, "btn-light").
elem(b8, button, c1).
attr(b8, class, "btn-dark").
attr(b8, class, "m-2").
attr(b8, class, "btn-sm").
attr(b8, label, "btn-dark").

% ---------
% Buttons C2
% ---------
elem(b1o, button, c2).
attr(b1o, class, "btn-outline-primary").
attr(b1o, label, "btn-outline-primary").
elem(b2o, button, c2).
attr(b2o, class, "btn-outline-secondary").
attr(b2o, label, "btn-outline-secondary").
elem(b3o, button, c2).
attr(b3o, class, "btn-outline-success").
attr(b3o, label, "btn-outline-success").
elem(b4o, button, c2).
attr(b4o, class, "btn-outline-danger").
attr(b4o, label, "btn-outline-danger").
elem(b5o, button, c2).
attr(b5o, class, "btn-outline-warning").
attr(b5o, label, "btn-outline-warning").
elem(b6o, button, c2).
attr(b6o, class, "btn-outline-info").
attr(b6o, label, "btn-outline-info").
elem(b7o, button, c2).
attr(b7o, class, "btn-outline-light").
attr(b7o, label, "btn-outline-light").
elem(b8o, button, c2).
attr(b8o, class, "btn-outline-dark").
attr(b8o, label, "btn-outline-dark").



% ---------
% Labels C3
% ---------

elem(c3, container, window).
attr(c3, class, "border").
attr(c3, class, "border-info").
attr(c3, class, "text-primary").
attr(c3, class, "p-2").
attr(c3, class, "justify-content-end").
attr(c3, class, "flex-row").


elem(l1, label, c3).
attr(l1, label, "This is some label taking the color from the container class").

elem(l2, label, c3).
attr(l2, label, "This label overwrites the color").
attr(l2, class, "text-danger").
attr(l2, class, "text-capitalize").


% ---------
% Dropdowns C4
% ---------

elem(c6, container, window).
attr(c6, class, "border").
attr(c6, class, "border-dark").
attr(c6, height, "200").
attr(c6, child_layout, flex).
attr(c6, flex_direction, row).

elem(c4, container, c6).
attr(c4, class, "bg-info").
attr(c4, class, "w-75").
attr(c4, class, "h-100").
attr(c4, class, "align-items-start").
attr(c4, class, "opacity-25").
% attr(c4, flex_direction, "row").
elem(c5, container, c6).
attr(c5, class, "bg-success").
attr(c5, class, "w-25").
attr(c5, class, "h-100").
attr(c5, class, "bg-opacity-50").

elem(dd1, dropdown_menu, c4).
attr(dd1, class, "btn-warning").
attr(dd1, class, "m-4").
elem(dd1_1, dropdown_menu_item, dd1).
attr(dd1_1, label, "1").
elem(dd1_2, dropdown_menu_item, dd1).
attr(dd1_2, label, "2").

elem(dd2, dropdown_menu, c4).
attr(dd2, class, "btn-warning").
attr(dd2, class, "m-4").
elem(dd2_1, dropdown_menu_item, dd2).
attr(dd2_1, label, "1").
elem(dd2_2, dropdown_menu_item, dd2).
attr(dd2_2, label, "2").


elem(dd3, dropdown_menu, c5).
attr(dd3, class, "btn-light").
attr(dd3, selected, "Choose a value").
elem(dd3_1, dropdown_menu_item, dd3).
attr(dd3_1, label, "INVALID").
attr(dd3_1, class, "text-danger").
attr(dd3_1, order, 1).
elem(dd3_2, dropdown_menu_item, dd3).
attr(dd3_2, label, "Valid").
attr(dd3_2, class, "text-uppercase").
attr(dd3_2, class, "text-success").