elem(w, window, root).
attr(w, class, ("d-flex";"flex-row")).


%%%%%%%%%%%%%%%%%%%%%%%%
% Objects
%%%%%%%%%%%%%%%%%%%%%%%%
elem(b, button, w).
attr(b, label, "not").


elem(objects(X), container, w):-object(X).
attr(objects(X), class, ("p-2";"bg-primary";"border")):-object(X).
attr(objects(X), class, ("custom-class")):-object(X).
attr(objects(X), width, 300):-object(X).
attr(objects(a), draggable_as, a):-object(a).
when(objects(b), drop, call, add_assumption(_dragged,true)):-object(b).

elem(l(X), label, objects(X)):-object(X).
attr(l(X), label, @stringify(X,true)):-object(X).
