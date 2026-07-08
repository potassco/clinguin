food(pizza).
food(sushi).
food(burgers).
food(salad).
#include "instance.lp".

{preference(first,P,F):food(F)}1:-person(P).
{preference(second,P,F):food(F)}1:-person(P).
:- preference(first,P,F), preference(second,P,F).

1{chosen(F):food(F)}1.

happy(P):-preference(_,P,F),chosen(F).
number_happy(N):- #count{1,P: happy(P)}=N.

#minimize{1@4,T,P:preference(T,P,F)}.

#maximize{1@3,P:person(P), happy(P)}.
#maximize{1@2,P:chosen(F),preference(first,P,F)}.
#maximize{1@1,P:chosen(F),preference(second,P,F)}.
