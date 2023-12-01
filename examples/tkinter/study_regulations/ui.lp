#script(python)
from clingo.symbol import String
def concat(*args):
    return String(''.join([str(x).strip('"') for x in args]))
#end.

attr(E,A,V):-propagate_attr(E,A,V).
propagate_attr(E',A,V):-propagate_attr(E,A,V),elem(E',_,E).

#const semester_width = 150.
#const window_height = 580.
#const module_color = "#F0EEEE".
#const header_color = "#CCC5D3".

%%%%%%%%%%%%%%%%%%%%%%%%
% WINDOW
%%%%%%%%%%%%%%%%%%%%%%%%
elem(window, window, root).
attr(window, child_layout, grid).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % SEMESTER
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(s(I), container, window):-I=1..n.
    attr(s(I), child_layout, grid):-I=1..n.
    attr(s(I), border_width, 1):-I=1..n.
    attr(s(I), height, window_height):-I=1..n.
    attr(s(I), width, semester_width):-I=1..n.
    attr(s(I), grid_column, I):-I=1..n.

        %%%%%%%%%%%%%%%%%%%%%%%%
        % HEADER
        %%%%%%%%%%%%%%%%%%%%%%%%
        elem(header(I), container, s(I)):-I=1..n.
        attr(header(I), child_layout, grid):-I=1..n.
        propagate_attr(header(I), background_color, header_color):-I=1..n.

            %%%%%%%%%%%%%%%%%%%%%%%%
            % HEADER LABEL
            %%%%%%%%%%%%%%%%%%%%%%%%
            elem(slabel(I), label, header(I)):-I=1..n.
            attr(slabel(I), label, @concat("Semester ",I)):-I=1..n.
            attr(slabel(I), font_size,15):-I=1..n.
            attr(slabel(I), height, 30):-I=1..n.
            attr(slabel(I), width, semester_width):-I=1..n.

            %%%%%%%%%%%%%%%%%%%%%%%%
            % HEADER DROPDOWN
            %%%%%%%%%%%%%%%%%%%%%%%%
            elem(sdd(I), dropdown_menu, header(I)):-I=1..n.
            attr(sdd(I), grid_row, 1):-I=1..n.
            attr(sdd(I), height, 50):-I=1..n.
            attr(sdd(I), width, semester_width-30):-I=1..n.
            attr(sdd(I), selected, "Add module"):-I=1..n.

                elem(ddmi(E,I), dropdown_menu_item, sdd(I)):-_any(in(E,s(I))), not _all(in(E,s(I))).
                attr(ddmi(E,I), label, E):-_any(in(E,s(I))), not _all(in(E,s(I))).
                when(ddmi(E,I), click, call, add_assumption(in(E,s(I)))):-_any(in(E,s(I))), not _all(in(E,s(I))).

        %%%%%%%%%%%%%%%%%%%%%%%%
        % SELEETED MODULES
        %%%%%%%%%%%%%%%%%%%%%%%%
        elem(sm(I), container, s(I)):-I=1..n.
        attr(sm(I), grid_row, 2):-I=1..n.
        attr(sm(I), height, 500):-I=1..n.
        attr(sm(I), width, semester_width):-I=1..n.
        attr(sm(I), border_width, 1):-I=1..n.

            %%%%%%%%%%%%%%%%%%%%%%%%
            % MODULE
            %%%%%%%%%%%%%%%%%%%%%%%%
            show_m(in(E,s(I))):-_all(in(E,s(I))).
            show_m(in(E,s(I))):-_clinguin_browsing, in(E,s(I)).
            elem(m(E,I), container, sm(I)):-show_m(in(E,s(I))).
            attr(m(E,I), border_width, 1):-show_m(in(E,s(I))).
            attr(m(E,I), child_layout, grid):-show_m(in(E,s(I))).
            propagate_attr(m(E,I), background_color, module_color):-show_m(in(E,s(I))).

                %%%%%%%%%%%%%%%%%%%%%%%%
                % MODULE LABEL
                %%%%%%%%%%%%%%%%%%%%%%%%
                elem(mlabel(E,I), label, m(E,I)):-show_m(in(E,s(I))).
                attr(mlabel(E,I), label, E):-show_m(in(E,s(I))).

                %%%%%%%%%%%%%%%%%%%%%%%%
                % MODULE REMOVE
                %%%%%%%%%%%%%%%%%%%%%%%%
                elem(mbutton(E,I), button, m(E,I)):-_clinguin_assume(in(E,s(I))).
                attr(mbutton(E,I), label, "-"):-_clinguin_assume(in(E,s(I))).
                attr(mbutton(E,I), grid_column, 1):-_clinguin_assume(in(E,s(I))).
                attr(mbutton(E,I), foreground_color, red):-_clinguin_assume(in(E,s(I))).
                when(mbutton(E,I), click, call, remove_assumption(in(E,s(I)))):-_clinguin_assume(in(E,s(I))).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Menu Bar
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(menu_bar, menu_bar, window).
    elem(menu_bar_section, menu_bar_section, menu_bar).
    attr(menu_bar_section, label, "Options").
    elem(menu_bar_section_clear, menu_bar_section_item, menu_bar_section).
    attr(menu_bar_section_clear, label, "Clear").
    attr(menu_bar_section_clear, accelerator, "Cmd+C").
    when(menu_bar_section_clear, click, call, clear_assumptions).
    elem(menu_bar_section_next, menu_bar_section_item, menu_bar_section).
    attr(menu_bar_section_next, label, "Next").
    attr(menu_bar_section_next, accelerator, "Cmd+N").
    when(menu_bar_section_next, click, call, next_solution).
    elem(menu_bar_section_select, menu_bar_section_item, menu_bar_section).
    attr(menu_bar_section_select, label, "Select").
    attr(menu_bar_section_select, accelerator, "Cmd+S").
    when(menu_bar_section_select, click, call, select).
