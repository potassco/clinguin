shown_value(X,Y,V) :- initial(X,Y,V).
shown_value(X,Y,V) :- _all(sudoku(X,Y,V)).
shown_value(X,Y,V) :- sudoku(X,Y,V), _clinguin_browsing.

forced_value(X,Y,V) :- _all(sudoku(X,Y,V)), not initial(X,Y,V), not _clinguin_assume(sudoku(X,Y,V),true).

block_start(1;4;7).
block_end(3;6;9).

elem(page, div, root).
attr(page, class, ("min-h-screen";"flex";"justify-center";"bg-background";"text-foreground";"p-6")).

elem(board, div, page).
attr(board, class, ("flex";"flex-col";"gap-4";"w-fit")).

elem(header, div, board).
attr(header, class, ("flex";"items-center";"justify-between";"gap-4")).
attr(header, order, 1).

elem(header_title, div, header).
attr(header_title, class, ("flex";"items-center";"gap-2")).
attr(header_title, order, 1).

elem(title_icon, icon, header_title).
attr(title_icon, icon, "Grid3x3").
attr(title_icon, icon_size, "size-6").
attr(title_icon, order, 1).

elem(title_text, h1, header_title).
attr(title_text, text, "Sudoku").
attr(title_text, class, ("text-lg";"font-semibold")).
attr(title_text, order, 2).

elem(header_actions, div, header).
attr(header_actions, class, ("flex";"items-center";"gap-2")).
attr(header_actions, order, 2).

elem(next_button, button, header_actions).
attr(next_button, text, "Next").
attr(next_button, order, 1).
attr(next_button, size, "sm").
when(next_button, click, call, next_solution).

elem(next_icon, icon, next_button).
attr(next_icon, icon, "SkipForward").
attr(next_icon, order, 1).

elem(clear_button, button, header_actions).
attr(clear_button, text, "Clear").
attr(clear_button, variant, "outline").
attr(clear_button, size, "sm").
attr(clear_button, class, ("hover:text-destructive")).
attr(clear_button, order, 3).
when(clear_button, click, call, clear_assumptions).

elem(clear_icon, icon, clear_button).
attr(clear_icon, icon, "Trash2").
attr(clear_icon, order, 1).

elem(actions_sep, separator, header_actions).
attr(actions_sep, orientation, "vertical").
attr(actions_sep, class, ("h-5";"mx-1")).
attr(actions_sep, order, 3).

elem(theme_button, theme_toggle, header_actions).
attr(theme_button, variant, "ghost").
attr(theme_button, size, "icon-sm").
attr(theme_button, order, 4).

elem(main, main, page).
attr(main, class, ("grow";"flex";"items-start";"justify-start";"p-6")).
attr(main, order, 2).

elem(sudoku_grid, div, board).
attr(sudoku_grid, order, 2).
attr(sudoku_grid, class, ("grid";"grid-cols-9";"border-2";"border-foreground/60";"rounded-md";"overflow-hidden";"shadow-sm")).

elem(cell(X,Y), dropdown_menu, sudoku_grid) :- pos(X,Y).

% grid order: row first, then column.
attr(cell(X,Y), order, (Y-1)*9+X) :- pos(X,Y).

elem(cell_trigger(X,Y), dropdown_menu(trigger), cell(X,Y)) :- pos(X,Y).
attr(cell_trigger(X,Y), class, ("size-10";"sm:size-12";"flex";"items-center";"justify-center";"gap-1";"rounded-none";"border";"border-foreground/30";"text-base";"font-medium";"focus:z-10";"focus:outline-none";"disabled:cursor-default";"disabled:opacity-100")) :- pos(X,Y).

attr(cell_trigger(X,Y), class, "bg-muted") :- subgrid(X,Y,S), S\2 == 0.
attr(cell_trigger(X,Y), class, "bg-primary/25") :- subgrid(X,Y,S), S\2 != 0.

attr(cell_trigger(X,Y), class, "border-l-2") :- pos(X,Y), block_start(X).
attr(cell_trigger(X,Y), class, "border-r-2") :- pos(X,Y), block_end(X).
attr(cell_trigger(X,Y), class, "border-t-2") :- pos(X,Y), block_start(Y).
attr(cell_trigger(X,Y), class, "border-b-2") :- pos(X,Y), block_end(Y).

attr(cell_trigger(X,Y), disabled, true) :- initial(X,Y,V).
attr(cell_trigger(X,Y), class, ("font-bold";"text-foreground")) :- initial(X,Y,V).

attr(cell_trigger(X,Y), disabled, true) :- forced_value(X,Y,V).
attr(cell_trigger(X,Y), class, "text-muted-foreground") :- forced_value(X,Y,V).

attr(cell_trigger(X,Y), class, ("font-semibold";"text-blue-600";"dark:text-blue-400")) :- _clinguin_assume(sudoku(X,Y,V),true), not initial(X,Y,V).

elem(cell_text(X,Y), span, cell_trigger(X,Y)) :- shown_value(X,Y,V).
attr(cell_text(X,Y), text, V) :- shown_value(X,Y,V).
attr(cell_text(X,Y), order, 1) :- shown_value(X,Y,V).

editable_cell(X,Y) :- pos(X,Y), not initial(X,Y,_), not forced_value(X,Y,_).


elem(cell_chevron(X,Y), icon, cell_trigger(X,Y)) :- editable_cell(X,Y).
attr(cell_chevron(X,Y), icon, "ChevronDown") :- editable_cell(X,Y).
attr(cell_chevron(X,Y), icon_size, "size-3") :- editable_cell(X,Y).
attr(cell_chevron(X,Y), order, 2) :- editable_cell(X,Y).
attr(cell_chevron(X,Y), class, "text-muted-foreground") :- editable_cell(X,Y).
attr(cell_trigger(X,Y), class, "cursor-pointer") :- editable_cell(X,Y).

elem(cell_content(X,Y), dropdown_menu(content), cell(X,Y)) :- pos(X,Y).
attr(cell_content(X,Y), align, "center") :- pos(X,Y).
attr(cell_content(X,Y), class, ("w-24";"min-w-24";"max-h-80")) :- pos(X,Y).

elem(clear_cell(X,Y), dropdown_menu(item), cell_content(X,Y)) :- pos(X,Y).
attr(clear_cell(X,Y), text, "Clear") :- pos(X,Y).
attr(clear_cell(X,Y), variant, "destructive") :- pos(X,Y).
attr(clear_cell(X,Y), order, 1) :- pos(X,Y).
when(clear_cell(X,Y), click, call, remove_assumption_signature(sudoku(X,Y,any))) :- pos(X,Y).

elem(clear_cell_icon(X,Y), icon, clear_cell(X,Y)) :- pos(X,Y).
attr(clear_cell_icon(X,Y), icon, "Ban") :- pos(X,Y).

elem(cell_separator(X,Y), dropdown_menu(separator), cell_content(X,Y)) :- pos(X,Y).
attr(cell_separator(X,Y), order, 2) :- pos(X,Y).

elem(cell_item(X,Y,V), dropdown_menu(item), cell_content(X,Y)) :- pos(X,Y), val(V).
attr(cell_item(X,Y,V), text, V) :- pos(X,Y), val(V).
attr(cell_item(X,Y,V), order, V+2) :- pos(X,Y), val(V).
attr(cell_item(X,Y,V), disabled, true) :- pos(X,Y), val(V), not _any(sudoku(X,Y,V)).
attr(cell_item(X,Y,V), class, "text-destructive") :- pos(X,Y), val(V), not _any(sudoku(X,Y,V)).
when(cell_item(X,Y,V), click, call, add_assumption(sudoku(X,Y,V),true)) :- pos(X,Y), val(V), _any(sudoku(X,Y,V)).
