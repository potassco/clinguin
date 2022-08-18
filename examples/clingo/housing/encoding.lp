
{in_house(P)}:-person(P).
% :- #count{P : person(P), in_house(P)} > #count{P : person(P), in_house(P)}.

{assign(bed(N,R),P)}:-in_house(P),bed(N,R).

:- assign(B,P1),assign(B,P2),P1!=P2.
:- assign(B1,P),assign(B2,P),B1!=B2.
:- in_house(P), not assign(_,P).
