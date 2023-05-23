#script(python)
from clingo.symbol import String
def concat(*args):
    return String(''.join([str(x).strip('"') for x in args]))
#end.

attribute(E,A,V):-propagate_attribute(E,A,V).
propagate_attribute(E',A,V):-propagate_attribute(E,A,V),element(E',_,E).

#const semester_width = 150.
#const window_height = 580.
#const module_color = "#F0EEEE".
#const header_color = "#CCC5D3".

% WINDOW
element(window, window, root).
attribute(window, child_layout, grid).

    % SEMESTER
    element(s(I), container, window):-semester(I).
    attribute(s(I), child_layout, grid):-semester(I).
    attribute(s(I), border_width, 1):-semester(I).
    attribute(s(I), height, window_height):-semester(I).
    attribute(s(I), width, semester_width):-semester(I).
    attribute(s(I), grid_column, I):-semester(I).

        % HEADER
        element(header(I), container, s(I)):-semester(I).
        attribute(header(I), child_layout, grid):-semester(I).
        propagate_attribute(header(I), background_color, header_color):-semester(I).

            % HEADER LABEL
            element(slabel(I), label, header(I)):-semester(I).
            attribute(slabel(I), label, @concat("Semester ",I)):-semester(I).
            attribute(slabel(I), font_size,15):-semester(I).
            attribute(slabel(I), height, 30):-semester(I).
            attribute(slabel(I), width, semester_width):-semester(I).

            % HEADER DROPDOWN
            element(sdd(I), dropdown_menu, header(I)):-semester(I).
            attribute(sdd(I), grid_row, 1):-semester(I).
            attribute(sdd(I), height, 50):-semester(I).
            attribute(sdd(I), width, semester_width-30):-semester(I).
            attribute(sdd(I), selected, "Add module"):-semester(I).

                element(ddmi(C,I), dropdown_menu_item, sdd(I)):-_b(in(C,x(I))), not _c(in(C,x(I))).
                attribute(ddmi(C,I), label, C):-_b(in(C,x(I))), not _c(in(C,x(I))).
                callback(ddmi(C,I), click, add_assumption(in(C,x(I)))):-_b(in(C,x(I))), not _c(in(C,x(I))).

        % SELECTED MODULES
        element(sm(I), container, s(I)):-semester(I).
        attribute(sm(I), grid_row, 2):-semester(I).
        attribute(sm(I), height, 500):-semester(I).
        attribute(sm(I), width, semester_width):-semester(I).
        attribute(sm(I), border_width, 1):-semester(I).

            % MODULE
            show_m(in(C,x(I))):-_c(in(C,x(I))).
            show_m(in(C,x(I))):-_clinguin_browsing, in(C,x(I)).
            element(m(C,I), container, sm(I)):-show_m(in(C,x(I))).
            attribute(m(C,I), border_width, 1):-show_m(in(C,x(I))).
            attribute(m(C,I), child_layout, grid):-show_m(in(C,x(I))).
            propagate_attribute(m(C,I), background_color, module_color):-show_m(in(C,x(I))).

                % MODULE LABEL
                element(mlabel(C,I), label, m(C,I)):-show_m(in(C,x(I))).
                attribute(mlabel(C,I), label, C):-show_m(in(C,x(I))).

                % MODULE REMOVE
                element(mbutton(C,I), button, m(C,I)):-_clinguin_assume(in(C,x(I))).
                attribute(mbutton(C,I), label, "-"):-_clinguin_assume(in(C,x(I))).
                attribute(mbutton(C,I), grid_column, 1):-_clinguin_assume(in(C,x(I))).
                attribute(mbutton(C,I), foreground_color, red):-_clinguin_assume(in(C,x(I))).
                callback(mbutton(C,I), click, remove_assumption(in(C,x(I)))):-_clinguin_assume(in(C,x(I))).
