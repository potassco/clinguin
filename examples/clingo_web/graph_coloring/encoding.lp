{ assign(N, C) : color(C) } = 1 :- node(N).

:- edge((N, M)), assign(N, C), assign(M, C).