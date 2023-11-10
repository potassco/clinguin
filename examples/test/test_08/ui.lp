elem(window, window, root).

attr(window, height, 600).
attr(window, width, 600).
attr(window, child_layout, absstatic).

elem(f1, container, window).
attr(f1, background_color, "#ff0000").

elem(b1, button, f1).
attr(b1, label, "My button").
attr(b1, background_color, "#00ff00").

elem(m1, message, window).
attr(m1, type, info).
attr(m1, title, "INFO").
attr(m1, message, "INFO MESSAGE").

elem(m2, message, window).
attr(m2, type, error).
attr(m2, title, "ERROR").
attr(m2, message, "ERROR MESSAGE").

elem(m3, message, window).
attr(m3, type, warning).
attr(m3, title, "WARNING").
attr(m3, message, "WARNING MESSAGE").




