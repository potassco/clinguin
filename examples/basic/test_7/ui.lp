element(window, window, root).

attribute(window, height, 50) :- h(X).
attribute(window, width, 50) :- w(X).
attribute(window, child_layout, grid).

element(canvas_c, container, window).
attribute(canvas_c, fit, true).
attribute(canvas_c, background_color, green).

element(canv, canvas, canvas_c).

attribute(canv, image_path, "./examples/basic/test_7/tommi.jpg").
attribute(canv, width, 250).
attribute(canv, height, 250).
attribute(canv, resize, true).

