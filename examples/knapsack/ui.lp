% UI state
column(not_available, 1, "ThumbsDown", "Excluded").
column(available, 2, "ThumbsUp", "Available").
column(taken, 3, "Backpack", "In the knapsack").

in_column(O, taken) :- object(O), _clinguin_assume(take(O), true).
in_column(O, taken) :- object(O), take(O), _clinguin_browsing.
in_column(O, not_available) :- object(O), _clinguin_assume(take(O), false).
in_column(O, available) :- object(O), not in_column(O, taken), not in_column(O, not_available).

decided(O) :- object(O), _clinguin_assume(take(O), _).
undecided(O) :- object(O), not decided(O).
rank(O, N) :- object(O), N = #count { O2 : object(O2), O2 < O }.

taken_value(S) :- S = #sum { V, O : in_column(O, taken), value(O, V) }.
taken_weight(S) :- S = #sum { W, O : in_column(O, taken), weight(O, W) }.

elem(X, icon, P) :- icon(X, P, _, _).
attr(X, icon, N; X, order, O) :- icon(X, _, N, O).

% Page + toolbar
elem(page, div, root).
attr(page, class, ("min-h-screen"; "flex"; "justify-center"; "bg-background"; "text-foreground"; "p-6")).

elem(board, div, page).
attr(board, class, ("flex"; "flex-col"; "gap-4"; "w-fit")).

elem(header, div, board).
attr(X, class, ("flex"; "items-center"; "justify-between"; "gap-4"); X, order, 1) :- X = header.

elem(header_title, div, header).
attr(X, class, ("flex"; "items-center"; "gap-2"); X, order, 1) :- X = header_title.

icon(title_icon, header_title, "Backpack", 1).
attr(X, icon_size, "size-6"; X, class, "text-primary") :- X = title_icon.

elem(title_text, h1, header_title).
attr(X, text, "Knapsack"; X, class, ("text-lg"; "font-semibold"); X, order, 2) :- X = title_text.

elem(header_actions, div, header).
attr(X, class, ("flex"; "items-center"; "gap-2"); X, order, 2) :- X = header_actions.

elem(next_button, button, header_actions).
attr(X, text, "Next optimal"; X, size, "sm"; X, order, 1) :- X = next_button.
when(next_button, click, call, next_solution(optN)).
icon(next_icon, next_button, "FastForward", 1).

elem(select_button, button, header_actions).
attr(X, text, "Select"; X, variant, "outline"; X, size, "sm"; X, order, 2) :- X = select_button.
attr(select_button, disabled, true) :- not _clinguin_browsing.
when(select_button, click, call, select) :- _clinguin_browsing.
icon(select_icon, select_button, "MousePointerClick", 1).

elem(clear_button, button, header_actions).
attr(X, text, "Clear"; X, variant, "outline"; X, size, "sm"; X, order, 3) :- X = clear_button.
when(clear_button, click, call, clear_assumptions).
icon(clear_icon, clear_button, "Trash2", 1).
attr(clear_icon, class, "text-destructive").

elem(actions_sep, separator, header_actions).
attr(X, orientation, "vertical"; X, class, ("h-5"; "mx-1"); X, order, 4) :- X = actions_sep.

elem(theme_button, theme_toggle, header_actions).
attr(X, variant, "ghost"; X, size, "icon"; X, order, 5) :- X = theme_button.

elem(summary, div, board).
attr(X, class, ("flex"; "items-center"; "gap-6"; "rounded-lg"; "border"; "border-border"; "px-4"; "py-3"); X, order, 2) :- X = summary.

elem(summary_value, div, summary).
attr(X, class, ("flex"; "items-baseline"; "gap-1"); X, order, 1) :- X = summary_value.

elem(summary_value_label, span, summary_value).
attr(X, text, "Value"; X, class, ("text-sm"; "text-muted-foreground"); X, order, 1) :- X = summary_value_label.

elem(summary_value_num, span, summary_value).
attr(X, text, @format("{} €", S); X, class, ("text-lg"; "font-semibold"); X, order, 2) :- taken_value(S), X = summary_value_num.

elem(summary_weight, div, summary).
attr(X, class, ("flex"; "grow"; "flex-col"; "gap-1"); X, order, 2) :- X = summary_weight.

elem(weight_text, div, summary_weight).
attr(X, class, ("flex"; "justify-between"; "text-sm"); X, order, 1) :- X = weight_text.

elem(weight_used, span, weight_text).
attr(X, text, @format("{} g / {} g", (S, M)); X, order, 1) :- taken_weight(S), weight_limit(M), X = weight_used.

elem(weight_left, span, weight_text).
attr(X, text, @format("{} g left", M - S); X, class, "text-muted-foreground"; X, order, 2) :- taken_weight(S), weight_limit(M), X = weight_left.

elem(weight_bar, progress, summary_weight).
attr(X, value, S; X, max, M; X, class, ("w-full"; "h-2"; "accent-primary"); X, order, 2) :- taken_weight(S), weight_limit(M), X = weight_bar.

% Columns
elem(columns, div, board).
attr(X, class, ("flex"; "flex-wrap"; "gap-4"; "items-start"); X, order, 3) :- X = columns.

elem(column(C), div, columns) :- column(C, _, _, _).
attr(X, class, ("w-72"; "min-h-64"; "flex"; "flex-col"; "gap-2"; "rounded-lg"; "border"; "p-3"); X, order, N) :- column(C, N, _, _), X = column(C).
attr(column(not_available), class, ("bg-destructive/5"; "border-destructive/30")).
attr(column(available), class, ("bg-muted/50"; "border-border")).
attr(column(taken), class, ("bg-primary/5"; "border-primary/30")).

elem(column_head(C), div, column(C)) :- column(C, _, _, _).
attr(X, class, ("flex"; "items-center"; "gap-2"; "pb-2"; "text-sm"; "font-medium"); X, order, 1) :- column(C, _, _, _), X = column_head(C).

icon(column_icon(C), column_head(C), I, 1) :- column(C, _, I, _).
attr(column_icon(C), icon_size, "size-4") :- column(C, _, _, _).

elem(column_title(C), span, column_head(C)) :- column(C, _, _, _).
attr(X, text, T; X, order, 2) :- column(C, _, _, T), X = column_title(C).

elem(column_empty(C), p, column(C)) :- column(C, _, _, _), not in_column(_, C).
attr(X, text, "Nothing here"; X, class, ("py-6"; "text-center"; "text-sm"; "text-muted-foreground"); X, order, 2) :- column(C, _, _, _), not in_column(_, C), X = column_empty(C).

% Item cards (sorted by name within each column)
elem(item(O), div, column(C)) :- in_column(O, C).
attr(X, class, ("flex"; "items-center"; "justify-between"; "gap-2"; "rounded-md"; "border"; "border-border"; "bg-background"; "px-3"; "py-2"; "shadow-xs"); X, order, N + 2) :- rank(O, N), X = item(O).

elem(item_info(O), div, item(O)) :- object(O).
attr(X, class, ("flex"; "flex-col"); X, order, 1) :- object(O), X = item_info(O).

elem(item_name(O), div, item_info(O)) :- object(O).
attr(X, class, ("flex"; "items-center"; "gap-1"; "font-medium"); X, order, 1) :- object(O), X = item_name(O).

elem(item_name_text(O), span, item_name(O)) :- object(O).
attr(X, text, @stringify(O, true); X, order, 1) :- object(O), X = item_name_text(O).

icon(item_medal(O), item_name(O), "Star", 2) :- in_column(O, available), _any_opt(take(O)).
attr(X, icon_size, "size-4"; X, class, "text-amber-500") :- in_column(O, available), _any_opt(take(O)), X = item_medal(O).

elem(item_meta(O), span, item_info(O)) :- object(O).
attr(X, text, @format("{} € · {} g", (V, W)); X, class, ("text-xs"; "text-muted-foreground"); X, order, 2) :- value(O, V), weight(O, W), X = item_meta(O).

elem(item_actions(O), div, item(O)) :- object(O).
attr(X, class, ("flex"; "items-center"; "gap-1"); X, order, 2) :- object(O), X = item_actions(O).

% Item actions
item_button(take, 1, "Plus", "Put in the knapsack").
item_button(exclude, 2, "X", "Exclude").
item_button(reset, 1, "Undo2", "Move back to available").

shows(O, take; O, exclude) :- undecided(O).
shows(O, reset) :- decided(O).

elem(btn(O, K), button, item_actions(O)) :- shows(O, K).
attr(X, variant, "ghost"; X, size, "icon"; X, title, T; X, order, N) :- shows(O, K), item_button(K, N, _, T), X = btn(O, K).
icon(btn_icon(O, K), btn(O, K), I, 1) :- shows(O, K), item_button(K, _, I, _).

attr(btn(O, K), class, "text-muted-foreground") :- shows(O, K), K != take.
attr(btn(O, exclude), class, "hover:text-destructive") :- shows(O, exclude).
attr(btn(O, take), disabled, true) :- shows(O, take), not _any(take(O)).

when(btn(O, take), click, call, add_assumption(take(O), true)) :- shows(O, take), _any(take(O)).
when(btn(O, exclude), click, call, add_assumption(take(O), false)) :- shows(O, exclude).
when(btn(O, reset), click, call, remove_assumption(take(O))) :- shows(O, reset).
