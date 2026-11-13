
% ============================================================
% PIGEONHOLE ASSIGNMENT - CLINGUIN V3
% ============================================================

#include "menu-bar.lp".

% ============================================================
% FRAMEWORK SCAFFOLD
% ============================================================

elem(ui_app, div, root).
attr(ui_app, class,
    ("min-h-screen"; "flex"; "flex-col";
     "bg-background"; "text-foreground")).

elem(ui_content, main, ui_app).
attr(ui_content, class,
    ("flex"; "min-h-0"; "grow"; "flex-col")).
attr(ui_content, order, 100).


% ============================================================
% APPLICATION UI
% ============================================================


% ============================================================
% 1. DERIVED FACTS
% ============================================================

assumed(P,B) :-
    pigeon(P), box(B),
    _clinguin_assume(in(P,B), true).

locked_pigeon(P) :-
    assumed(P,_).

% Show explicitly assumed assignments, including during UNSAT.
shown_assignment(P,B) :-
    assumed(P,B).

% Show assignments that hold in all models.
shown_assignment(P,B) :-
    pigeon(P), box(B),
    _all(in(P,B)),
    not _clinguin_unsat.

% Show assignments in the currently browsed solution.
shown_assignment(P,B) :-
    pigeon(P), box(B),
    in(P,B),
    _clinguin_browsing,
    not _clinguin_unsat.

% Candidate assignments.
available(B,P) :-
    box(B),
    pigeon(P),
    _any(in(P,B)),
    not _all(in(P,B)),
    not locked_pigeon(P),
    not _clinguin_unsat.

has_available(B) :-
    available(B,_).

% Statistics.
n_locked(N) :-
    N = #count { P : locked_pigeon(P) }.

n_pigeons(N) :-
    N = #count { P : pigeon(P) }.

n_boxes_used(N) :-
    N = #count { B : shown_assignment(_,B) }.

all_locked :-
    n_locked(N),
    n_pigeons(N),
    N > 0.

% Solver states.
status(unsat) :-
    _clinguin_unsat.

status(browsing) :-
    _clinguin_browsing,
    not _clinguin_unsat.

status(complete) :-
    all_locked,
    not _clinguin_browsing,
    not _clinguin_unsat.

status(ready) :-
    not all_locked,
    not _clinguin_browsing,
    not _clinguin_unsat.


% ============================================================
% 2. HEADER AND MENU BAR
% ============================================================

menubar_title_override("Pigeonhole Assignment").
menubar_subtitle_override("One pigeon per box").
menubar_icon_override("Bird").

% Tools dropdown.
elem(tools_menu, dropdown_menu, menubar_right).
attr(tools_menu, order, 1).

elem(tools_trigger, dropdown_menu(trigger), tools_menu).
attr(tools_trigger, text, "Tools").
attr(tools_trigger, class,
    ("inline-flex"; "items-center"; "rounded-md";
     "border"; "px-3"; "py-2"; "text-sm";
     "font-medium")).

elem(tools_content, dropdown_menu(content), tools_menu).
attr(tools_content, class, "w-52").
attr(tools_content, align, "end").

elem(tools_label, dropdown_menu(label), tools_content).
attr(tools_label, text, "Actions").
attr(tools_label, order, 1).

% Clear assumptions.
elem(clear_item, dropdown_menu(item), tools_content).
attr(clear_item, text, "Clear assignments").
attr(clear_item, order, 2).

when(clear_item, click, call, clear_assumptions).

% Restart application.
elem(restart_item, dropdown_menu(item), tools_content).
attr(restart_item, text, "Restart application").
attr(restart_item, class, "text-destructive").
attr(restart_item, order, 3).

when(restart_item, click, call, restart).

% Theme toggle.
elem(theme_switch, theme_toggle, menubar_right).
attr(theme_switch, order, 2).
attr(theme_switch, variant, "outline").
attr(theme_switch, size, "sm").


% ============================================================
% 3. MAIN PAGE
% ============================================================

elem(app_page, div, ui_content).
attr(app_page, class,
    ("mx-auto"; "flex"; "w-full"; "max-w-6xl";
     "flex-col"; "gap-5"; "p-4"; "sm:p-6")).


% ============================================================
% 4. STATISTICS BAR
% ============================================================

stat(locked,  "Lock",    "Locked",     1).
stat(pigeons, "Bird",    "Pigeons",    2).
stat(boxes,   "Package", "Boxes used", 3).

elem(stats_bar, section, app_page).
attr(stats_bar, class,
    ("grid"; "grid-cols-1"; "gap-3"; "sm:grid-cols-3")).
attr(stats_bar, order, 1).

elem(stat_card(K), div, stats_bar) :-
    stat(K,_,_,_).

attr(stat_card(K), class,
    ("flex"; "items-center"; "gap-3"; "rounded-lg";
     "border"; "bg-card"; "p-4")) :-
    stat(K,_,_,_).

attr(stat_card(K), order, O) :-
    stat(K,_,_,O).

% Statistic icon.
elem(stat_icon(K), icon, stat_card(K)) :-
    stat(K,_,_,_).

attr(stat_icon(K), icon, I) :-
    stat(K,I,_,_).

attr(stat_icon(K), class, "text-muted-foreground") :-
    stat(K,_,_,_).

% Statistic information.
elem(stat_info(K), div, stat_card(K)) :-
    stat(K,_,_,_).

attr(stat_info(K), class,
    ("flex"; "flex-col"; "min-w-0")) :-
    stat(K,_,_,_).

% Statistic value.
elem(stat_value(K), span, stat_info(K)) :-
    stat(K,_,_,_).

attr(stat_value(K), class,
    ("text-2xl"; "font-semibold")) :-
    stat(K,_,_,_).

attr(stat_value(locked), text, N) :-
    n_locked(N).

attr(stat_value(pigeons), text, N) :-
    n_pigeons(N).

attr(stat_value(boxes), text, N) :-
    n_boxes_used(N).

% Statistic label.
elem(stat_label(K), span, stat_info(K)) :-
    stat(K,_,_,_).

attr(stat_label(K), text, L) :-
    stat(K,_,L,_).

attr(stat_label(K), class,
    ("text-sm"; "text-muted-foreground")) :-
    stat(K,_,_,_).


% ============================================================
% 5. BOXES BOARD
% ============================================================

elem(board_section, section, app_page).
attr(board_section, class,
    ("flex"; "flex-col"; "gap-3")).
attr(board_section, order, 2).

elem(board_title, h2, board_section).
attr(board_title, text, "Boxes").
attr(board_title, class,
    ("text-lg"; "font-semibold")).

elem(board, div, board_section).
attr(board, class,
    ("grid"; "grid-cols-1"; "gap-3";
     "sm:grid-cols-2"; "lg:grid-cols-3";
     "xl:grid-cols-5")).


% ============================================================
% 6. BOX CARDS
% ============================================================

elem(box_card(B), article, board) :-
    box(B).

attr(box_card(B), class,
    ("flex"; "min-w-0"; "flex-col"; "gap-3";
     "rounded-lg"; "border"; "bg-card";
     "p-3"; "shadow-sm")) :-
    box(B).

attr(box_card(B), order, B) :-
    box(B).

% Box header.
elem(box_header(B), div, box_card(B)) :-
    box(B).

attr(box_header(B), class,
    ("flex"; "items-center";
     "justify-between"; "gap-2")) :-
    box(B).

% Box title.
elem(box_title(B), h3, box_header(B)) :-
    box(B).

attr(box_title(B), class,
    ("flex"; "items-center"; "gap-1";
     "text-sm"; "font-semibold")) :-
    box(B).

elem(box_icon(B), icon, box_title(B)) :-
    box(B).

attr(box_icon(B), icon, "Package") :-
    box(B).

elem(box_prefix(B), span, box_title(B)) :-
    box(B).

attr(box_prefix(B), text, "Box") :-
    box(B).

elem(box_number(B), span, box_title(B)) :-
    box(B).

attr(box_number(B), text, B) :-
    box(B).


% ============================================================
% 7. ASSIGN PIGEON DROPDOWN
% ============================================================

% Only display dropdown if candidates exist.
elem(box_dd(B), dropdown_menu, box_header(B)) :-
    has_available(B).

elem(box_dd_trigger(B),
     dropdown_menu(trigger), box_dd(B)) :-
    has_available(B).

attr(box_dd_trigger(B), class,
    ("inline-flex"; "h-8"; "w-8";
     "items-center"; "justify-center";
     "rounded-full"; "border"; "text-sm")) :-
    has_available(B).

attr(box_dd_trigger(B), text, "+") :-
    has_available(B).

% Accessible trigger label.
elem(trigger_a11y(B), span, box_dd_trigger(B)) :-
    has_available(B).

attr(trigger_a11y(B), class, "sr-only") :-
    has_available(B).

attr(trigger_a11y(B), text, "Assign a pigeon to box") :-
    has_available(B).

elem(trigger_num(B), span, box_dd_trigger(B)) :-
    has_available(B).

attr(trigger_num(B), class, "sr-only") :-
    has_available(B).

attr(trigger_num(B), text, B) :-
    has_available(B).

% Dropdown content.
elem(box_dd_content(B),
     dropdown_menu(content), box_dd(B)) :-
    has_available(B).

attr(box_dd_content(B), class, "w-44") :-
    has_available(B).

elem(box_dd_label(B),
     dropdown_menu(label), box_dd_content(B)) :-
    has_available(B).

attr(box_dd_label(B), text, "Assign pigeon") :-
    has_available(B).

attr(box_dd_label(B), order, 1) :-
    has_available(B).

% Dropdown options.
elem(box_dd_item(B,P),
     dropdown_menu(item), box_dd_content(B)) :-
    available(B,P).

attr(box_dd_item(B,P), class,
    ("flex"; "items-center"; "gap-1")) :-
    available(B,P).

attr(box_dd_item(B,P), order, P+1) :-
    available(B,P).

% Assign pigeon using backend assumption.
when(box_dd_item(B,P), click, call,
    add_assumption(in(P,B), true)) :-
    available(B,P).

% Pigeon label.
elem(dd_pigeon_prefix(B,P),
     span, box_dd_item(B,P)) :-
    available(B,P).

attr(dd_pigeon_prefix(B,P), text, "Pigeon") :-
    available(B,P).

elem(dd_pigeon_number(B,P),
     span, box_dd_item(B,P)) :-
    available(B,P).

attr(dd_pigeon_number(B,P), text, P) :-
    available(B,P).


% ============================================================
% 8. PIGEON ASSIGNMENTS INSIDE BOXES
% ============================================================

elem(box_pigeons(B), div, box_card(B)) :-
    box(B).

attr(box_pigeons(B), class,
    ("flex"; "min-h-9"; "flex-col"; "gap-1")) :-
    box(B).

% Locked pigeons are interactive buttons.
elem(chip(B,P), button, box_pigeons(B)) :-
    shown_assignment(P,B),
    assumed(P,B).

% Inferred or browsed assignments are display-only.
elem(chip(B,P), div, box_pigeons(B)) :-
    shown_assignment(P,B),
    not assumed(P,B).

attr(chip(B,P), class,
    ("flex"; "min-w-0"; "items-center"; "gap-1";
     "rounded-md"; "px-2"; "py-1"; "text-xs")) :-
    shown_assignment(P,B).

% Locked assignment appearance.
attr(chip(B,P), class,
    ("bg-primary"; "text-primary-foreground")) :-
    assumed(P,B).

% Inferred assignment appearance.
attr(chip(B,P), class,
    ("bg-accent"; "text-accent-foreground")) :-
    shown_assignment(P,B),
    not assumed(P,B).

attr(chip(B,P), order, P) :-
    shown_assignment(P,B).

% Remove assumption when clicking a locked pigeon.
when(chip(B,P), click, call,
    remove_assumption(in(P,B))) :-
    assumed(P,B).

% Accessible removal text.
elem(chip_remove_a11y(B,P),
     span, chip(B,P)) :-
    assumed(P,B).

attr(chip_remove_a11y(B,P), class, "sr-only") :-
    assumed(P,B).

attr(chip_remove_a11y(B,P),
     text, "Remove assignment for") :-
    assumed(P,B).

% Pigeon display.
elem(chip_prefix(B,P), span, chip(B,P)) :-
    shown_assignment(P,B).

attr(chip_prefix(B,P), text, "Pigeon") :-
    shown_assignment(P,B).

elem(chip_number(B,P), span, chip(B,P)) :-
    shown_assignment(P,B).

attr(chip_number(B,P), text, P) :-
    shown_assignment(P,B).

% Remove icon.
elem(chip_remove_icon(B,P), icon, chip(B,P)) :-
    assumed(P,B).

attr(chip_remove_icon(B,P), icon, "X") :-
    assumed(P,B).


% ============================================================
% 9. EMPTY BOX MESSAGE
% ============================================================

elem(empty_box(B), p, box_pigeons(B)) :-
    box(B),
    not shown_assignment(_,B),
    not _clinguin_unsat.

attr(empty_box(B), text, "No fixed pigeon") :-
    box(B),
    not shown_assignment(_,B),
    not _clinguin_unsat.

attr(empty_box(B), class,
    ("text-xs"; "text-muted-foreground")) :-
    box(B),
    not shown_assignment(_,B),
    not _clinguin_unsat.


% ============================================================
% 10. STATUS AREA
% ============================================================

elem(status_area, div, app_page).
attr(status_area, class,
    ("flex"; "flex-col"; "gap-3";
     "sm:flex-row"; "sm:items-start")).
attr(status_area, order, 3).

elem(status_alert, alert, status_area).
attr(status_alert, class, "flex-1").

% Status variants.
attr(status_alert, variant, "destructive") :-
    status(unsat).

attr(status_alert, variant, "default") :-
    status(ready).

attr(status_alert, variant, "default") :-
    status(browsing).

attr(status_alert, variant, "default") :-
    status(complete).

% Alert title.
elem(status_title, alert(title), status_alert).

attr(status_title, text, "Unsatisfiable") :-
    status(unsat).

attr(status_title, text, "Browsing solutions") :-
    status(browsing).

attr(status_title, text, "All locked in!") :-
    status(complete).

attr(status_title, text, "Ready") :-
    status(ready).

% Alert description.
elem(status_description,
     alert(description), status_alert).

attr(status_description, text,
    "The current assignments contradict the constraints. Remove a locked pigeon or clear assignments.") :-
    status(unsat).

attr(status_description, text,
    "Showing one valid full assignment. Lock it in, view the next solution, or stop browsing.") :-
    status(browsing).

attr(status_description, text,
    "Every pigeon has an explicit box assignment.") :-
    status(complete).

attr(status_description, text,
    "Use the plus button on a box to lock a pigeon, or browse complete solutions.") :-
    status(ready).


% ============================================================
% 11. HELP DIALOG
% ============================================================

elem(help_dialog, dialog, status_area).

elem(help_trigger,
     dialog(trigger), help_dialog).

attr(help_trigger, text, "How it works").

attr(help_trigger, class,
    ("inline-flex"; "h-9"; "items-center";
     "rounded-md"; "border"; "px-4";
     "text-sm"; "font-medium")).

% Dialog content.
elem(help_content,
     dialog(content), help_dialog).

attr(help_content, class, "sm:max-w-md").

elem(help_header,
     dialog(header), help_content).

elem(help_title,
     dialog(title), help_header).

attr(help_title, text,
    "The pigeonhole principle").

elem(help_description,
     dialog(description), help_header).

attr(help_description, text,
    "There is one more box than pigeons, so a valid assignment exists before additional choices. Each pigeon uses one box, and each box can hold at most one pigeon.").

% Dialog footer.
elem(help_footer,
     dialog(footer), help_content).

elem(help_close,
     dialog(close), help_footer).

attr(help_close, text, "Got it").

attr(help_close, class,
    ("inline-flex"; "h-9"; "items-center";
     "rounded-md"; "bg-primary"; "px-4";
     "text-sm"; "font-medium";
     "text-primary-foreground")).


% ============================================================
% 12. SOLUTION BROWSING CONTROLS
% ============================================================

elem(actions, div, app_page).

attr(actions, class,
    ("flex"; "flex-wrap"; "items-center";
     "justify-end"; "gap-2"; "pb-4")).

attr(actions, order, 4).

% Next solution.
elem(next_btn, button, actions).

attr(next_btn, text, "Next solution").
attr(next_btn, variant, "outline").

attr(next_btn, disabled, true) :-
    _clinguin_unsat.

when(next_btn, click, call, next_solution) :-
    not _clinguin_unsat.

% Stop browsing.
elem(stop_btn, button, actions) :-
    _clinguin_browsing,
    not _clinguin_unsat.

attr(stop_btn, text, "Stop browsing") :-
    _clinguin_browsing,
    not _clinguin_unsat.

attr(stop_btn, variant, "secondary") :-
    _clinguin_browsing,
    not _clinguin_unsat.

when(stop_btn, click, call, stop_browsing) :-
    _clinguin_browsing,
    not _clinguin_unsat.

% Lock the current solution.
elem(select_btn, button, actions) :-
    _clinguin_browsing,
    not _clinguin_unsat.

attr(select_btn, text, "Lock in solution") :-
    _clinguin_browsing,
    not _clinguin_unsat.

when(select_btn, click, call,
    select("#show in/2.")) :-
    _clinguin_browsing,
    not _clinguin_unsat.


% ============================================================
% 13. NOTIFICATIONS
% ============================================================

% Unsatisfiable notification.
elem(unsat_msg, sonner, app_page) :-
    status(unsat).

attr(unsat_msg, title, "Unsatisfiable") :-
    status(unsat).

attr(unsat_msg, description,
    "No valid assignment with these choices.") :-
    status(unsat).

attr(unsat_msg, type, danger) :-
    status(unsat).

% Completed assignment notification.
elem(complete_msg, sonner, app_page) :-
    status(complete).

attr(complete_msg, title, "Assignment complete!") :-
    status(complete).

attr(complete_msg, description,
    "All pigeons are locked into boxes.") :-
    status(complete).

attr(complete_msg, type, success) :-
    status(complete).

% ============================================================
% END OF UI
% ============================================================
