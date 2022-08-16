floor(0..10).
init_on(1).
n_floors(10).



#program base.
holds(on(F),0) :- init_on(F). 
holds(called(6),0).

#program step(t).

#external query(t).
#external check(t).
#external call(F,t):floor(F).

holds(called(F),t):-call(F,t).
action(up;down;serve;wait).
1 { occ(A,t): action(A)} 1.

holds(on(F+1),t) :- occ(up,t), holds(on(F),t-1).
holds(on(F-1),t) :- occ(down,t), holds(on(F),t-1).
holds(on(F),t) :- occ(wait,t), holds(on(F),t-1).
holds(on(F),t) :- occ(serve,t), holds(on(F),t-1).
served(F,t) :-  occ(serve,t), holds(on(F),t-1).
holds(called(F),t) :- holds(called(F),t-1), not served(F,t).

:- occ(up,t), holds(on(F),t-1), not floor(F+1).
:- occ(down,t), holds(on(F),t-1), not floor(F-1).
:- occ(serve,t), holds(on(F),t-1), not holds(called(F),t-1).

goal(t):- #count{F:holds(called(F),t)}==0, query(t).
:-check(t), not goal(t).


