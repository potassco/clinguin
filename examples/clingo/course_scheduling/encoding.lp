#const n_semesters=4.
semester(1..n_semesters).
1{in(C,S) : course(C)}1:-semester(S).
:-in(C,S'),in(C,S),S<S'.