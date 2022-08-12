
node(tom,toms_family).
edge((tom,max),toms_family).
edge((bill,jen),bills_family).
graph(toms_family).
graph(bills_family).
node(max,toms_family).
node(bill,bills_family).
node(jen,bills_family).
attr(graph_nodes,bills_family,(color,-1),blue).
attr(graph_nodes,toms_family,(color,-1),red).

node(test).
