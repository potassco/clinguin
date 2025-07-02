% {master(P)}:-skill(P).

leaf(P):-skill(P), not parent(_,P).
root(P):-skill(P), not parent(P,_).

{master(P);fail(P)}1:-skill(P).

master(P):- skill(P), not leaf(P), #false: relative(P',P), skill(P'), not master(P').

relative(P,P''):-parent(P, P''), parent(P',P'').
