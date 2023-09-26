elem(window, window, root).

% A form container, which is a placeholder for possible forms
elem(sb, sidebar, window).

% A form container, which is a placeholder for possible forms
% elem(form_container, container, window).

% A canvas, where images can be displayed.
elem(c, canvas, window).

% Specifying a special type from the ''clingraph-backend'' (not yet there).
attr(c, image_type, clingraph_svg).

% Specifying that we want an svg as an output, which enables interactivity.
% attr(c, image_type, svg).

%%%%%% Clingrph nodes from svg

% Creating nodes in the frontend - for svgs only
elem(n(X), svg_node, c) :- _clingraph(node(X)).
% For interactivity/callbacks it is necessary to specify some sort of id, which (might) differ from the clinguin id.
attr(n(X), id, X) :- _clingraph(node(X)).

%%%%%% Form 

elem(f(X), container, sb) :- _clingraph(node(X)).
attr(f(X), visibility, hidden) :- _clingraph(node(X)).

    elem(t(X), textbox, f(X)) :- _clingraph(node(X)).
    attr(t(X), label, "Name") :- _clingraph(node(X)).

    elem(c(X), checkbox, f(X)) :- _clingraph(node(X)).
    attr(c(X), label, "Include Node") :- _clingraph(node(X)).

    elem(b(X), button, f(X)) :- _clingraph(node(X)).
    attr(b(X), label, "Submit") :- _clingraph(node(X)).



%%%%%%%%%%%% Interactivity predicate wit arity 4 might be better for the frontend and for clorm to give errors...


% One option using the same context to have a persistent context after calls to solver
% The context has as first argument some type of id so that it can be overwritten like a key-value pair
% Context is passed as a dictionaryy in the solve call {selected_node:xxx} then reified as input to the context selected_node(xxx)
when(n(X), click, context, (selected_node, X)):- _clingraph(node(X)).

% Update will change the value of an attribute directly to show the UI again
%   - Maybe some limitations are needed... like not positioning but only style
when(n(X), click, update, (f(X), visibility, shown)):- _clingraph(node(X)).
when(n(X), click, update, (f(Y), visibility, hidden)):- _clingraph(node(X)), _clingraph(node(Y)).

when(n(X), click, update, (n(X), opacity, "1")):- _clingraph(node(X)).
when(n(X), click, update, (n(Y), opacity, "0.2")):- _clingraph(node(X)),  _clingraph(node(X)).


% Keep Permanent changes using the _clinguin_context from the previous call
attr(f(X), visibility, shown) :- _clingraph(node(X)), _clinguin_context(selected_node,X).
attr(f(X), visibility, hidden) :- _clingraph(node(X)), not _clinguin_context(selected_node,X).

% Special predicate _value for the input value when the type of the call is input
when(t(X), input, context, (name(X),_value)):- _clingraph(node(X)).
when(c(X), input, context, (include(X),_value)):- _clingraph(node(X)).
% when(c(X), click, call, add_assumption(X)):- _clingraph(node(X)).

% Replace _ with context??
% but what if it is not given. could we add some sort of required fields? 
% when(c(X), click, call, add_assumption(select(_name(X),include(X)))):- _clingraph(node(X)).
when(c(X), click, call, add_atom(select(_name(X),_include(X)))):- _clingraph(node(X)).
when(c(X), click, call, add_atom(select(_value(name(X)),_value(_include(X))))):- _clingraph(node(X)).


%%%%%%%%%%%%