element(w, window, root).
attribute(w, height, 500).
attribute(w, width, 500).
attribute(w, backgroundcolor, white).
attribute(w, childorg, relstatic).

element(m, menubar, w).

element(ms1, menubarsection, m).
attribute(ms1, label, "File").

element(ms1i1, menubarsectionitem, ms1).
attribute(ms1i1, label, "Open").
element(ms1i2, menubarsectionitem, ms1).
attribute(ms1i2, label, "Close").
callback(ms1i2, click, clear).

element(ms2, menubarsection, m).
element(ms2i2, menubarsectionitem, ms2).

element(c, container, w).
attribute(c, width, 250).
attribute(c, height, 150).
attribute(c, borderwidth, 2).
attribute(c, onhover, true).
attribute(c, onhoverbackgroundcolor, blue).
attribute(c, onhoverbordercolor, red).
attribute(c, posx, 25).
attribute(c, posy, 0).
attribute(c, childorg, absstatic).

element(b, button, c).
attribute(b, backgroundcolor, blue).
attribute(b, foregroundcolor, brown).
attribute(b, label, "Clear!").
attribute(b, onhover, true).
attribute(b, onhoverbackgroundcolor, gray).
attribute(b, onhoverforegroundcolor, beige).
attribute(b, fontsize, 15).
callback(b, click, clear).

element(c2, container, w).
attribute(c2, width, 180).
attribute(c2, height, 180).
attribute(c2, borderwidth, 2).
attribute(c2, onhover, true).
attribute(c2, onhoverbackgroundcolor, blue).
attribute(c2, onhoverbordercolor, red).
attribute(c2, posx, 25).
attribute(c2, posy, 50).
attribute(c2, childorg, grid).

element(c20, container, c2).
attribute(c20, width, 120).
attribute(c20, height, 60).
attribute(c20, backgroundcolor, red).
attribute(c20, gridcolumn, 0).
attribute(c20, gridrow, 0).
attribute(c20, gridcolumnspan, 2).
attribute(c20, gridrowspan, 1).

element(c21, container, c2).
attribute(c21, width, 60).
attribute(c21, height, 120).
attribute(c21, backgroundcolor, blue).
attribute(c21, gridcolumn, 2).
attribute(c21, gridrow, 0).
attribute(c21, gridcolumnspan, 1).
attribute(c21, gridrowspan, 2).

element(c22, container, c2).
attribute(c22, width, 60).
attribute(c22, height, 120).
attribute(c22, backgroundcolor, green).
attribute(c22, gridcolumn, 0).
attribute(c22, gridrow, 1).
attribute(c22, gridcolumnspan, 1).
attribute(c22, gridrowspan, 2).

element(c23, container, c2).
attribute(c23, width, 120).
attribute(c23, height, 60).
attribute(c23, backgroundcolor, pink).
attribute(c23, gridcolumn, 1).
attribute(c23, gridrow, 2).
attribute(c23, gridcolumnspan, 2).
attribute(c23, gridrowspan, 1).

element(c24, container, c2).
attribute(c24, width, 60).
attribute(c24, height, 60).
attribute(c24, backgroundcolor, black).
attribute(c24, gridcolumn, 1).
attribute(c24, gridrow, 1).
attribute(c24, gridcolumnspan, 1).
attribute(c24, gridrowspan, 1).












