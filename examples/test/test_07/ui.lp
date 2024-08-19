elem(window, window, root).

attr(window, height, 500).
attr(window, width, 450).
attr(window, pos_x, 0).
attr(window, pos_y, 100).

elem(canvis(1), canvas, window).
attr(canvis(1), height, 500).
attr(canvis(1), width, 450).
attr(canvis(1), image, "examples/test/test_07/tommi.jpg").
attr(canvis(1), image, "examples/test/test_07/tommi.jpg").
attr(canvis(1), filter, "invert(1)").
when(canvis(1), click, update, (msg, visibility, shown)).

attr(canvis(1), resize, true).

elem(msg, message, window).
attr(msg, title, "Clicked").
attr(msg, visibility, "hidden").


