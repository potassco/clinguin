element(window, window, root).

h(500).
w(500).

attribute(window, height, X) :- h(X).
attribute(window, width, X) :- w(X).
attribute(window, background_color, white).
attribute(window, child_layout, absstatic).
attribute(window, resizable_x, 0).

element(frame, container, window).
attribute(frame, height, 300).
attribute(frame, width, 250).
attribute(frame, background_color, green).
attribute(frame, pos_x, 0).
attribute(frame, pos_y, 25).

element(canv, canvas, frame).
attribute(canv, image, clingraph_default).
attribute(canv, width, 200).
attribute(canv, height, 200).

element(frame2, container, window).
attribute(frame2, height, 300).
attribute(frame2, width, 250).
attribute(frame2, background_color, gray).
attribute(frame2, pos_x, 250).
attribute(frame2, pos_y, 25).

element(canv2, canvas, frame2).
attribute(canv2, image, clingraph).
attribute(canv2, width, 200).
attribute(canv2, height, 200).

element(bf, container, window).
attribute(bf, height, 75).
attribute(bf, width, 150).
attribute(bf, background_color, pink).
attribute(bf, pos_x, 275).
attribute(bf, pos_y, 375).

element(l1, label, bf).
attribute(l1, background_color, blue).
attribute(l1, foreground_color, brown).
attribute(l1, label, "Next Image").
attribute(l1, on_hover, true).
attribute(l1, on_hover_background_color, gray).
attribute(l1, on_hover_foreground_color, beige).
attribute(l1, font_size, 15).
callback(l1, click, nextGraph).

element(message, message, window) :- no_more_graphs.
attribute(message, title, "Finished") :- no_more_graphs.
attribute(message, message, "No more graphs available.") :- no_more_graphs.

%--------------------------------------------------------
element(c2, container, window).
attribute(c2, width, 150).
attribute(c2, height, 75).
attribute(c2, border_width, 1).
attribute(c2, border_color, pink).
attribute(c2, background_color, white).
attribute(c2, pos_x, 75).
attribute(c2, pos_y, 375).
attribute(c2, on_hover, true).
attribute(c2, on_hover_background_color, gray).
callback(c2, click, clear).

element(l2, label, c2).
attribute(l2, background_color, blue).
attribute(l2, foreground_color, brown).
attribute(l2, label, "Clear!").
attribute(l2, on_hover, true).
attribute(l2, on_hover_background_color, gray).
attribute(l2, on_hover_foreground_color, beige).
attribute(l2, font_size, 15).
callback(l2, click, clear).




