elem(w, window, root).
attr(w, class, ("d-inline-flex")).


elem(coll(P),collapse, w):-root(P).
elem(coll(P),collapse, child(P')):-skill(P), parent(P,P'), not leaf(P).
elem(coll(P),button, child(P')):-skill(P), parent(P,P'), leaf(P).
attr(coll(P),icon, "fa-hand-point-right"):-parent(P',P).
attr(coll(P),icon, "fa-medal"):-leaf(P), _all(master(P)).
attr(coll(P),class, "text-success"):- _all(master(P)).
attr(coll(P),class, "text-dark"):-leaf(P), not _all(master(P)).
attr(coll(P),icon, "fa-circle-xmark"):-leaf(P), _all(fail(P)).
when(coll(P),click, call, add_assumption(master(P),true)):-leaf(P).


attr(coll(P),label, P):-skill(P).
attr(coll(P),collapsed, false):-skill(P).

elem(child(P),container, coll(P)):-skill(P).
attr(child(P),class, ("ps-4";"border-start")):-skill(P).



elem(side,sidebar, w).
attr(side,title, "Instance Manager").
attr(side,position, end).
attr(side,class, ("bg-primary";"bg-opacity-10")).

file(F):- _clinguin_optional_file(F).
elem(files,container, side).

    elem(file(F),checkbox, files):-file(F).
    attr(file(F),label, F):-file(F).
    attr(file(F),checked, true):-_clinguin_active_file(F).
    when(file(F), click, call, activate_file(F)):-file(F), not _clinguin_active_file(F).
    when(file(F), click, call, deactivate_file(F)):-file(F), _clinguin_active_file(F).

elem(fi, file_input, side).
attr(fi, accept, ".lp").
attr(fi, order, 1).
when(fi, file_selected, (upload_file(_value),activate_file(_value))).


%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar
%%%%%%%%%%%%%%%%%%%%%%%%
elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Skill manager").
attr(menu_bar, icon, "fa-hand-holding-heart").

