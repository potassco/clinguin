elem(seat_ddi(S,P), dropdown_menu_item, seat_dd(S)):-
                          not _any(assign(P,S)), person(P,_), seat(S).
attr(seat_ddi(S,P), label, P):-
                          not _any(assign(P,S)), person(P,_), seat(S).
when(seat_ddi(S,P), click, call, add_assumption(assign(P,S),true)):-
                          not _any(assign(P,S)), person(P,_), seat(S).
attr(seat_ddi(S,P), class, "text-danger"):-
                          not _any(assign(P,S)), person(P,_), seat(S).
attr(seat_dd(S), class, ("text-danger")):- _clinguin_mus(assign(P,S)).
