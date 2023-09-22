element(window, window, root).
% attribute(window, child_layout, flex).
% attribute(window, flex_direction, column).

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


element(default, button, window).
attribute(default, label, "Default").

% element(special, button, window).
% attribute(special, label, "Special").
% attribute(special, class, "btn-light").
% attribute(special, class, "border-info").

% element(special2, button, window).
% attribute(special2, label, "Special").
% attribute(special2, class, "btn-info").
% attribute(special2, class, "border-primary").

element(b1, button, window).
attribute(b1, class, "btn-primary").
attribute(b1, label, "Primary").
element(b2, button, window).
attribute(b2, class, "btn-secondary").
attribute(b2, label, "Secondary").
element(b3, button, window).
attribute(b3, class, "btn-success").
attribute(b3, label, "Success").
element(b4, button, window).
attribute(b4, class, "btn-danger").
attribute(b4, label, "Danger").
element(b5, button, window).
attribute(b5, class, "btn-warning").
attribute(b5, label, "Warning").
element(b6, button, window).
attribute(b6, class, "btn-info").
attribute(b6, label, "Info").
element(b7, button, window).
attribute(b7, class, "btn-light").
attribute(b7, label, "Light").
element(b8, button, window).
attribute(b8, class, "btn-dark").
attribute(b8, label, "Dark").


element(b1o, button, window).
attribute(b1o, class, "btn-outline-primary").
attribute(b1o, label, "Primary").
element(b2o, button, window).
attribute(b2o, class, "btn-outline-secondary").
attribute(b2o, label, "Secondary").
element(b3o, button, window).
attribute(b3o, class, "btn-outline-success").
attribute(b3o, label, "Success").
element(b4o, button, window).
attribute(b4o, class, "btn-outline-danger").
attribute(b4o, label, "Danger").
element(b5o, button, window).
attribute(b5o, class, "btn-outline-warning").
attribute(b5o, label, "Warning").
element(b6o, button, window).
attribute(b6o, class, "btn-outline-info").
attribute(b6o, label, "Info").
element(b7o, button, window).
attribute(b7o, class, "btn-outline-light").
attribute(b7o, label, "Light").
element(b8o, button, window).
attribute(b8o, class, "btn-outline-dark").
attribute(b8o, label, "Dark").

