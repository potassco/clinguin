p(1) :- not p(2).
p(2) :- not p(1).

element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, backgroundcolor, white).

element(c, container, w).
attribute(c, width, 100).
attribute(c, height, 50).
attribute(c, borderwidth, 2).
attribute(c, onhover, true).
attribute(c, onhoverbackgroundcolor, blue).
attribute(c, onhoverbordercolor, red).

element(m, dropdownmenu, c).

element(mi(X), dropdownmenuitem, m) :- p(X).
attribute(mi(X), label, X) :- p(X).
attribute(m, selected, mi(X)) :- p(X).
callback(mi(X), click, assume(p(X))) :- p(X).

element(c2, container, w).
attribute(c2, width, 100).
attribute(c2, height, 50).
attribute(c2, borderwidth, 20).
attribute(c2, bordercolor, pink).
attribute(c2, backgroundcolor, red).




