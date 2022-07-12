
element(window, window, root).

attribute(window, height, 500).
attribute(window, width, 500).
attribute(window, bgc, black).

attribute(window, corg, grid).
attribute(window, corg_col, 2).
attribute(window, corg_row, 1).

element(c0, container, window).
attribute(c0, height, 300).
attribute(c0, width, 200).
attribute(c0, bgc, blue).
attribute(c0, gridx, 0).
attribute(c0, gridy, 0).

element(c1, container, window).
attribute(c1, height, 300).
attribute(c1, width, 200).
attribute(c1, bgc, blue).
attribute(c1, gridx, 0).
attribute(c1, gridy, 0).

callback(c0, click, assume(c0)).
callback(c1, click, solve()).
