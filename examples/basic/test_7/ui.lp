element(window, window, root).

attribute(window, height, 600).
attribute(window, width, 600).

element(canv, canvas, window).
attribute(canv, image_path, "./examples/basic/test_7/tommi.jpg").
attribute(canv, width, 500).
attribute(canv, height, 500).
attribute(canv, resize, true).

element(l, label, window).
attribute(l, label, "This should be displayed somewhere on the screen.").
attribute(l, background_color, pink).

