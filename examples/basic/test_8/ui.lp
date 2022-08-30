element(window, window, root).

attribute(window, height, 600).
attribute(window, width, 600).
attribute(window, child_layout, absstatic).

element(f1, container, window).
attribute(f1, background_color, "#ff0000").

element(b1, button, f1).
attribute(b1, label, "My button").
attribute(b1, background_color, "#00ff00").

element(m1, message, window).
attribute(m1, type, info).
attribute(m1, title, "INFO").
attribute(m1, message, "MESSAGE").

element(m2, message, window).
attribute(m2, type, error).
attribute(m2, title, "ERROR").
attribute(m2, message, "MESSAGE").

element(m3, message, window).
attribute(m3, type, warning).
attribute(m3, title, "WARNING").
attribute(m3, message, "MESSAGE").




