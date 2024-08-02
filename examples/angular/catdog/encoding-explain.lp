#include "encoding-explain-example.lp".

{assign(P,S):seat(S)}:- person(P,_).

:- person(P,_), not assign(P,_), cons(all_assigned, _).
:- assign(P,S), assign(P,S'), S>S', cons(in_only_one, _).
:- assign(P,S), assign(P',S), P'>P, cons(only_one, _).
:- assign(P,(T,_)), assign(P',(T,_)), person(P,cat), person(P',dog),
   cons(different_type, _).

cons(min,"Minimize").
cons(all_assigned,"All people need an assigned seat").
cons(in_only_one,"Each person can only have one seat").
cons(only_one,"Two people can not be seated on the same seat").
cons(different_type, "All people on a table must prefer the same pet").


