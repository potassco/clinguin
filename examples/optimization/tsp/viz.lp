attr(node, N, style, filled) :- node(N).
attr(edge, (V0, V1), label, C) :- weight(V0, V1, C).
attr(edge, (V0, V1), color, red) :- selected(V0,V1).

