
{assign(bed(N,R),P)}:-person(P),bed(N,R).

:- assign(B,P1),assign(B,P2),P1!=P2.
:- assign(B1,P),assign(B2,P),B1!=B2.
:- person(P), not assign(_,P).

% free(bed(N,R)):- not assign(bed(N,R),_), assign(bed()).
% Least rooms possible
#minimize{1,R:assign(bed(_,R),_)}.

% Least epty beds possible
#minimize{1,B,R:bed(B,R),assign(bed(_,R),_),not assign(bed(B,R),_)}.
