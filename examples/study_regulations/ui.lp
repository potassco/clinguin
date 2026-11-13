semester(1..n).
shown(E, I) :- _all(in(E, s(I))).
shown(E, I) :- in(E, s(I)), _clinguin_browsing.
removable(E, I) :- shown(E, I), _clinguin_assume(in(E, s(I)), true).
inferred(E, I) :- shown(E, I), not removable(E, I).
assignable(E, I) :- semester(I), _any(in(E, s(I))), not _all(in(E, s(I))).
module_rank(E, N) :- map(c, E, _), N = #count { E2 : map(c, E2, _), E2 < E }.

elem(X, icon, P) :- icon(X, P, _, _).
attr(X, icon, N; X, order, O) :- icon(X, _, N, O).

elem(page, div, root).
attr(page, class, ("min-h-screen"; "bg-background"; "text-foreground")).

elem(header, header, page).
attr(X, class, ("flex"; "flex-wrap"; "items-center"; "justify-between"; "gap-4"; "border-b"; "border-border"; "bg-card"; "px-6"; "py-4");
    X, order, 1) :- X = header.

elem(header_brand, div, header).
attr(X, class, ("flex"; "items-center"; "gap-3"); X, order, 1) :- X = header_brand.

icon(header_icon, header_brand, "GraduationCap", 1).
attr(X, icon_size, "size-7"; X, class, "text-primary") :- X = header_icon.

elem(title, h1, header_brand).
attr(X, text, "Study Regulations"; X, class, ("text-xl"; "font-semibold"; "tracking-tight"); X, order, 2) :- X = title.

elem(header_actions, div, header).
attr(X, class, ("flex"; "items-center"; "gap-2"); X, order, 2) :- X = header_actions.

elem(next_solution, button, header_actions).
attr(X, content, "Next solution"; X, variant, "outline"; X, order, 1) :- X = next_solution.
when(next_solution, click, call, next_solution).

elem(clear_assignments, button, header_actions).
attr(X, content, "Clear"; X, variant, "ghost"; X, order, 2;
    X, class, ("text-destructive"; "hover:bg-destructive/10"; "hover:text-destructive")) :- X = clear_assignments.
when(clear_assignments, click, call, clear_assumptions).
icon(clear_assignments_icon, clear_assignments, "Eraser", 1).

elem(theme, theme_toggle, header_actions).
attr(X, variant, "outline"; X, size, "icon"; X, order, 3) :- X = theme.

% ============================================================
% SEMESTER GRID + CARDS
% ============================================================

elem(main, main, page).
attr(X, class, "p-4"; X, order, 2) :- X = main.

elem(semester_grid, div, main).
attr(X, class, ("mx-auto"; "grid"; "w-full"; "max-w-7xl"; "gap-4");
    X, style, "grid-template-columns:repeat(auto-fit,minmax(16rem,1fr))") :- X = semester_grid.

elem(semester_card(I), section, semester_grid) :- semester(I).
attr(X, class, ("flex"; "flex-col"; "overflow-hidden"; "rounded-xl"; "border"; "border-border"; "bg-card"; "shadow-sm");
    X, style, "min-height:14rem"; X, order, I) :- semester(I), X = semester_card(I).

elem(semester_header(I), div, semester_card(I)) :- semester(I).
attr(X, class, ("flex"; "items-center"; "justify-between"; "gap-3"; "border-b"; "border-border"; "bg-muted/50"; "p-3");
    X, order, 1) :- semester(I), X = semester_header(I).

elem(semester_title(I), h2, semester_header(I)) :- semester(I).
attr(X, text, @format("Semester {}", I); X, class, "font-semibold"; X, order, 1) :- semester(I), X = semester_title(I).

% ============================================================
% ASSIGNMENT DROPDOWN
% ============================================================

elem(module_menu(I), dropdown_menu, semester_header(I)) :- semester(I).
attr(module_menu(I), order, 2) :- semester(I).

elem(module_trigger(I), dropdown_menu(trigger), module_menu(I)) :- semester(I).
attr(X, content, "Assign"; X, aria-label, "Assign module"; X, order, 1;
    X, class, ("inline-flex"; "h-8"; "items-center"; "gap-1"; "rounded-md"; "border"; "border-border"; "bg-background"; "px-2"; "text-xs"; "font-medium"; "shadow-xs"))
    :- semester(I), X = module_trigger(I).
icon(module_trigger_icon(I), module_trigger(I), "Plus", 1) :- semester(I).

elem(module_content(I), dropdown_menu(content), module_menu(I)) :- semester(I).
attr(X, align, "end"; X, style, "min-width:15rem;max-height:18rem;overflow-y:auto"; X, order, 2)
    :- semester(I), X = module_content(I).

elem(module_item(I, E), dropdown_menu(item), module_content(I)) :- assignable(E, I).
attr(X, content, @upper(E); X, order, N + 1) :- assignable(E, I), module_rank(E, N), X = module_item(I, E).
when(module_item(I, E), click, call, add_assumption(in(E, s(I)), true)) :- assignable(E, I).
icon(module_item_icon(I, E), module_item(I, E), "Plus", 1) :- assignable(E, I).

% ============================================================
% MODULE LIST
% ============================================================

elem(module_list(I), div, semester_card(I)) :- semester(I).
attr(X, class, ("flex"; "flex-1"; "flex-col"; "gap-2"; "p-3"); X, order, 2) :- semester(I), X = module_list(I).

elem(empty_semester(I), p, module_list(I)) :- semester(I), not shown(_, I).
attr(X, text, "No modules assigned."; X, class, ("m-auto"; "text-sm"; "text-muted-foreground"))
    :- semester(I), not shown(_, I), X = empty_semester(I).

% ============================================================
% MODULE ROWS
% ============================================================

elem(module_card(I, E), div, module_list(I)) :- inferred(E, I).
elem(module_card(I, E), button, module_list(I)) :- removable(E, I).

attr(module_card(I, E), class, ("flex"; "h-auto"; "w-full"; "items-center"; "justify-start"; "gap-2"; "rounded-md"; "border";
    "px-3"; "py-2"; "text-left"; "text-sm"; "transition-colors")) :- shown(E, I).
attr(module_card(I, E), order, N + 1) :- shown(E, I), module_rank(E, N).
attr(module_card(I, E), class, ("border-border"; "bg-background")) :- inferred(E, I).

attr(X, type, "button"; X, variant, "ghost";
    X, class, ("group"; "cursor-pointer"; "border-primary/30"; "bg-primary/5"; "text-primary"; "hover:bg-destructive/20"; "hover:text-destructive");
    X, aria-label, @format("Remove {} from semester {}", @upper(E), I)) :- removable(E, I), X = module_card(I, E).
when(module_card(I, E), click, call, remove_assumption(in(E, s(I)))) :- removable(E, I).

% Name
elem(module_name(I, E), span, module_card(I, E)) :- shown(E, I).
attr(X, text, @upper(E); X, class, "font-medium"; X, order, 1) :- shown(E, I), X = module_name(I, E).

% Trash icon, only visible on hover
icon(module_remove_icon(I, E), module_card(I, E), "Trash2", 2) :- removable(E, I).
attr(X, icon_size, "size-4"; X, class, ("hidden"; "shrink-0"; "text-destructive"; "group-hover:inline-block"))
    :- removable(E, I), X = module_remove_icon(I, E).

% ECTS
elem(module_ects(I, E), span, module_card(I, E)) :- shown(E, I), map(c, E, _).
attr(X, text, @format("{} ECTS", C); X, order, 3;
    X, class, ("ml-auto"; "text-xs"; "text-muted-foreground"; "tabular-nums")) :- shown(E, I), map(c, E, C), X = module_ects(I, E).
attr(module_ects(I, E), class, "group-hover:text-destructive") :- removable(E, I).
