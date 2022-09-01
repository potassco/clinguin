2{selected(V0,V1) : edge((V0,V1)); selected(V2,V0) : edge((V2,V0))}2 :- node(V0).

r(V) :- selected(0,V).
r(V1) :- selected(V0, V1), r(V0).
r(V0) :- selected(V0, V1), r(V1).

:- node(V), not r(V).


%#minimize{C:cost(C)}.

