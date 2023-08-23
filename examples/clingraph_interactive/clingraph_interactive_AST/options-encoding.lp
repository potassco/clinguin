option_context(node,P,checkbox,show_children,false) :- ast_show(node,P), user_input(node,P,checkbox,show_children,false).
option_context(node,P,checkbox,show_children,true) :- ast_show(node,P), user_input(node,P,checkbox,show_children,true).
option_context(node,P,checkbox,show_children,false) :- ast_show(node,P), not user_input(node,P,checkbox,show_children,_).


#show option_context/5.
