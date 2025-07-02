elem(w, window, root).
attr(w, class, ("d-inline-flex")).

elem(buttons, container, w).
attr(buttons, order, 1).
attr(buttons, class, ("d-flex";"flex-row";"pb-4")).

    elem(collapse_all, button, buttons).
    attr(collapse_all, label, "Collapse all").
    attr(collapse_all, class, ("btn-sm";"btn-outline-dark";"m-2")).
    attr(collapse_all, icon, ("fa-down-left-and-up-right-to-center")).
    when(collapse_all, click, update, (coll(P),collapsed,true)):-elem(coll(P),collapse,_).

    elem(expand_all, button, buttons).
    attr(expand_all, label, "Expand all").
    attr(expand_all, class, ("btn-sm";"btn-outline-dark";"m-2")).
    attr(expand_all, icon, ("fa-up-right-and-down-left-from-center")).
    when(expand_all, click, update, (coll(P),collapsed,false)):-elem(coll(P),collapse,_).



elem(coll(P),collapse, w):-root(P).
attr(coll(P),order, 2):-root(P).
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
attr(side,title, "File Manager").
attr(side,position, end).
attr(side,class, ("bg-primary";"bg-opacity-10")).
attr(side,width, "400").

elem(side_container,container, side).

elem(info, label, side_container).
attr(info,label, "Upload ASP instances using predicates skill/1 and parent/2. Then click on the skills to mark them as mastered.").
attr(info,class, ("text-start";"fst-italic")).
attr(info,order, 1).


elem(files_collapse,collapse, side_container).
attr(files_collapse,label, "Available files").
attr(files_collapse,order, 2).
attr(files_collapse,class, ("h6";"mt-5")).
attr(files_collapse,icon, "fa-file").
attr(files_collapse,collapsed, false).


    elem(files,container, files_collapse):-file(F).
    attr(files,class, "ps-5"):-file(F).

        file(F):- _clinguin_optional_file(F).
        elem(file(F),checkbox, files):-_clinguin_optional_file(F).
        attr(file(F),label, F):-_clinguin_optional_file(F).
        attr(file(F),checked, true):-_clinguin_active_file(F).
        when(file(F), click, call, activate_file(F)):-_clinguin_optional_file(F), not _clinguin_active_file(F).
        when(file(F), click, call, deactivate_file(F)):-_clinguin_optional_file(F), _clinguin_active_file(F).


elem(files_upload_multiple,collapse, side_container).
attr(files_upload_multiple,label, "Upload multiple files").
attr(files_upload_multiple,order, 3).
attr(files_upload_multiple,class, ("h6";"mt-5")).
attr(files_upload_multiple,icon, "fa-upload").
attr(files_upload_multiple,collapsed, false).


    elem(fi_multi, file_input, files_upload_multiple).
    attr(fi_multi, accept, ".lp").
    attr(fi_multi, multiple, true).
    attr(fi_multi, order, 1).
    when(fi_multi, change, call, (upload_file)).

elem(files_upload_confirm,collapse, side_container).
attr(files_upload_confirm,label, "Upload file with confirmation").
attr(files_upload_confirm,order, 5).
attr(files_upload_confirm,class, ("h6";"mt-5")).
attr(files_upload_confirm,icon, "fa-upload").
attr(files_upload_confirm,collapsed, false).


    elem(fi_single, file_input, files_upload_confirm).
    attr(fi_single, accept, ".lp").
    attr(fi_single, multiple, false).
    attr(fi_single, order, 1).
    when(fi_single, change, update, (modalAccept, visibility, shown)).



    elem(modalAccept, modal, w).
    attr(modalAccept, title, "Are you sure you want to upload the file?").
    attr(modalAccept, visibility, hidden).

        elem(modalAcceptButton, button, modalAccept).
        attr(modalAcceptButton, label, "Upload and Ground").
        attr(modalAcceptButton, icon, "fa-upload").
        attr(modalAcceptButton, class, "btn-success").
        when(modalAcceptButton, click, call, (upload_file, activate_file(_context_value(filename)))).

    elem(modalAcceptLabel, label, modalAccept).
    attr(modalAcceptLabel, label, "Uploading this file will add it to the control and ground again.").
    attr(modalAcceptLabel, class, ("fst-italic";"p-3")).

elem(files_upload_button,collapse, side_container).
attr(files_upload_button,label, "Upload file automatic activation").
attr(files_upload_button,order, 4).
attr(files_upload_button,class, ("h6";"mt-5")).
attr(files_upload_button,icon, "fa-upload").
attr(files_upload_button,collapsed, false).

    elem(files_content, container, files_upload_button).

    elem(fi_button, file_input, files_content).
    attr(fi_button, accept, ".lp").
    attr(fi_button, multiple, false).
    attr(fi_button, order, 1).
    when(fi_button, change, update, (fi_button_upload, disabled, false)).

    elem(fi_button_upload, button, files_content).
    attr(fi_button_upload, label, "Upload file").
    attr(fi_button_upload, icon, "fa-upload").
    attr(fi_button_upload, class, ("btn-success";"btn-sm";"mt-2")).
    attr(fi_button_upload, order, 2).
    attr(fi_button_upload, disabled, true).
    when(fi_button_upload, click, call, (upload_file, activate_file(_context_value(filename)))).

%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar
%%%%%%%%%%%%%%%%%%%%%%%%
elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Skill manager").
attr(menu_bar, icon, "fa-hand-holding-heart").


    elem(menu_bar_restart, button, menu_bar).
    attr(menu_bar_restart, label, "Restart").
    attr(menu_bar_restart, icon, "fa-arrows-rotate").
    attr(menu_bar_restart, class, "btn-outline-danger").
    attr(menu_bar_restart, class, "border-0").
    when(menu_bar_restart, click, call, restart).
