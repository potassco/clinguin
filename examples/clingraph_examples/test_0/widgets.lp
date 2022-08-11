element(window, window, root).

h(500).
w(500).

attribute(window, height, X) :- h(X).
attribute(window, width, X) :- w(X).
attribute(window, background_color, white).
%attribute(window, child_layout, absstatic).
attribute(window, resizable_x, 0).

element(frame, container, window).
attribute(frame, height, 450).
attribute(frame, width, 450).
attribute(frame, background_color, green).

element(canv, canvas, frame).
attribute(canv, image, clingraph).





node(oscar).
node(andres).
edge((oscar,andres)).
attr(node,andres,label,"Andres").
attr(node,oscar,label,"Oscar").
attr(edge,(oscar,andres),label,"friends").


