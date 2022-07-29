p(1) :- not p(2).
p(2) :- not p(1).

element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, backgroundcolor, white).
attribute(w, childorg, relstatic).

element(c, container, w).
attribute(c, width, 250).
attribute(c, height, 150).
attribute(c, borderwidth, 2).
attribute(c, onhover, true).
attribute(c, onhoverbackgroundcolor, blue).
attribute(c, onhoverbordercolor, red).
attribute(c, posx, 25).
attribute(c, posy, 0).
attribute(c, childorg, absstatic).

element(cc, container, c).
attribute(cc, width, 100).
attribute(cc, height, 50).
attribute(cc, backgroundcolor, green).
attribute(cc, borderwidth, 2).
attribute(cc, posx, 0).
attribute(cc, posy, 0).

element(ccc, container, c).
attribute(ccc, width, 100).
attribute(ccc, height, 50).
attribute(ccc, backgroundcolor, yellow).
attribute(ccc, borderwidth, 2).
attribute(ccc, posx, 0).
attribute(ccc, posy, 50).

element(m, dropdownmenu, ccc).
attribute(m, backgroundcolor, black).
attribute(m, foregroundcolor, white).
attribute(m, onhover, true).
attribute(m, onhoverbackgroundcolor, white).
attribute(m, onhoverforegroundcolor, black).

element(mi(X), dropdownmenuitem, m) :- p(X).
attribute(mi(X), label, X) :- p(X).
attribute(m, selected, X) :- p(X).
callback(mi(X), click, assume(p(X))) :- p(X).

element(c2, container, w).
attribute(c2, width, 100).
attribute(c2, height, 50).
attribute(c2, borderwidth, 20).
attribute(c2, bordercolor, pink).
attribute(c2, backgroundcolor, red).
attribute(c2, posx, 40).
attribute(c2, posy, 50).


element(c4, container, c).
attribute(c4, width, 146).
attribute(c4, height, 146).
attribute(c4, backgroundcolor, beige).
attribute(c4, posx, 100).
attribute(c4, posy, 0).
attribute(c4, childorg, grid).
attribute(c4, padx, 10).
attribute(c4, pady, 10).

t(1..3).
r(1..3).
pos(T,R) :- t(T), r(R).

element(c(X,Y), container, c4) :- pos(X,Y).
attribute(c(X,Y), width, 48) :- pos(X,Y).
attribute(c(X,Y), height, 48) :- pos(X,Y).
attribute(c(X,Y), gridx, X) :- pos(X,Y).
attribute(c(X,Y), gridy, Y) :- pos(X,Y).
attribute(c(X,Y), backgroundcolor, pink) :- pos(X,Y), (X + Y) \ 2 = 0.
attribute(c(X,Y), backgroundcolor, red) :- pos(X,Y), (X + Y) \ 2 = 1.




