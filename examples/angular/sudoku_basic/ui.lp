elem(window,window,root).
attr(window,child_layout,grid).
attr(window,class,("justify-content-start")).

    elem(dd(X,Y),dropdown_menu,window):-pos(X,Y).
    attr(dd(X,Y),width,50):-pos(X,Y).
    attr(dd(X,Y),height,50):-pos(X,Y).
    attr(dd(X,Y),grid_column,X):-pos(X,Y).
    attr(dd(X,Y),grid_row,Y):-pos(X,Y).
    attr(dd(X,Y),class,("border-dark";"bg-primary")):-pos(X,Y).
    attr(dd(X,Y),class,"bg-opacity-50"):-subgrid(X,Y,S), S\2!=0.
    attr(dd(X,Y),selected,V):-_all(sudoku(X,Y,V)).

        elem(ddv(X,Y,V),dropdown_menu_item,dd(X,Y)):-_any(sudoku(X,Y,V)).
        attr(ddv(X,Y,V),label,V):-_any(sudoku(X,Y,V)).
        when(ddv(X,Y,V),click,call,add_assumption(sudoku(X,Y,V),true)):-_any(sudoku(X,Y,V)).
