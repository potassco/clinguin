
elem(window,window,root).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Grid
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(sudoku,container,window).
    attr(sudoku,child_layout,grid).
    attr(sudoku,width,100).
    attr(sudoku,height,100).

        %%%%%%%%%%%%%%%%%%%%%%%%
        % Cell dropdown
        %%%%%%%%%%%%%%%%%%%%%%%%
        elem(pos(X,Y),dropdown_menu,sudoku):-pos(X,Y).
        attr(pos(X,Y),width,50):-pos(X,Y).
        attr(pos(X,Y),height,50):-pos(X,Y).
        attr(pos(X,Y),grid_column,X):-pos(X,Y).
        attr(pos(X,Y),grid_row,Y):-pos(X,Y).
        attr(pos(X,Y),class,"border-dark"):-pos(X,Y).
        attr(pos(X,Y),class,"bg-primary"):-pos(X,Y), not _clinguin_mus(sudoku(X,Y,_)), not _clinguin_mus(initial(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(sudoku(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(initial(X,Y,_)).
        attr(pos(X,Y),class,"bg-opacity-10"):-subgrid(X,Y,S), S\2==0.
        attr(pos(X,Y),class,"bg-opacity-50"):-subgrid(X,Y,S), S\2!=0.
        attr(pos(X,Y),class,("opacity-100";"disabled";"fw-bold";"text-dark")):-initial(X,Y,V).
        attr(pos(X,Y),class,("text-primary")):-_clinguin_assume(sudoku(X,Y,V),true).
        attr(pos(X,Y),selected,V):-initial(X,Y,V).
        attr(pos(X,Y),selected,V):-sudoku(X,Y,V), _clinguin_browsing.
        attr(pos(X,Y),selected,V):-_clinguin_assume(sudoku(X,Y,V),true).

            %%%%%%%%%%%%%%%%%%%%%%%%
            % Cell items
            %%%%%%%%%%%%%%%%%%%%%%%%
            elem(remove(X,Y), dropdown_menu_item, pos(X,Y)):-pos(X,Y).
            attr(remove(X,Y), icon, ("fa-ban";"text-info")):-pos(X,Y).
            when(remove(X,Y), click, call, remove_assumption_signature(sudoku(X,Y,any))):-pos(X,Y).

            elem(pos_v(X,Y,V),dropdown_menu_item,pos(X,Y)):-pos(X,Y), val(V).
            attr(pos_v(X,Y,V),class,("text-danger")):-pos(X,Y), val(V), not _any(sudoku(X,Y,V)).
            attr(pos_v(X,Y,V),label,V):-pos(X,Y), val(V).
            when(pos_v(X,Y,V),click,call,(remove_assumption_signature(sudoku(X,Y,any)),
                                        add_assumption(sudoku(X,Y,V),true)))
                :-pos(X,Y), val(V).


%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar
%%%%%%%%%%%%%%%%%%%%%%%%
elem(menu_bar, menu_bar, window).
attr(menu_bar, title, "Sudoku").
attr(menu_bar, icon, "fa-table-cells").

    elem(menu_bar_clear, button, menu_bar).
    attr(menu_bar_clear, label, "Clear").
    attr(menu_bar_clear, icon, "fa-trash").
    attr(menu_bar_clear, class, ("btn-outline-danger";"border-0")).
    when(menu_bar_clear, click, callback, clear_assumptions).

    elem(menu_bar_select, button, menu_bar).
    attr(menu_bar_select, label, "Select solution").
    attr(menu_bar_select, icon, "fa-hand-pointer").
    when(menu_bar_select, click, callback, select).

    elem(menu_bar_next, button, menu_bar).
    attr(menu_bar_next, label, "Next").
    attr(menu_bar_next, icon, "fa-forward-step").
    when(menu_bar_next, click, callback, next_solution).