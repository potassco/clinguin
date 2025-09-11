1 { lives(P,R) : region(R) } 1 :- person(P).

&sus{ 0 } =: deduction(P) :- person(P), not deduction(P,_,_).
&in{ L..H } =: deduction(P) :- deduction(P,L,H).
&sus{ T } =: rate(P) :- lives(P,R), income(P,I),
                        T = #max{ T' : rate(R,L,T'), I>=L}.

&sus{ I*rate(P)-100*deduction(P) } =: 100*tax(P) :- income(P,I).
&sus{ tax(P) : lives(P,R) } =: total(R) :- region(R).
&min{ tax(P) : person(P) } =: min.
&max{ tax(P) : person(P) } =: max.
min_taxes(P) :- &min{ tax(P') : person(P') } = tax(P), person(P).
max_taxes(P) :- &max{ tax(P') : person(P') } = tax(P), person(P).

#show lives/2.
#show min_taxes/1.
#show max_taxes/1.
