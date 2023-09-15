#script(python)
from clingo.symbol import String
def concat(*args):
    return String(''.join([str(x).strip('"') for x in args]))
#end.

element(window, window, root).
%attribute(window, child_layout, flex).
%attribute(window, flex_direction, column).
attribute(window, child_layout, absstatic).

% A canvas, where images can be displayed.
element(c, canvas, window).
attribute(c, pos_x, 200).
attribute(c, pos_y, 20).
attribute(c, height, 500).
attribute(c, width, 500).

% Specifying a special type from the ''clingraph-backend'' (not yet there).
attribute(c, image_type, clingraph_svg).

%%%%%% Clingraph nodes from svg

% Creating nodes in the frontend - for svgs only
element(n(X), svg_node, c) :- ast_show(node,X).
% For interactivity/callbacks it is necessary to specify some sort of id, which (might) differ from the clinguin id.
attribute(n(X), id, X) :- ast_show(node,X).

%%%%%% Form 

element(f, container, window).
attribute(c, pos_x, 0).
attribute(c, pos_y, 20).
attribute(c, height, 30).
attribute(c, width, 150).

element(b, button, f).
attribute(b, label, "Show Children").
do(b, click, callback, add_atom(show_children(_value_context(selected_node),true))).
attribute(b, disabled, true).

%element(f(X), container, window) :- ast_show(node,X).
%attribute(f(X), visibility, hidden) :- ast_show(node,X).

%element(l(X), label, f(X)) :- ast_show(node,X).
%attribute(l(X), label, X) :- ast_show(node,X).

%element(b(X), button, f(X)) :- ast_show(node,X).
%attribute(b(X), label, "Show Children") :- ast_show(node,X).
%do(b(X), click, call, add_atom(show_children(X,true))) :- ast_show(node,X).


%%%%%%%%%%%% Interactivity predicate wit arity 4 might be better for the frontend and for clorm to give errors...


% One option using the same context to have a persistent context after calls to solver
% The context has as first argument some type of id so that it can be overwritten like a key-value pair
% Context is passed as a dictionaryy in the solve call {selected_node:xxx} then reified as input to the context selected_node(xxx)

do(n(X), click, context, (selected_node, X)):- ast_show(node,X).
do(n(X), click, update, (b, label, @concat("Show Children of: ", X))) :- ast_show(node,X).
do(n(X), click, update, (b, disabled, false)) :- ast_show(node,X).

% Update will change the value of an attribute directly to show the UI again
%   - Maybe some limitations are needed... like not positioning but only style
%do(n(X), click, update, (f(X), visibility, shown)):- ast_show(node,X).
%do(n(X), click, update, (f(Y), visibility, hidden)):- ast_show(node,X), ast_show(node,Y), X != Y.

% Keep Permanent changes using the _clinguin_context from the previous call
% attribute(f(X), visibility, shown) :- ast_show(node,X). _clinguin_context(selected_node,X).
% attribute(f(X), visibility, hidden) :- ast_show(node,X). not _clinguin_context(selected_node,X).

% Special predicate _value for the input value when the type of the call is input
%do(t(X), input, context, (name(X),_value)):- ast_show(node,X).
%do(c(X), input, context, (include(X),_value)):- ast_show(node,X).
% do(c(X), click, call, add_assumption(X)):- ast_show(node,X).

% Replace _ with context??
% but what if it is not given. could we add some sort of required fields? 
% do(c(X), click, call, add_assumption(select(_name(X),include(X)))):- ast_show(node,X).
% I think we don't want this here, this should be handled by the context!
% do(c(X), click, call, add_atom(select(_name(X),_include(X)))):- ast_show(node,X).

%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
element(m, menu_bar, window).
element(ms, menu_bar_section, m).
attribute(m, title,"Interactive AST Example").
attribute(ms, label, "Options").
element(ms_clear, menu_bar_section_item, ms).
attribute(ms_clear, label, "Clear").
do(ms_clear, click, call, clear_atoms).

