attr(node, N, style, filled):- node(N).
attr(node, N, fillcolor, white):- node(N), not _c(assign(N,_)), not _clinguin_browsing.
attr(node, N, fillcolor, white):- node(N), not assign(N,_), _clinguin_browsing.
opacity(N,""):-_clinguin_assume(assign(N, _)).
opacity(N,"30"):- node(N), not _clinguin_assume(assign(N, _)).
color_hex(blue,"#42b0f5").
color_hex(red,"#ed5345").
color_hex(green,"#6ac25d").
attr(node, N, fillcolor, @concat(CH,O)):- assign(N, C), _clinguin_browsing, color_hex(C,CH), opacity(N,O).
attr(node, N, fillcolor, @concat(CH,O)):- _c(assign(N, C)), color_hex(C,CH), opacity(N,O).
attr(node, N, color, gray):- opacity(N,"30").
attr(node, N, fontcolor, gray):- opacity(N,"30").

