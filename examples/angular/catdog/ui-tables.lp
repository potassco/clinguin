elem(w, window, root).%%#(\label{ui:tables:elem:one}#)
attr(w, flex_direction, row).%%#(\label{ui:tables:attr:one}#)

elem(tables, container, w).%%#(\label{ui:tables:container:one}#)

elem(table(T), container, tables):- seat((T,_)).%%#(\label{ui:tables:container:two}#)
attr(table(T), order, T):- seat((T,_)).%%#(\label{ui:tables:attr:two}#)
attr(table(T), width, 200):- seat((T,_)).%%#(\label{ui:tables:attr:tri}#)
attr(table(T), class, ("bg-primary";"bg-opacity-25";"rounded";%%#(\label{ui:tables:class:one:a}#)
                       "d-flex";"flex-column";"align-items-start";%%#(\label{ui:tables:class:one:b}#)
                       "p-2";"m-2"%%#(\label{ui:tables:class:one:c}#)
                     )):- seat((T,_)).%%#(\label{ui:tables:class:one:d}#)

elem(table_label(T), label, table(T)):- seat((T,_)).%%#(\label{ui:tables:label:one}#)
attr(table_label(T), order, 1):- seat((T,_)).
attr(table_label(T), label, @concat("","Table",T)):- seat((T,_)).%%#(\label{ui:tables:label:tri}#)

elem(seat_dd((T,C)), dropdown_menu, table(T)):- seat((T,C)).%%#(\label{ui:tables:dropdown:one:a}#)
attr(seat_dd((T,C)), order, C+1):- seat((T,C)).%%#(\label{ui:tables:dropdown:one:b}#)
attr(seat_dd(S), class, ("btn-sm";"btn-primary";"m-2")):- seat(S).%%#(\label{ui:tables:dropdown:one:c}#)
attr(seat_dd(S), selected, P):- _all(assign(P,S)).%%#(\label{ui:tables:dropdown:one:d}#)

elem(seat_ddi(S,P), dropdown_menu_item, seat_dd(S)):-_any(assign(P,S)).%%#(\label{ui:tables:dropdown:two:a}#)
attr(seat_ddi(S,P), label, P):- _any(assign(P,S)).%%#(\label{ui:tables:dropdown:two:b}#)
when(seat_ddi(S,P), click, call, add_assumption(assign(P,S))):- %%#(\label{ui:tables:dropdown:two:c}#)
                     _any(assign(P,S)).
