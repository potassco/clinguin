element(window, window, root).

attribute(window, height, 600).
attribute(window, width, 600).
attribute(window, child_layout, absstatic).

element(f1, container, window).
attribute(f1, background_color, "#ff0000").

element(b1, button, f1).
attribute(b1, label, "My button").
attribute(b1, background_color, "#00ff00").

