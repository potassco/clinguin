
p(1) :- not p(2).
p(2) :- not p(1).


t(1..3).
r(1..3).
pos(T,R) :- t(T), r(R).


