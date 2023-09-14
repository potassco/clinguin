element(w, window, root).
attribute(w, child_layout, absstatic).

element(c1, container, w).
attribute(c1, pos_x, 0).
attribute(c1, pos_y, 0).
attribute(c1, height, 200).
attribute(c1, width, 500).
attribute(c1, child_layout, flex).
attribute(c1, flex_direction, row_reverse).

element(t1, textfield, c1).
attribute(t1, placeholder, "Type Name Here").
do(t1, type, context, (t1_content, _value)).


element(b1, button, c1).
do(b1, click, callback, add_atom(name(_value_context(t1_content)))).
attribute(b1, label, "Add Name").

element(c2, container, w).
attribute(c2, pos_x, 0).
attribute(c2, pos_y, 250).
attribute(c2, height, 200).
attribute(c2, width, 500).
attribute(c2, child_layout, flex).
attribute(c2, flex_direction, column).

element(c3(X), container, c2) :- name(X).
attribute(c3(X), child_layout, flex) :- name(X).
attribute(c3(X), flex_direction, row) :- name(X).

element(l(X), label, c3(X)) :- name(X).
attribute(l(X), label, X) :- name(X).
attribute(l(X), background_color, "#00ff00") :- name(X).

element(b(X), button, c3(X)) :- name(X).
attribute(b(X), label, "Remove Name") :- name(X).
do(b(X), click, callback, remove_atom(name(X))) :- name(X).

