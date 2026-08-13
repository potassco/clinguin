elem(w,window,root).
attr(w, class, ("min-h-screen"; "flex"; "flex-col"; "bg-muted")).

elem(main,container,w).
attr(main, class, ("flex"; "items-center"; "justify-center"; "p-6"; "grow")).
attr(main, order, 2).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Grid
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(sudoku,container,main).
    attr(sudoku, class, ("grid"; "grid-cols-9"; "grid-rows-9"; "bg-card"; "border"; "border-dark")).

        %%%%%%%%%%%%%%%%%%%%%%%%
        % Cell dropdown
        %%%%%%%%%%%%%%%%%%%%%%%%
        elem(dd(X,Y), dropdown_menu, sudoku) :- pos(X,Y).
        attr(dd(X,Y), class, @concat("col-start-", X)) :- pos(X,Y).
		attr(dd(X,Y), class, @concat("row-start-", Y)) :- pos(X,Y).
		attr(dd(X,Y), class, ("size-12"; "flex"; "items-center"; "justify-center";
							"border"; "border-border"; "text-lg"; "font-medium";
							"cursor-pointer"; "select-none")) :- pos(X,Y).
		attr(dd(X,Y), class, "bg-muted") :- subgrid(X,Y,S), S\2==0.
		attr(dd(X,Y), class, "bg-card") :- subgrid(X,Y,S), S\2!=0.
		attr(dd(X,Y), class, ("font-bold"; "text-foreground"; "pointer-events-none")) :- initial(X,Y,V).
		attr(dd(X,Y), disabled, "true") :- initial(X,Y,V).
		attr(dd(X,Y), disabled, "true") :- _all(sudoku(X,Y,V)), not _clinguin_assume(sudoku(X,Y,V), true), not initial(X,Y,V).
		attr(dd(X,Y), class, ("text-primary"; "dark:text-green-500")) :- _clinguin_assume(sudoku(X,Y,V), true).
		attr(dd(X,Y), class, ("text-muted-foreground"; "pointer-events-none")) :- _all(sudoku(X,Y,V)), not _clinguin_assume(sudoku(X,Y,V), true), not initial(X,Y,V).
		attr(dd(X,Y), label, V) :- _all(sudoku(X,Y,V)).
		attr(dd(X,Y), label, V) :- sudoku(X,Y,V), _clinguin_browsing.

			elem(ddc(X,Y), dropdown_menu_content, dd(X,Y)) :- pos(X,Y).
			attr(ddc(X,Y), class, ("w-40")) :- pos(X,Y).

				%%%%%%%%%%%%%%%%%%%%%%%%
				% Cell items
				%%%%%%%%%%%%%%%%%%%%%%%%
				elem(remove(X,Y), dropdown_menu_item, ddc(X,Y)) :- pos(X,Y).
				attr(remove(X,Y), label, "Clear") :- pos(X,Y).
				attr(remove(X,Y), variant, "destructive") :- pos(X,Y).
				attr(remove(X,Y), order, 0) :- pos(X,Y).
				when(remove(X,Y), click, call, remove_assumption_signature(sudoku(X,Y,any))) :- pos(X,Y).

					elem(remove_icon(X,Y), icon, remove(X,Y)) :- pos(X,Y).
					attr(remove_icon(X,Y), icon, "Ban") :- pos(X,Y).

				elem(ddi(X,Y,V), dropdown_menu_item, ddc(X,Y)) :- pos(X,Y), val(V).
				attr(ddi(X,Y,V), label, V) :- pos(X,Y), val(V).
				attr(ddi(X,Y,V), order, V) :- pos(X,Y), val(V).
				attr(ddi(X,Y,V), class, ("pointer-events-none"; "opacity-50")) :- pos(X,Y), val(V), not _any(sudoku(X,Y,V)).
				when(ddi(X,Y,V), click, call, add_assumption(sudoku(X,Y,V), true)) :- pos(X,Y), val(V).


%%%%%%%%%%%%%%%%%%%%%%%%
% Header
%%%%%%%%%%%%%%%%%%%%%%%%
elem(header, container, w).
attr(header, class, ("flex"; "items-center"; "justify-between"; "px-6"; "py-4"; "bg-card"; "border-b"; "shadow-sm")).
attr(header, order, 1).

	elem(header_left, container, header).
	attr(header_left, class, ("flex"; "items-center"; "gap-2")).
	attr(header_left, order, 1).

		elem(title_icon, icon, header_left).
		attr(title_icon, icon, "Grid3x3").
		attr(title_icon, order, 1).

		elem(title_text, text, header_left).
		attr(title_text, text, "Sudoku").
		attr(title_text, order, 2).
		attr(title_text, class, ("text-lg"; "font-semibold")).

	elem(header_right, container, header).
	attr(header_right, class, ("flex"; "items-center"; "gap-2")).
	attr(header_right, order, 2).

		elem(header_clear, button, header_right).
		attr(header_clear, label, "Clear").
		attr(header_clear, variant, "outline").
		attr(header_clear, order, 1).
		when(header_clear, click, call, clear_assumptions).

			elem(header_clear_icon, icon, header_clear).
			attr(header_clear_icon, icon, "Trash2").

		elem(header_select, button, header_right).
		attr(header_select, label, "Select solution").
		attr(header_select, variant, "outline").
		attr(header_select, order, 2).
		when(header_select, click, call, select).

			elem(header_select_icon, icon, header_select).
			attr(header_select_icon, icon, "MousePointerClick").

		elem(header_next, button, header_right).
		attr(header_next, label, "Next").
		attr(header_next, variant, "outline").
		attr(header_next, order, 3).
		when(header_next, click, call, next_solution).

			elem(header_next_icon, icon, header_next).
			attr(header_next_icon, icon, "SkipForward").

		elem(theme_toggle, theme_toggle, header_right).
		attr(theme_toggle, order, 4).
		attr(theme_toggle, icon_dark, "Moon").
		attr(theme_toggle, icon_light, "Sun").
		attr(theme_toggle, variant, "outline").
		attr(theme_toggle, class, ("p-2"; "rounded-full")).
