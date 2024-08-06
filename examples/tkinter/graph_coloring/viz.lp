color_hex(blue,"#0052CC").
color_hex(red,"#FF5630").
color_hex(green,"#36B37E").

attr(node, N, style, filled):- node(N).
attr(node, N, fillcolor, white):- node(N), not _all(assign(N,_)), not _clinguin_browsing.
attr(node, N, fillcolor, white):- node(N), not assign(N,_), _clinguin_browsing.
opacity(N,""):-_clinguin_assume(assign(N, _),true).
opacity(N,"30"):- node(N), not _clinguin_assume(assign(N, _),true).
attr(node, N, fillcolor, @concat(CH,O)):- assign(N, C), _clinguin_browsing, color_hex(C,CH), opacity(N,O).
attr(node, N, fillcolor, @concat(CH,O)):- _all(assign(N, C)), color_hex(C,CH), opacity(N,O).
attr(node, N, color, gray):- opacity(N,"30").
attr(node, N, fontcolor, gray):- opacity(N,"30").


