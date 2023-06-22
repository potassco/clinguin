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
    element(s(I), container, window):-I=1..n.
    attribute(s(I), child_layout, grid):-I=1..n.
    attribute(s(I), border_width, 1):-I=1..n.
    attribute(s(I), height, window_height):-I=1..n.
    attribute(s(I), width, semester_width):-I=1..n.
    attribute(s(I), grid_column, I):-I=1..n.

        % HEADER
        element(header(I), container, s(I)):-I=1..n.
        attribute(header(I), child_layout, grid):-I=1..n.
        propagate_attribute(header(I), background_color, header_color):-I=1..n.

            % HEADER LABEL
            element(slabel(I), label, header(I)):-I=1..n.
            attribute(slabel(I), label, @concat("Semester ",I)):-I=1..n.
            attribute(slabel(I), font_size,15):-I=1..n.
            attribute(slabel(I), height, 30):-I=1..n.
            attribute(slabel(I), width, semester_width):-I=1..n.

            % HEADER DROPDOWN
            element(sdd(I), dropdown_menu, header(I)):-I=1..n.
            attribute(sdd(I), grid_row, 1):-I=1..n.
            attribute(sdd(I), height, 50):-I=1..n.
            attribute(sdd(I), width, semester_width-30):-I=1..n.
            attribute(sdd(I), selected, "Add module"):-I=1..n.

                element(ddmi(E,I), dropdown_menu_item, sdd(I)):-_b(in(E,s(I))), not _c(in(E,s(I))).
                attribute(ddmi(E,I), label, E):-_b(in(E,s(I))), not _c(in(E,s(I))).
                callback(ddmi(E,I), click, add_assumption(in(E,s(I)))):-_b(in(E,s(I))), not _c(in(E,s(I))).

        % SELEETED MODULES
        element(sm(I), container, s(I)):-I=1..n.
        attribute(sm(I), grid_row, 2):-I=1..n.
        attribute(sm(I), height, 500):-I=1..n.
        attribute(sm(I), width, semester_width):-I=1..n.
        attribute(sm(I), border_width, 1):-I=1..n.

            % MODULE
            show_m(in(C,x(I))):-_c(in(C,x(I))).
            show_m(in(C,x(I))):-_clinguin_browsing, in(C,x(I)).
            show_m(in("",x(I))):- semester(I), not _clinguin_browsing, not _c(in(_,x(I))).
			      show_m(in("",x(I))):- semester(I), _clinguin_browsing, not in(_,x(I)).
            element(m(C,I), container, sm(I)):-show_m(in(C,x(I))).
            attribute(m(C,I), border_width, 1):-show_m(in(C,x(I))).
            attribute(m(C,I), child_layout, grid):-show_m(in(C,x(I))).
            propagate_attribute(m(C,I), background_color, module_color):-show_m(in(C,x(I))).

                % MODULE LABEL
                element(mlabel(E,I), label, m(E,I)):-show_m(in(E,s(I))).
                attribute(mlabel(E,I), label, E):-show_m(in(E,s(I))).

                % MODULE REMOVE
                element(mbutton(E,I), button, m(E,I)):-_clinguin_assume(in(E,s(I))).
                attribute(mbutton(E,I), label, "-"):-_clinguin_assume(in(E,s(I))).
                attribute(mbutton(E,I), grid_column, 1):-_clinguin_assume(in(E,s(I))).
                attribute(mbutton(E,I), foreground_color, red):-_clinguin_assume(in(E,s(I))).
                callback(mbutton(E,I), click, remove_assumption(in(E,s(I)))):-_clinguin_assume(in(E,s(I))).
