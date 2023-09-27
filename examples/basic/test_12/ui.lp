elem(w, window, root).
attr(w, child_layout, absstatic).

elem(c1, container, w).
attr(c1, pos_x, 0).
attr(c1, pos_y, 0).
attr(c1, height, 200).
attr(c1, width, 500).
attr(c1, child_layout, flex).
attr(c1, flex_direction, row_reverse).

elem(t1, textfield, c1).
attr(t1, placeholder, "Type Name Here").
when(t1, type, context, (t1_content, _value)).


elem(b1, button, c1).
when(b1, click, callback, add_atom(name(_context_value(t1_content)))).
attr(b1, label, "Add Name").

elem(c2, container, w).
attr(c2, pos_x, 0).
attr(c2, pos_y, 250).
attr(c2, height, 200).
attr(c2, width, 500).
attr(c2, child_layout, flex).
attr(c2, flex_direction, column).

elem(c3(X), container, c2) :- name(X).
attr(c3(X), child_layout, flex) :- name(X).
attr(c3(X), flex_direction, row) :- name(X).

elem(l(X), label, c3(X)) :- name(X).
attr(l(X), label, X) :- name(X).
attr(l(X), background_color, "#00ff00") :- name(X).

elem(b(X), button, c3(X)) :- name(X).
attr(b(X), label, "Remove Name") :- name(X).
when(b(X), click, callback, remove_atom(name(X))) :- name(X).

