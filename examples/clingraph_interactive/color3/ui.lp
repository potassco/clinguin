elem(window, window, root).
attr(window, child_layout, flex).
attr(window, flex_direction, row).


% A canvas, where images can be displayed.
elem(c, canvas, window).

% Specifying a special type from the ''clingraph-backend'' (not yet there).
attr(c, image_type, clingraph_svg).

%%%%%% Clingraph nodes from svg

% Creating nodes in the frontend - for svgs only
elem(n(X), svg_node, c) :- _clingraph(node(X)).
% For interactivity/callbacks it is necessary to specify some sort of id, which (might) differ from the clinguin id.
attr(n(X), id, X) :- _clingraph(node(X)).

%%%%%% Form 

elem(f(X), container, window) :- _clingraph(node(X)).
attr(f(X), visibility, hidden) :- _clingraph(node(X)).

elem(l(X), label, f(X)) :- _clingraph(node(X)).
attr(l(X), label, X) :- _clingraph(node(X)).

elem(d(X), dropdown_menu, f(X)) :- _clingraph(node(X)).
attr(d(X), selected, C) :- _clingraph(node(X)), _c(assign(X,C)).

elem(d(X,C), dropdown_menu_item, d(X)) :- _b(assign(X,C)).
attr(d(X,C), label, C) :- _b(assign(X,C)).

% when(d(X,C), click, context, (operation, (add_assumption(X), add_assumption(assign(X,C)))) :- _b(assign(X,C)).

when(d(X,C), click, context, (d(X), add_assumption(assign(X,C)))) :- _b(assign(X,C)).
when(d(X,C), click, update, (d(X), selected, C)) :- _b(assign(X,C)).

%elem(t(X), textbox, f(X)) :- _clingraph(node(X)).
%attr(t(X), label, "Name") :- _clingraph(node(X)).

%elem(c(X), checkbox, f(X)) :- _clingraph(node(X)).
%attr(c(X), label, "Include Node") :- _clingraph(node(X)).

elem(b(X), button, f(X)) :- _clingraph(node(X)).
attr(b(X), label, "Submit") :- _clingraph(node(X)).
when(b(X), click, call, transfer_context) :- _clingraph(node(X)).

%%%%%%%%%%%% Interactivity predicate wit arity 4 might be better for the frontend and for clorm to give errors...


% One option using the same context to have a persistent context after calls to solver
% The context has as first argument some type of id so that it can be overwritten like a key-value pair
% Context is passed as a dictionaryy in the solve call {selected_node:xxx} then reified as input to the context selected_node(xxx)
when(n(X), click, context, (selected_node, X)):- _clingraph(node(X)).

% Update will change the value of an attribute directly to show the UI again
%   - Maybe some limitations are needed... like not positioning but only style
when(n(X), click, update, (f(X), visibility, shown)):- _clingraph(node(X)).
when(n(X), click, update, (f(Y), visibility, hidden)):- _clingraph(node(X)), _clingraph(node(Y)), X != Y.

% Keep Permanent changes using the _clinguin_context from the previous call
% attr(f(X), visibility, shown) :- _clingraph(node(X)), _clinguin_context(selected_node,X).
% attr(f(X), visibility, hidden) :- _clingraph(node(X)), not _clinguin_context(selected_node,X).

% Special predicate _value for the input value when the type of the call is input
%when(t(X), input, context, (name(X),_value)):- _clingraph(node(X)).
%when(c(X), input, context, (include(X),_value)):- _clingraph(node(X)).
% when(c(X), click, call, add_assumption(X)):- _clingraph(node(X)).

% Replace _ with context??
% but what if it is not given. could we add some sort of required fields? 
% when(c(X), click, call, add_assumption(select(_name(X),include(X)))):- _clingraph(node(X)).
% I think we don't want this here, this should be handled by the context!
% when(c(X), click, call, add_atom(select(_name(X),_include(X)))):- _clingraph(node(X)).



%---------------------------------------------------------------------------------------
% Menu Bar
%---------------------------------------------------------------------------------------

% Menu bar
elem(m, menu_bar, window).
elem(ms, menu_bar_section, m).
attr(m, title,"Interactive 3-Color Example").
attr(ms, label, "Options").
elem(ms_clear, menu_bar_section_item, ms).
attr(ms_clear, label, "Clear").
when(ms_clear, click, call, clear_assumptions).
elem(ms_next, menu_bar_section_item, ms).
attr(ms_next, label, "Next").
when(ms_next, click, call, next_solution).

