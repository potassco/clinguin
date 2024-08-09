{assign(P,S):seat(S)}:- person(P,_).

:- person(P,_), #count{S:assign(P, S)}!=1, cons(exacly_one, _).
:- assign(P,S), assign(P',S), P'>P, cons(only_one, _).
:- assign(P,(T,_)), assign(P',(T,_)), person(P,cat), person(P',dog),
   cons(different_type, _).

cons(exacly_one, "All people need exactly one seat").
cons(only_one, "Two people can not be seated on the same seat").
cons(different_type, "All people on a table must prefer the same pet").