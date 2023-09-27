#script(python)
from clingo.symbol import String
def concat(*args):
    return String(''.join([str(x).strip('"') for x in args]))
#end.

elem(window, window, root).
%attr(window, child_layout, flex).
%attr(window, flex_direction, column).
attr(window, child_layout, absstatic).

% A canvas, where images can be displayed.
elem(c, canvas, window).
attr(c, pos_x, 200).
attr(c, pos_y, 20).
attr(c, height, 500).
attr(c, width, 500).

% Specifying a special type from the ''clingraph-backend'' (not yet there).
attr(c, image_type, clingraph_svg).

%%%%%% Clingraph nodes from svg

% Creating nodes in the frontend - for svgs only
elem(n(X), svg_node, c) :- ast_show(node,X).
% For interactivity/callbacks it is necessary to specify some sort of id, which (might) differ from the clinguin id.
attr(n(X), id, X) :- ast_show(node,X).

%%%%%% Form 

elem(f, container, window).
attr(c, pos_x, 0).
attr(c, pos_y, 20).
attr(c, height, 30).
attr(c, width, 150).

elem(b, button, f).
attr(b, label, "Show Children").
when(b, click, callback, add_atom(show_children(_context_value(selected_node),true))).
attr(b, disabled, true).

%elem(f(X), container, window) :- ast_show(node,X).
%attr(f(X), visibility, hidden) :- ast_show(node,X).

%elem(l(X), label, f(X)) :- ast_show(node,X).
%attr(l(X), label, X) :- ast_show(node,X).

%elem(b(X), button, f(X)) :- ast_show(node,X).
%attr(b(X), label, "Show Children") :- ast_show(node,X).
%when(b(X), click, call, add_atom(show_children(X,true))) :- ast_show(node,X).


%%%%%%%%%%%% Interactivity predicate wit arity 4 might be better for the frontend and for clorm to give errors...


% One option using the same context to have a persistent context after calls to solver
% The context has as first argument some type of id so that it can be overwritten like a key-value pair
% Context is passed as a dictionaryy in the solve call {selected_node:xxx} then reified as input to the context selected_node(xxx)

when(n(X), click, context, (selected_node, X)):- ast_show(node,X).
when(n(X), click, update, (b, label, @concat("Show Children of: ", X))) :- ast_show(node,X).
when(n(X), click, update, (b, disabled, false)) :- ast_show(node,X).

% Update will change the value of an attribute directly to show the UI again
%   - Maybe some limitations are needed... like not positioning but only style
%when(n(X), click, update, (f(X), visibility, shown)):- ast_show(node,X).
%when(n(X), click, update, (f(Y), visibility, hidden)):- ast_show(node,X), ast_show(node,Y), X != Y.

% Keep Permanent changes using the _clinguin_context from the previous call
% attr(f(X), visibility, shown) :- ast_show(node,X). _clinguin_context(selected_node,X).
% attr(f(X), visibility, hidden) :- ast_show(node,X). not _clinguin_context(selected_node,X).

% Special predicate _value for the input value when the type of the call is input
%when(t(X), input, context, (name(X),_value)):- ast_show(node,X).
%when(c(X), input, context, (include(X),_value)):- ast_show(node,X).
% when(c(X), click, call, add_assumption(X)):- ast_show(node,X).

% Replace _ with context??
% but what if it is not given. could we add some sort of required fields? 
% when(c(X), click, call, add_assumption(select(_name(X),include(X)))):- ast_show(node,X).
% I think we don't want this here, this should be handled by the context!
% when(c(X), click, call, add_atom(select(_name(X),_include(X)))):- ast_show(node,X).

%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
elem(m, menu_bar, window).
elem(ms, menu_bar_section, m).
attr(m, title,"Interactive AST Example").
attr(ms, label, "Options").
elem(ms_clear, menu_bar_section_item, ms).
attr(ms_clear, label, "Clear").
when(ms_clear, click, call, clear_atoms).

