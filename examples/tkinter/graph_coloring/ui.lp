elem(window, window, root).
attr(window, child_layout, grid).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Canvas
    %%%%%%%%%%%%%%%%%%%%%%%%

    elem(canv, canvas, window).
    attr(canv, image, clingraph__default).
    attr(canv, width, 250).
    attr(canv, height, 250).
    attr(canv, resize, true).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Edition container
    %%%%%%%%%%%%%%%%%%%%%%%%

    elem(node(N), container, window):-node(N).
    attr(node(N), width, 200):-node(N).
    attr(node(N), height, 30):-node(N).
    attr(node(N), grid_row, N):-node(N).
    attr(node(N), child_layout, grid):-node(N).

        elem(l(N), label, node(N)):-node(N).
        attr(l(N), grid_column, 0):-node(N).
        attr(l(N), label, N):-node(N).

        %%%%%%%%%%%%%%%%%%%%%%%%
        % Dropdown
        %%%%%%%%%%%%%%%%%%%%%%%%

        elem(dmc(N), dropdown_menu, node(N)):-node(N).
        attr(dmc(N), grid_column, 1):-node(N).
        attr(dmc(N), width, 100):-node(N).
        attr(dmc(N), height, 30):-node(N).
        attr(dmc(N), selected, C):-assign(N,C), _clinguin_browsing.
        attr(dmc(N), selected, C):-_c(assign(N,C)).
        when(dmc(N), clear, call, remove_assumption_signature(assign(N,any))) :- node(N).

            elem(dmi(N,C), dropdown_menu_item, dmc(N)):-_b(assign(N,C)).
            attr(dmi(N,C), label, C):-_b(assign(N,C)).
            when(dmi(N,C), click, call, add_assumption(assign(N,C))):-_b(assign(N,C)).

