#script(python)
from clingo.symbol import String
def concat(*args):
    return String(''.join([str(x).strip('"') for x in args]))
#end.
element(window, window, root).
attribute(window, resizable_x, 1).
attribute(window, resizable_y, 1).
attribute(window, child_layout, flex).

element(container(S), container, window):-semester(S).
attribute(container(S), child_layout, grid):-semester(S).

element(label(S), label, container(S)):-semester(S).
attribute(label(S), label, @concat("Semester ",S)):-semester(S).

element(dm(S), dropdown_menu, container(S)):-semester(S).
attribute(dm(S), grid_column, 1):-semester(S).
attribute(dm(S), selected, C):-in(C,S).

element(dmi(S,C), dropdown_menu_item, dm(S)):-_b(in(C,S)).
attribute(dmi(S,C), label, C):-_b(in(C,S)).
callback(dmi(S,C), click, add_assumption(in(C,S))):-_b(in(C,S)).
