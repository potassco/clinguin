elem(w, window, root).
elem(b1, button, w).
attr(b1, label, "Button 1").
when(b1, click, call, next_solution).