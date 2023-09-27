#const _color_primary= "#0052CC".
#const _color_secondary= "#6554C0".
#const _color_success= "#36B37E".
#const _color_info= "#B3BAC5".
#const _color_warning= "#FFAB00".
#const _color_danger= "#FF5630".
#const _color_light= "#F4F5F7".

node(I) :- ast_node(I, _, _), ast_show(node, I).
edge(I) :- ast_edge(I, _, _), ast_show(edge, I).

attr(node, I, label, @concat(
    "<<table border='0' cellborder='1' cellspacing='0' cellpadding='3'>",
    "<tr>",
        "<td>{{id}}</td>",
        "<td>{{type}}</td>",
        "{% if variant %}<td>{{variant}}</td>{% endif %}",
    "</tr>",
    "{% if value %}",
        "<tr><td colspan='{{colspan}}'>",
            "<font face='monospace'> {{value}} </font>",
        "</td></tr>",
    "{% endif %}",
    "</table>>"
)) :- node(I).

attr(node, I, fillcolor, @concat(_color_secondary,"50"))
    :- node(I), _clinguin_context(selected_node, I).
attr(node, I, style, filled)
    :- node(I), _clinguin_context(selected_node, I).
attr(node, I, (label, id), I)
    :- node(I).
attr(node, I, (label, type), T)
    :- node(I), ast_node(I, type, T).
attr(node, I, (label, variant), V)
    :- node(I), ast_node(I, variant, V).
attr(node, I, (label, colspan), 2)
    :- node(I), ast_node(I, value, _), not ast_node(I, variant, _).
attr(node, I, (label, colspan), 3)
    :- node(I), ast_node(I, value, _), ast_node(I, variant, _).
attr(node, I, (label, value), @html_escape(V))
    :- node(I), ast_node(I, value, V).

attr(edge, I, label, L) :- edge(I), ast_edge(I, key, L).

attr(graph_nodes, default, fontsize, 10).
attr(graph_nodes, default, shape, plain).

attr(graph_edges, default, fontsize, 10).