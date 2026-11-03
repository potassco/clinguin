% ============================================================================
% CLINGUIN UI QUICK START
%
% 1. Uncomment the templates you want to use.
% 2. Customize each enabled template in its own file.
% 3. Write your application UI below "APPLICATION UI".
%
% Reusable templates attach to one of these stable elements:
%     ui_app      - the complete application
%     ui_content  - the main application content
% ============================================================================


% ==============================================================================
% TEMPLATES
%
% Uncomment the templates you want to use. Customize each template in
% its own file.
% ==============================================================================

% Sticky menu bar. Customize it in menu-bar.lp.
#include "menu-bar.lp".



% ============================================================================
% FIXED STRUCTURE
%
% The following elements are used by the templates and should not be removed
% or renamed.
% ============================================================================

% The root element is the top-level container for the application.
elem(ui_app, div, root).
attr(ui_app, class,
    ("min-h-screen";
     "flex";
     "flex-col";
     "bg-background";
     "text-foreground")).


	% The main content area is where the application content is displayed.
	elem(ui_content, main, ui_app).
	attr(ui_content, class,
		("flex";
		"min-h-0";
		"grow";
		"flex-col")).
	attr(ui_content, order, 100).


% ============================================================================
% APPLICATION UI
%
% Add the elements of your application below and attach top-level content to
% ui_content.
% ============================================================================


% Generated via LLM prompt as a test.

%%% Menu bar configuration
menubar_title_override("Smart placement").
menubar_subtitle_override("Seat guests using few tables and few empty seats").
menubar_icon_override("Utensils").

%%% Presentation helpers
ui_person(P) :- person(P).
ui_person(P) :- _clinguin_atom(person(P)).

included(P) :- ui_person(P), _clinguin_external(include(P), true).
some_included :- included(_).

chosen(S,T,P) :- seat(S,T), ui_person(P),
    _clinguin_assume(assign(seat(S,T),P), true).
seat_chosen(S,T) :- chosen(S,T,_).
has_chosen_seat(P) :- chosen(_,_,P).

planned(S,T,P) :- seat(S,T), assign(seat(S,T),P), not _clinguin_unsat.

shown(S,T,P) :- chosen(S,T,P).
shown(S,T,P) :- planned(S,T,P), not seat_chosen(S,T).
seat_filled(S,T) :- shown(S,T,_).

possible(S,T,P) :- seat(S,T), ui_person(P), _any(assign(seat(S,T),P)).

unseated(P) :- included(P), not has_chosen_seat(P).
some_unseated :- unseated(_).

has_seat(T) :- seat(_,T).

%%% Page
elem(app_page, div, ui_content).
attr(app_page, class,
    ("mx-auto"; "flex"; "w-full"; "max-w-screen-xl"; "flex-col"; "gap-4";
     "p-4"; "md:p-6")).

%%% Unsatisfiable state
elem(unsat_alert, alert, app_page) :- _clinguin_unsat.
attr(unsat_alert, variant, "destructive") :- _clinguin_unsat.
attr(unsat_alert, order, 1) :- _clinguin_unsat.

elem(unsat_title, alert(title), unsat_alert) :- _clinguin_unsat.
attr(unsat_title, text, "No valid seating plan") :- _clinguin_unsat.

elem(unsat_description, alert(description), unsat_alert) :- _clinguin_unsat.
attr(unsat_description, text,
    "More people are included than there are seats, or seat choices conflict. Exclude someone or clear a seat choice.")
    :- _clinguin_unsat.

%%% Main grid
elem(main_grid, div, app_page).
attr(main_grid, order, 2).
attr(main_grid, class,
    ("grid"; "grid-cols-1"; "gap-4";
     "lg:grid-cols-[minmax(260px,1fr)_minmax(0,2fr)]")).

%%% People panel
elem(people_panel, section, main_grid).
attr(people_panel, order, 1).
attr(people_panel, class,
    ("flex"; "min-w-0"; "flex-col"; "gap-4"; "rounded-lg"; "border";
     "bg-card"; "text-card-foreground"; "p-4")).

elem(people_heading, h2, people_panel).
attr(people_heading, order, 1).
attr(people_heading, text, "People").
attr(people_heading, class, ("text-lg"; "font-semibold")).

elem(people_hint, p, people_panel).
attr(people_hint, order, 2).
attr(people_hint, text, "Check the people who need a seat.").
attr(people_hint, class, ("text-sm"; "text-muted-foreground")).

elem(people_list, ul, people_panel).
attr(people_list, order, 3).
attr(people_list, class, ("flex"; "flex-col"; "gap-2")).

elem(person_item(P), li, people_list) :- ui_person(P).
attr(person_item(P), class, ("flex"; "flex-col"; "gap-1")) :- ui_person(P).

elem(person_label(P), label, person_item(P)) :- ui_person(P).
attr(person_label(P), text, P) :- ui_person(P).
attr(person_label(P), class,
    ("flex"; "items-center"; "gap-2"; "text-sm"; "font-medium")) :- ui_person(P).

elem(person_checkbox(P), checkbox, person_label(P)) :- ui_person(P).
attr(person_checkbox(P), checked, true) :- included(P).
attr(person_checkbox(P), checked, false) :- ui_person(P), not included(P).
attr(person_checkbox(P), disabled, true) :- included(P), has_chosen_seat(P).
when(person_checkbox(P), checked_change, call, set_external(include(P), true)) :-
    ui_person(P), not included(P).
when(person_checkbox(P), checked_change, call, set_external(include(P), false)) :-
    included(P), not has_chosen_seat(P).

elem(person_note(P), p, person_item(P)) :- included(P), has_chosen_seat(P).
attr(person_note(P), text, "Clear this person's seat choice to exclude them.") :-
    included(P), has_chosen_seat(P).
attr(person_note(P), class, ("pl-6"; "text-xs"; "text-muted-foreground")) :-
    included(P), has_chosen_seat(P).

%%% Included people without a chosen seat
elem(unseated_section, div, people_panel).
attr(unseated_section, order, 4).
attr(unseated_section, class, ("flex"; "flex-col"; "gap-2"; "border-t"; "pt-4")).

elem(unseated_heading, h3, unseated_section).
attr(unseated_heading, order, 1).
attr(unseated_heading, text, "Included, no seat chosen yet").
attr(unseated_heading, class, ("text-sm"; "font-semibold")).

elem(unseated_list, ul, unseated_section) :- some_unseated.
attr(unseated_list, order, 2) :- some_unseated.
attr(unseated_list, class, ("flex"; "flex-wrap"; "gap-2")) :- some_unseated.

elem(unseated_item(P), li, unseated_list) :- unseated(P).
attr(unseated_item(P), text, P) :- unseated(P).
attr(unseated_item(P), class,
    ("rounded-md"; "bg-muted"; "px-2"; "py-1"; "text-sm")) :- unseated(P).

elem(unseated_empty, p, unseated_section) :- not some_unseated.
attr(unseated_empty, order, 2) :- not some_unseated.
attr(unseated_empty, text, "Everyone included has a chosen seat.") :-
    not some_unseated, some_included.
attr(unseated_empty, text, "No one is included yet.") :-
    not some_unseated, not some_included.
attr(unseated_empty, class, ("text-sm"; "text-muted-foreground")) :-
    not some_unseated.

%%% Add a person
elem(add_form, form, people_panel).
attr(add_form, order, 5).
attr(add_form, class, ("flex"; "flex-col"; "gap-2"; "border-t"; "pt-4")).
when(add_form, submit, call, add_atom(person(_context_value(name)))).

elem(add_label, label, add_form).
attr(add_label, order, 1).
attr(add_label, for, "new-person-name").
attr(add_label, text, "New person").

elem(add_row, div, add_form).
attr(add_row, order, 2).
attr(add_row, class, ("flex"; "gap-2")).

elem(add_input, input, add_row).
attr(add_input, order, 1).
attr(add_input, id, "new-person-name").
attr(add_input, name, "name").
attr(add_input, type, "text").
attr(add_input, placeholder, "Name").
attr(add_input, required, true).
attr(add_input, class, ("min-w-0"; "grow")).

elem(add_button, button, add_row).
attr(add_button, order, 2).
attr(add_button, type, "submit").
attr(add_button, variant, "secondary").
attr(add_button, text, "Add").

elem(add_hint, p, add_form).
attr(add_hint, order, 3).
attr(add_hint, text, "New people start excluded. Check them to include them.").
attr(add_hint, class, ("text-xs"; "text-muted-foreground")).

%%% Tables area
elem(tables_area, section, main_grid).
attr(tables_area, order, 2).
attr(tables_area, class, ("flex"; "min-w-0"; "flex-col"; "gap-4")).

elem(tables_heading, h2, tables_area).
attr(tables_heading, order, 1).
attr(tables_heading, text, "Tables").
attr(tables_heading, class, ("text-lg"; "font-semibold")).

elem(tables_hint, p, tables_area).
attr(tables_hint, order, 2).
attr(tables_hint, text,
    "Choose a person to fix a seat. Other seats show the solver's suggestion.").
attr(tables_hint, class, ("text-sm"; "text-muted-foreground")).

elem(tables_grid, div, tables_area).
attr(tables_grid, order, 3).
attr(tables_grid, class,
    ("grid"; "grid-cols-1"; "gap-4"; "sm:grid-cols-2"; "xl:grid-cols-3")).

elem(table_card(T), article, tables_grid) :- table(T,_).
attr(table_card(T), order, T) :- table(T,_).
attr(table_card(T), class,
    ("flex"; "min-w-0"; "flex-col"; "gap-3"; "rounded-lg"; "border";
     "bg-card"; "text-card-foreground"; "p-4")) :- table(T,_).

elem(table_title(T), h3, table_card(T)) :- table(T,_).
attr(table_title(T), order, 1) :- table(T,_).
attr(table_title(T), text, L) :- table(T,L).
attr(table_title(T), class, ("font-semibold")) :- table(T,_).

elem(seat_none(T), p, table_card(T)) :- table(T,_), not has_seat(T).
attr(seat_none(T), order, 2) :- table(T,_), not has_seat(T).
attr(seat_none(T), text, "This table has no seats.") :- table(T,_), not has_seat(T).
attr(seat_none(T), class, ("text-sm"; "text-muted-foreground")) :-
    table(T,_), not has_seat(T).

elem(seat_list(T), ul, table_card(T)) :- table(T,_), has_seat(T).
attr(seat_list(T), order, 2) :- table(T,_), has_seat(T).
attr(seat_list(T), class, ("flex"; "flex-col"; "gap-2")) :- table(T,_), has_seat(T).

elem(seat_row(S,T), li, seat_list(T)) :- seat(S,T), table(T,_).
attr(seat_row(S,T), order, S) :- seat(S,T), table(T,_).
attr(seat_row(S,T), class, ("flex"; "flex-wrap"; "items-center"; "gap-2")) :-
    seat(S,T), table(T,_).

elem(seat_name(S,T), span, seat_row(S,T)) :- seat(S,T), table(T,_).
attr(seat_name(S,T), order, 1) :- seat(S,T), table(T,_).
attr(seat_name(S,T), text, "Seat") :- seat(S,T), table(T,_).
attr(seat_name(S,T), class, ("text-sm"; "text-muted-foreground")) :-
    seat(S,T), table(T,_).

elem(seat_number(S,T), span, seat_row(S,T)) :- seat(S,T), table(T,_).
attr(seat_number(S,T), order, 2) :- seat(S,T), table(T,_).
attr(seat_number(S,T), text, S) :- seat(S,T), table(T,_).
attr(seat_number(S,T), class, ("w-4"; "text-sm"; "text-muted-foreground")) :-
    seat(S,T), table(T,_).

%%% Seat dropdown
elem(seat_menu(S,T), dropdown_menu, seat_row(S,T)) :- seat(S,T), table(T,_).
attr(seat_menu(S,T), order, 3) :- seat(S,T), table(T,_).

elem(seat_trigger(S,T), dropdown_menu(trigger), seat_menu(S,T)) :-
    seat(S,T), table(T,_).
attr(seat_trigger(S,T), text, P) :- shown(S,T,P), table(T,_).
attr(seat_trigger(S,T), text, "Empty") :-
    seat(S,T), table(T,_), not seat_filled(S,T).
attr(seat_trigger(S,T), class,
    ("inline-flex"; "h-9"; "min-w-32"; "items-center"; "rounded-md";
     "border"; "border-input"; "bg-background"; "px-3"; "text-sm";
     "hover:bg-muted")) :- seat(S,T), table(T,_).
attr(seat_trigger(S,T), class, ("border-primary"; "font-semibold")) :-
    seat_chosen(S,T), table(T,_).

elem(seat_status(S,T), span, seat_row(S,T)) :- seat(S,T), table(T,_).
attr(seat_status(S,T), order, 4) :- seat(S,T), table(T,_).
attr(seat_status(S,T), class, ("text-xs"; "text-muted-foreground")) :-
    seat(S,T), table(T,_).
attr(seat_status(S,T), text, "chosen by you") :- seat_chosen(S,T), table(T,_).
attr(seat_status(S,T), text, "suggested") :-
    seat_filled(S,T), table(T,_), not seat_chosen(S,T).
attr(seat_status(S,T), text, "stays empty") :-
    seat(S,T), table(T,_), not seat_filled(S,T), not _clinguin_unsat.
attr(seat_status(S,T), text, "no plan") :-
    seat(S,T), table(T,_), not seat_filled(S,T), _clinguin_unsat.

elem(seat_content(S,T), dropdown_menu(content), seat_menu(S,T)) :-
    seat(S,T), table(T,_).

elem(seat_menu_label(S,T), dropdown_menu(label), seat_content(S,T)) :-
    seat(S,T), table(T,_).
attr(seat_menu_label(S,T), order, 1) :- seat(S,T), table(T,_).
attr(seat_menu_label(S,T), text, "Assign a person") :- seat(S,T), table(T,_).

elem(seat_clear(S,T), dropdown_menu(item), seat_content(S,T)) :-
    seat(S,T), table(T,_).
attr(seat_clear(S,T), order, 2) :- seat(S,T), table(T,_).
attr(seat_clear(S,T), text, "Clear seat choice") :- seat(S,T), table(T,_).
attr(seat_clear(S,T), disabled, true) :-
    seat(S,T), table(T,_), not seat_chosen(S,T).
when(seat_clear(S,T), click, call,
    remove_assumption_signature(assign(seat(S,T),any))) :-
    seat_chosen(S,T), table(T,_).

elem(seat_separator(S,T), dropdown_menu(separator), seat_content(S,T)) :-
    seat(S,T), table(T,_).
attr(seat_separator(S,T), order, 3) :- seat(S,T), table(T,_).

elem(seat_option(S,T,P), dropdown_menu(item), seat_content(S,T)) :-
    seat(S,T), table(T,_), ui_person(P).
attr(seat_option(S,T,P), order, 4) :- seat(S,T), table(T,_), ui_person(P).
attr(seat_option(S,T,P), text, P) :- seat(S,T), table(T,_), ui_person(P).
attr(seat_option(S,T,P), disabled, true) :-
    seat(S,T), table(T,_), ui_person(P), not possible(S,T,P).
attr(seat_option(S,T,P), disabled, true) :- chosen(S,T,P), table(T,_).
when(seat_option(S,T,P), click, call, add_assumption(assign(seat(S,T),P), true)) :-
    possible(S,T,P), table(T,_), not chosen(S,T,P).
