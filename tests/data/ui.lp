
elem(w, window, root).
attr(w, class, ("min-h-screen"; "p-6"; "flex"; "flex-col"; "gap-6")).


elem(header, container, w).
attr(header, class, ("flex"; "items-center"; "justify-between"; "border-b"; "pb-4")).
attr(header, order, 1).

elem(title, text, header).
attr(title, text, "Solution Browser").
attr(title, class, ("text-xl"; "font-semibold")).

elem(toggle, theme_toggle, header).
attr(toggle, icon_dark, "Sun").
attr(toggle, icon_light, "Moon").
attr(toggle, class, ("p-2"; "rounded-md"; "hover:bg-gray-100")).


elem(content, container, w).
attr(content, class, ("flex"; "flex-row"; "gap-3"; "flex-wrap")).
attr(content, order, 2).

elem(card(X), container, content) :- object(X).
attr(card(X), class, ("flex"; "items-center"; "gap-2"; "px-3"; "py-2"; "border"; "border-gray-300"; "rounded-md")) :- object(X).

elem(label(X), text, card(X)) :- object(X).
attr(label(X), text, @stringify(X, true)) :- object(X).
attr(label(X), icon, "Dot") :- object(X).
attr(label(X), class, ("text-sm"; "font-medium")) :- object(X).


elem(footer, container, w).
attr(footer, class, ("flex"; "justify-end"; "border-t"; "pt-4")).
attr(footer, order, 3).

elem(next_btn, button, footer).
attr(next_btn, label, "Next solution").
attr(next_btn, icon, "ArrowRight").
when(next_btn, click, call, next_solution).
