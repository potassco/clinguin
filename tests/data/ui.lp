elem(w, window, root).
attr(w, class, ("flex"; "flex-col"; "gap-4"; "p-4")).

elem(b, button, w).
attr(b, label, "Next").
attr(b, variant, "primary").
attr(b, class, ("hover:bg-blue-600";"bg-gray-500";"text-white";"order-1")).
attr(b, order, 1).
when(b, click, call, next_solution).

elem(c, container, w).
attr(c, class, ("p-2";"border";"border-gray-300";"rounded-md"; "flex"; "flex-row";"justify-evenly";"order-2")).
attr(c, order, 2).

elem(objects(X), container, c) :- object(X).
attr(objects(X), class, ("p-2";"border";"border-gray-300";"rounded-md";"text-center")) :- object(X).

elem(l(X), label, objects(X)) :- object(X).
attr(l(X), label, @stringify(X, true)) :- object(X).
attr(l(X), class, ("text-sm";"font-medium";"p-2")) :- object(X).
