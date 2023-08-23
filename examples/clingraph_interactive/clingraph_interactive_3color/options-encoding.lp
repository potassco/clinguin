option_context(node,P,select,change_color,C) :- assign(P,C). 
select_option(change_color,C) :- color(C). 
option_context(node,N,checkbox,set_important,true) :- node(N), user_input(node,N,checkbox,set_important,true). 
option_context(node,N,checkbox, set_important, false) :- node(N), not user_input(node,N,checkbox,set_important,true).

#show select_option/2.
#show option_context/5.