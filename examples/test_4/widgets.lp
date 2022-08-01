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


