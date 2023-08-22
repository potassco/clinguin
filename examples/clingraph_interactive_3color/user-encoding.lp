assign(N,C) :- node(N), color(C), user_input(node,N,select, change_color,C).
#show attr(node, N, label, "Important!") : user_input(node,N,checkbox,set_important,true).