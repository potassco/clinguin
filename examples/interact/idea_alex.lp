element(window, window, root).

% A form container, which is a placeholder for possible forms
element(form_container, container, window).

% A canvas, where images can be displayed.
element(c, canvas, window).

% Specifying a special type from the ''clingraph-backend'' (not yet there).
attribute(c, image_type, clingraph).

% Specifying that we want an svg as an output, which enables interactivity.
attribute(c, image_type, svg).

% Creating nodes in the frontend - for svgs only
element(n(X), svg_node, c) :- node(X).
% For interactivity/callbacks it is necessary to specify some sort of id, which (might) differ from the clinguin id.
attribute(n(X), id, X) :- node(X).

% Interactivity predicate:
% Specifies that there should be some action purely in the frontend (e.g. on a press on an svg node a form should appear)
% What type of interactivty should be there.
interactivity(n(X), action_type, click) :- node(X).

% --- SUSANA MEETING --
% -> For now ignore interactivity_list(n(X)...) and svg_interactivity_target ...
% Interactivity for what svg-elements?
interactivity_list(n(X), svg_element, "g") :- node(X).
interactivity_list(n(X), svg_element, "circle") :- node(X).

% Svg specific - to what other svg-elements does interactivity apply? (e.g. consider <g> <title>#ID</title> ... </g>, then possibly also to title)
interactivity(n(X), svg_interactivity_target, ancestor) :- node(X).
% ----------------------

% Specify what shall happen on the click (says, something with form f(x))
interactivity(n(X), action, f(X)) :- node(X).
% Less/More general?
interactivity(n(x), action_type, show) :- node(X).

% The element where the form resides
element(f(X), form, form_container) :- node(X).

% If n(X) has action click, then f(X) should be shown
interactivity(f(X), shown_if, n(X)) :- node(X)

% Form elements [...]
element(b(X), button, f(X)) :- node(X).
attribute(b(X), label, "Assume Node") :- node(X).
callback(b(X), click, add_assumption(node(X))) :- node(X).