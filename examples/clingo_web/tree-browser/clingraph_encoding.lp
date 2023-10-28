
attr(graph,default,fontname,@clinguin_fontname).
attr(graph,default,size,"10,10!").
attr(graph_nodes,default,fontname,@clinguin_fontname):-node(X).

node(X):-group(X).
attr(node,X,label,@stringify(X,true)):-group(X).
attr(node,X,style,"filled"):-node(X).
attr(node,X,fillcolor,@color(blue,50)):-node(X),parent(X,_).
attr(node,X,fillcolor,@color(yellow,50)):-node(X), not parent(X,_).

edge((X,Y)):-parent(X,Y).

