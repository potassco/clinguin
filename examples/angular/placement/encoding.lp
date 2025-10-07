
% #external setting_seats.
#external include(P):person(P).

1{assign(seat(S,T),P):seat(S,T)}1:-include(P).

:- assign(B,P1),assign(B,P2),P1<P2.

% Least tables selected
#minimize{1@2,T:assign(seat(_,T),_)}.

% Least empty seats possible
#minimize{1@1,S,T:seat(S,T),assign(seat(_,T),_),not assign(seat(S,T),_)}.

