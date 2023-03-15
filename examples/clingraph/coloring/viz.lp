attr(node, N, style, filled):- node(N).
attr(node, N, color, C):- assign(N, C), clinguin_browsing.
attr(node, N, color, C):- _c(assign(N, C)).

