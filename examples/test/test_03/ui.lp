elem(w, window, root).
attr(w, height, 500).
attr(w, width, 500).
attr(w, background_color, white).
attr(w, child_layout, relstatic).

    elem(c, container, w).
    attr(c, width, 250).
    attr(c, height, 150).
    attr(c, border_width, 2).
    attr(c, on_hover, true).
    attr(c, on_hover_background_color, blue).
    attr(c, on_hover_border_color, red).
    attr(c, pos_x, 25).
    attr(c, pos_y, 0).
    attr(c, child_layout, absstatic).

        elem(cc, container, c).
        attr(cc, width, 100).
        attr(cc, height, 50).
        attr(cc, background_color, green).
        attr(cc, border_width, 2).
        attr(cc, pos_x, 0).
        attr(cc, pos_y, 0).

        elem(m, dropdown_menu, c).
        attr(m, width, 100).
        attr(m, height, 50).
        attr(m, pos_x, 0).
        attr(m, pos_y, 50).
        attr(m, background_color, black).
        attr(m, foreground_color, white).
        attr(m, on_hover, true).
        attr(m, on_hover_background_color, white).
        attr(m, on_hover_foreground_color, black).

            elem(mi(X), dropdown_menu_item, m) :- _any(p(X)).
            attr(mi(X), label, X) :- _any(p(X)).
            when(mi(X), click, callback, add_assumption(p(X),true)) :- _any(p(X)).
            attr(m, selected, X) :- _all(p(X)).

        elem(c4, container, c).
        attr(c4, width, 146).
        attr(c4, height, 146).
        attr(c4, background_color, beige).
        attr(c4, pos_x, 100).
        attr(c4, pos_y, 0).
        attr(c4, child_layout, grid).

            elem(c(X,Y), container, c4) :- pos(X,Y).
            attr(c(X,Y), width, 48) :- pos(X,Y).
            attr(c(X,Y), height, 48) :- pos(X,Y).
            attr(c(X,Y), grid_column, X) :- pos(X,Y).
            attr(c(X,Y), grid_row, Y) :- pos(X,Y).
            attr(c(X,Y), background_color, pink) :- pos(X,Y), (X + Y) \ 2 = 0.
            attr(c(X,Y), background_color, red) :- pos(X,Y), (X + Y) \ 2 = 1.

    elem(l1, label, w).
    attr(l1, background_color, blue).
    attr(l1, foreground_color, brown).
    attr(l1, label, "Clear!").
    attr(l1, on_hover, true).
    attr(l1, on_hover_background_color, gray).
    attr(l1, on_hover_foreground_color, beige).
    attr(l1, font_size, 15).
    attr(l1, font_weight, "i").
    attr(l1, width, 100).
    attr(l1, height, 50).
    attr(l1, pos_x, 40).
    attr(l1, pos_y, 50).
    when(l1, click, callback, clear_assumptions).

    elem(b, button, w).
    attr(b, background_color, blue).
    attr(b, foreground_color, brown).
    attr(b, label, "Clear!").
    attr(b, on_hover, true).
    attr(b, on_hover_background_color, gray).
    attr(b, on_hover_foreground_color, beige).
    attr(b, font_size, 18).
    attr(b, font_weight, "bi").
    attr(b, width, 100).
    attr(b, height, 50).
    attr(b, pos_x, 40).
    attr(b, pos_y, 70).
    when(b, click, callback, clear_assumptions).


