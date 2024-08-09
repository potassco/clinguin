elem(w, window, root).
attr(w, flex_direction, row).

elem(tables, container, w).

elem(table(T), container, tables):- seat((T,_)).
attr(table(T), order, T):- seat((T,_)).
attr(table(T), width, 200):- seat((T,_)).
attr(table(T), class, ("bg-primary";"bg-opacity-25";"rounded";
                       "d-flex";"flex-column";"align-items-start";
                       "p-2";"m-2"
                     )):- seat((T,_)).

elem(table_label(T), label, table(T)):- seat((T,_)).
attr(table_label(T), order, 1):- seat((T,_)).
attr(table_label(T), label, @concat("","Table",T)):- seat((T,_)).

elem(seat_dd((T,C)), dropdown_menu, table(T)):- seat((T,C)).
attr(seat_dd((T,C)), order, C+1):- seat((T,C)).
attr(seat_dd(S), class, ("btn-sm";"btn-primary";"m-2")):- seat(S).
attr(seat_dd(S), selected, P):- _clinguin_assume(assign(P,S),true).

elem(seat_ddi(S,P), dropdown_menu_item, seat_dd(S)):-_any(assign(P,S)).
attr(seat_ddi(S,P), label, P):- _any(assign(P,S)).
when(seat_ddi(S,P), click, call, add_assumption(assign(P,S))):-
                     _any(assign(P,S)).


%------------------------------
% Extension from the paper
% -----------------------------
elem(seat_ddi(S,remove), dropdown_menu_item, seat_dd(S)):- seat(S).
attr(seat_ddi(S,remove), label, "-"):- seat(S).
when(seat_ddi(S,remove), click, call, remove_assumption_signature(assign(any,(S)))):- seat(S).
