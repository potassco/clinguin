object(a).
object(b).

1{object(c);object(d)}1.


#const n=10.
#external find.
pigeon(1..n+1). box(1..n).
1 { in(X,Y) : box(Y) } 1 :- pigeon(X), find.
:- 2 { in(X,Y) : pigeon(X) },  box(Y), find.
