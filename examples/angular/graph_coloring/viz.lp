#const _color_primary= "#0052CC".
#const _color_secondary= "#6554C0".
#const _color_success= "#36B37E".
#const _color_info= "#B3BAC5".
#const _color_warning= "#FFAB00".
#const _color_danger= "#FF5630".
#const _color_light= "#F4F5F7".


color_hex(blue,@color(blue)).
color_hex(red,@color(red)).
color_hex(green,@color(green)).

attr(node, N, style, filled):- node(N).
attr(node, N, fillcolor, white):- node(N), not _all(assign(N,_)), not _clinguin_browsing.
attr(node, N, fillcolor, white):- node(N), not assign(N,_), _clinguin_browsing.
opacity(N,""):-_clinguin_assume(assign(N, _)).
opacity(N,"30"):- node(N), not _clinguin_assume(assign(N, _)).
attr(node, N, fillcolor, @concat(CH,O)):- assign(N, C), _clinguin_browsing, color_hex(C,CH), opacity(N,O).
attr(node, N, fillcolor, @concat(CH,O)):- _all(assign(N, C)), color_hex(C,CH), opacity(N,O).
attr(node, N, color, gray):- opacity(N,"30").
attr(node, N, fontcolor, gray):- opacity(N,"30").

