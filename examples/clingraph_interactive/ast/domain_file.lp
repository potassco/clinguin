#defined user_input/5.
#defined show_children/2.
#defined show_all/0.

ast_show(node,0).
ast_ancestor(0,0).
ast_ancestor(A,N) :- ast_edge(I, _, _), I = (A, N), ast_show(node, A), ast_show(node,N).
ast_ancestor(A,N) :- ast_edge(I1, _,_), I1 = (A,P), ast_ancestor(P,N).

ast_show(node, C) :- ast_edge((P,C),_,_), show_children(P,true), not ast_node(C, type, "Location").
ast_show(edge, I) :- ast_edge(I, _, _), I = (I1, I2), ast_show(node, I1), ast_show(node,I2).

ast_show(node, C) :- show_all, ast_edge((P,C),_,_), ast_ancestor(A,P), not ast_node(C, type, "Location").
ast_show(edge, I) :- show_all, ast_edge(I, _, _), I = (I1, I2), ast_show(node, I1), ast_show(node,I2).


