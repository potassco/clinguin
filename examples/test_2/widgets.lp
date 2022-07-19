p(1) :- not p(2).
p(2) :- not p(1).

element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, backgroundcolor, black).

element(m, dropdownmenu, w).
attribute(m, height, 20).
attribute(m, width, 50).

element(mi(X), dropdownmenuitem, m) :- p(X).
%attribute(m, selected, mi(X)) :- p(X).
callback(mi(X), click, assume(p(X))) :- p(X).






