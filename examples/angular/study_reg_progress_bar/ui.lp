%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Semester Definition
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

semester(I) :- _clinguin_const(n,N), I = 1..N.
values(3..8).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Root Window Configuration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(w, window, root).
attr(w, flex_direction, column).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Main container
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(main_container, container, w).
attr(main_container, order, 1).
attr(main_container, flex_direction, row).
attr(main_container, class, ("m-2")).

attr(main_container, class, "align-self-center").

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Left main container
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(left_container, container, main_container).
attr(left_container, order, 1).
attr(left_container, flex_direction, column).
attr(left_container, class, ("m-2")).
attr(left_container, child_layout, flex).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Container for 'n' value display and update button
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(n_input_container, container, left_container).
attr(n_input_container, order, 4).
attr(n_input_container, flex_direction, column).
attr(n_input_container, class, ("m-2")).
attr(n_input_container, class, "align-self-center").

elem(n_l, label, n_input_container).
attr(n_l, label, @concat("Current number of semesters: ", N)) :- _clinguin_const(n, N).
attr(n_l, order, 1).
attr(n_l, class, ("fw-bold"; "p-2"; "m-2")).

elem(n_dd, dropdown_menu, n_input_container).
attr(n_dd, order, 2).
attr(n_dd, selected, "Change").
attr(n_dd, class, ("btn-sm"; "btn-secondary"; "p-2"; "m-2")).

elem(n_ddi(V), dropdown_menu_item, n_dd) :- values(V).
attr(n_ddi(V), label, V) :- values(V).
when(n_ddi(V), click, call, set_constant("n", V)) :- values(V).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Container for semesters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(semester_container, container, left_container).
attr(semester_container, order, 2).
attr(semester_container, flex_direction, row).
attr(semester_container, class, "align-self-center").

elem(s(I), container, semester_container) :- semester(I).
attr(s(I), order, I) :- semester(I).
attr(s(I), class, ("border-opacity-50";"fw-bold";"p-3";"m-2"; "rounded"; "border"; "border-secondary"; "border-2")):-semester(I).

elem(s_t(I), container, s(I)):-semester(I).
attr(s_t(I), order, 1):-semester(I).
attr(s_t(I), class, ("bg-secondary";"text-light";"fw-bold";"p-2";"m-1"; "rounded")):-semester(I).

elem(s_l(I), label, s_t(I)):-semester(I).
attr(s_l(I), label, @concat("Semester ",I)):-semester(I).
attr(s_l(I), order, 1):-semester(I).

elem(s_dd(I), dropdown_menu, s_t(I)):-semester(I).
attr(s_dd(I), order, 2):-semester(I).
attr(s_dd(I), selected, "Assign module"):-semester(I).
attr(s_dd(I), class, ("btn-sm";"btn-outline-light"; "m-2")):-semester(I).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dropdown menu items
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(s_ddi(I,E), dropdown_menu_item, s_dd(I)):-_any(in(E,s(I))), not _all(in(E,s(I))).
attr(s_ddi(I,E), label, @concat(E, " (", C, " ECTS)")):-_any(in(E,s(I))), not _all(in(E,s(I))), map(c, E, C).
when(s_ddi(I,E), click, call, add_assumption(in(E,s(I)))):-_any(in(E,s(I))), not _all(in(E,s(I))).

elem(s_modules(I), container, s(I)):-semester(I).
attr(s_modules(I), class, ("bg-white")):-semester(I).
attr(s_modules(I), order, 2):-semester(I).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Module display in semesters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

shown_module(E,I):-_all(in(E,s(I))).
shown_module(E,I):-in(E,s(I)),_clinguin_browsing.

elem(s_module(I,E), container, s_modules(I)):-shown_module(E,I).
attr(s_module(I,E), height, C*10):-shown_module(E,I), map(c,E,C).
attr(s_module(I,E), class, ("border"; "border-secondary";
                            "d-flex";"flex-row";"justify-content-between";"align-items-center";
                            "p-3";"m-2"; "rounded"; "border-2"; "border-opacity-50")):-shown_module(E,I).

elem(s_module_l(I,E), label, s_module(I,E)):-shown_module(E,I).
attr(s_module_l(I,E), label, E):-shown_module(E,I).
attr(s_module_l(I,E), class, ("text-black"; "fw-bold")):-shown_module(E,I).

elem(s_module_b(I,E), button, s_module(I,E)):-_clinguin_assume(in(E,s(I))).
attr(s_module_b(I,E), icon, "fa-times"):-_clinguin_assume(in(E,s(I))).
attr(s_module_b(I,E), class, ("btn-sm";"btn-outline")):-_clinguin_assume(in(E,s(I))).
when(s_module_b(I,E), click, call, remove_assumption(in(E,s(I)))):-_clinguin_assume(in(E,s(I))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Main Menu Bar Configuration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Study Regulations").
attr(menu_bar, icon, "fa-graduation-cap").

elem(menu_bar_clear, button, menu_bar).
attr(menu_bar_clear, label, "Clear").
attr(menu_bar_clear, icon, "fa-trash").
attr(menu_bar_clear, class, ("btn-sm";"btn-outline-secondary")).
when(menu_bar_clear, click, call, clear_assumptions).

elem(menu_bar_next, button, menu_bar).
attr(menu_bar_next, label, "Next").
attr(menu_bar_next, icon, "fa-forward-step").
attr(menu_bar_next, class, ("btn-sm";"btn-outline-secondary")).
when(menu_bar_next, click, call, next_solution).

elem(menu_bar_select, button, menu_bar).
attr(menu_bar_select, label, "Select").
attr(menu_bar_select, icon, "fa-hand-pointer").
attr(menu_bar_select, class, ("btn-sm";"btn-outline-secondary")).
when(menu_bar_select, click, call, select).

elem(menu_bar_download, button, menu_bar).
attr(menu_bar_download, label, "Download Study Plan").
attr(menu_bar_download, icon, "fa-download").
attr(menu_bar_download, class, ("btn-sm";"btn-outline-secondary")).
when(menu_bar_download, click, update, (download_modal, visible, shown)).

elem(menu_bar_download_asp, button, menu_bar).
attr(menu_bar_download_asp, label, "Download ASP Model").
attr(menu_bar_download_asp, icon, "fa-download").
attr(menu_bar_download_asp, class, ("btn-sm";"btn-outline-secondary")).
when(menu_bar_download_asp, click, call, download("#show in.","asp_study_plan.lp")).

elem(download_modal, modal, w).
attr(download_modal, title, "Download Study Plan").

elem(download_filename, textfield, download_modal).
attr(download_filename, placeholder, "Enter file name (e.g., study_plan.txt)").
attr(download_filename, width, 300).
when(download_filename, input, context, (file_name, _value)).

elem(download_button, button, download_modal).
attr(download_button, label, "Download").
attr(download_button, class, ("btn-primary", "mt-3")).
when(download_button, click, call, custom_download(_context_value(file_name, str, "semester_assignments.txt"))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Module Information Modal
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(module_info_modal(E), modal, left_container) :- in(E,_).
attr(module_info_modal(E), title, E) :- in(E,_).

elem(module_info_credits(E), label, module_info_modal(E)) :- in(E,_).
attr(module_info_credits(E), label, @concat("Credits: ", C)) :- map(c,E,C).

when(s_module_l(I,E), click, update, (module_info_modal(E), visible, shown)) :- shown_module(E,I).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Credits Display Under Each Semester
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(s_credits(I), container, s(I)) :- semester(I).
attr(s_credits(I), order, 3) :- semester(I).
attr(s_credits(I), class, ("bg-light"; "p-2"; "mt-2"; "rounded"; "text-center"; "fw-bold"; "mt-auto")) :- semester(I).

elem(s_credits_label(I), label, s_credits(I)) :- semester(I).
attr(s_credits_label(I), label, @concat(SC, " ECTS")) :- 
    semester(I),
    SC = #sum{ C,E : map(c,E,C), shown_module(E,I) }.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Total Credits Display at the Top of the Page
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(total_credits_container, container, left_container).
attr(total_credits_container, order, 1).
attr(total_credits_container, class, ("bg-secondary"; "text-white"; "p-3"; "rounded"; "m-2"; "align-self-center")).

elem(total_credits_label, label, total_credits_container).
attr(total_credits_label, label, @concat("Total credits: ", TC)) :- 
    TC = #sum{ C,E : map(c,E,C), shown_module(E,_) }.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Side right bar
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(right_container, container, main_container).
attr(right_container, order, 2).
attr(right_container, flex_direction, column).
attr(right_container, class, ("ms-5")).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Containers for subsets of modules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Identify all subsets
subset(E,S) :- map(l, S, _); map(u, S, _), in(E, S).

% Create containers for each subset
elem(subset_container(S), container, right_container) :- subset(E,S).
attr(subset_container(S), class, ("border-opacity-50";"fw-bold";"p-2";"m-2"; "rounded"; "border"; "border-secondary"; "border-2")) :- subset(E,S).
attr(subset_container(S), flex_direction, column) :- subset(E,S).
attr(subset_container(S), width, 300) :- subset(E,S).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Labels for subsets
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(subset_l_container(S), container, subset_container(S)):-subset(E,S).
attr(subset_l_container(S), order, 1):-subset(E,S).
attr(subset_l_container(S), class, ("bg-secondary";"text-light";"fw-bold";"p-2";"mt-2";"mb-2";"rounded")):-subset(E,S).

elem(subset_l(S), label, subset_l_container(S)):-subset(E,S).
attr(subset_l(S), label, S):-subset(E,S).
attr(subset_l(S), order, 1):-subset(E,S).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Display modules in subsets
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

elem(subset_module(S), container, subset_container(S)) :- subset(E,S).
attr(subset_module(S), order, 2):- subset(E,S).
attr(subset_module(S), class, ("d-flex"; "flex-wrap"; "pt-2")):- subset(E,S).
attr(subset_module(S), flex_direction, row) :- subset(E,S).

% Module is visibly selected if it's shown in any semester
module_visibly_selected(E) :- shown_module(E, I), semester(I).

elem(subset_module_button(E,S), button, subset_module(S)) :- in(E,S), subset(E,S).
attr(subset_module_button(E,S), label, E) :- in(E,S), subset(E,S).
attr(subset_module_button(E,S), class, ("btn-sm"; "m-1"; "disabled")) :- in(E,S), subset(E,S).
attr(subset_module_button(E,S), class, "btn-secondary") :- in(E,S), subset(E,S), module_visibly_selected(E).
attr(subset_module_button(E,S), class, "btn-outline-secondary") :- in(E,S), subset(E,S), not module_visibly_selected(E).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Display progress bar for credits in each subset
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Calculate the total credits for visibly selected modules within each subset
subset_total_credits(S, TotalCredits) :-
    subset(_, S),
    TotalCredits = #sum { C, E : module_visibly_selected(E), in(E, S), map(c, E, C) }.

% Calculate the remaining credits for each subset
remaining_credits(S, Remaining) :-
    map(l, S, LowerBound),
    subset_total_credits(S, TotalCredits),
    Remaining = LowerBound - TotalCredits.

% Calculate the percentage of credits completed for each subset
progress_percentage(S, Percentage) :-
    map(l, S, LowerBound),
    subset_total_credits(S, TotalCredits),
    LowerBound > 0,
    Percentage = (TotalCredits * 100) / LowerBound.

elem(progress_bar_container(S), container, subset_container(S)) :- subset(_, S).
attr(progress_bar_container(S), order, 4) :- subset(_, S).
attr(progress_bar_container(S), class, ("pt-3")) :- subset(_, S).



% Display the progress bar showing percentage of completed credits
elem(subset_progress_bar(S), progress_bar, progress_bar_container(S)) :- subset(_, S).
attr(subset_progress_bar(S), value, P) :- progress_percentage(S, P).
attr(subset_progress_bar(S), class, ("progress-bar-striped"; "progress-bar-animated"; "rounded")) :- subset(_, S).
attr(subset_progress_bar(S), label, @concat("Remaining credits needed in ", S, ": ", Remaining)) :-
    remaining_credits(S, Remaining).
attr(subset_progress_bar(S), height, 30) :- progress_percentage(S, P).
attr(subset_progress_bar(S), class, "bg-success") :- progress_percentage(S, P), P >= 100.
attr(subset_progress_bar(S), class, "bg-warning") :- progress_percentage(S, P), P >= 50, P < 100.
attr(subset_progress_bar(S), class, "bg-danger") :- progress_percentage(S, P), P < 50.



% all borders
%attr(E,class,("border-1";"border";"border-dark")):- elem(E, container, _).