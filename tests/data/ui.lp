
elem(w, window, root).
attr(w, class, ("min-h-screen"; "p-6"; "flex"; "flex-col"; "gap-6"; "logo-bg")).


elem(header, container, w).
attr(header, class, ("flex"; "items-center"; "justify-between"; "border-b"; "pb-4")).
attr(header, order, 1).

elem(title, text, header).
attr(title, text, "Clinguin v.3 Test").
attr(title, class, ("text-xl"; "font-semibold"; "inline-flex"; "items-center"; "gap-5"; "flex-row-reverse")).
attr(title, icon, "/assets/potassco-logo.svg").
attr(title, icon_size, "size-10").


elem(toggle, theme_toggle, header).
attr(toggle, icon_dark, "Sun").
attr(toggle, icon_light, "Moon").
attr(toggle, variant, "outline").
attr(toggle, class, ("p-2";"rounded-full")).


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
when(next_btn, click, call, set_external(find,true)).

elem(unsat_msg, sonner, w):-_clinguin_unsat.
attr(unsat_msg, title, "Unsatisfiable"):-_clinguin_unsat.
attr(unsat_msg, type, error):-_clinguin_unsat.

elem(toggle_btn, button, footer).
attr(toggle_btn, label, "Toggle content").
attr(content, visibility, hidden) :- _clinguin_external(content_hidden, true).

when(toggle_btn, click, call, set_external(content_hidden,true)) :-
    not _clinguin_external(content_hidden, true).
when(toggle_btn, click, call, set_external(content_hidden,false)) :-
    _clinguin_external(content_hidden, true).
