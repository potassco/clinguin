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
attribute(frame, width, 500).
attribute(frame, background_color, green).
attribute(frame, pos_x, 0).
attribute(frame, pos_y, 25).

element(canv, canvas, frame).
attribute(canv, image, "./out/toms_family.png").
attribute(canv, width, 250).
attribute(canv, height, 250).
attribute(canv, resize, false).

element(bf, container, window).
attribute(bf, height, 75).
attribute(bf, width, 150).
attribute(bf, background_color, pink).
attribute(bf, pos_x, 175).
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




