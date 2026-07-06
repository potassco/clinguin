#const n_pigeons = 4.
%#const n_boxes = 5.

pigeon(1..n_pigeons).
box(1..n_pigeons+1).

1 { in(P,B) : box(B) } 1 :- pigeon(P).
:- 2 { in(P,B) : pigeon(P) }, box(B).
