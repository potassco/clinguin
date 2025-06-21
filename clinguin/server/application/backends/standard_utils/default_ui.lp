% # Window
% -------
elem(w, window, root).
attr(w, class, ("d-flex"; "flex-column")).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% #General attributes
attr(main(S), class, ("d-flex"; "flex-row";"bg-opacity-25";"w-100";"p-2";"rounded";"m-2")):-elem(main(S),container,_).
attr(main(S), class, ("bg-info")):-elem(main(S),container,_),not _clinguin_unsat.
attr(main(S), class, ("bg-danger")):-elem(main(S),container,_), _clinguin_unsat.
attr(section(S), class, ("d-flex"; "flex-column"; "align-items-center";"rounded";"p-2";"m-2";"bg-light";"shadow")):-elem(section(S),container,_).
attr(title(T), class, ("h5";"pb-1")):-elem(title(T),label,_).
attr(title(T), order, 1):-elem(title(T),label,_).
attr(content(C), class, ("d-flex"; "flex-column";"w-100";"p-1";"border-top";"border-bottom")):-elem(content(C),container,_).
attr(content(C), order, 2):-elem(content(C),container,_).
attr(footer(C), class, ("d-flex"; "flex-column";"w-100";"p-1")):-elem(footer(C),container,_).
attr(footer(C), order, 3):-elem(content(C),container,_).
attr(footer_elem(C), class, ("d-flex";"flex-row-reverse")):- elem(footer_elem(C),container,_).
attr(footer_item(C), class, ("m-1";"btn-primary")):- elem(footer_item(C),button,_).
attr(footer_item(C), class, ("m-1")):- elem(footer_item(C),textfield,_).
attr(footer_item(C), class, ("m-1";"btn-outline-dark")):- elem(footer_item(C),dropdown_menu,_).

attr(elem_container(C), class, ("d-flex"; "flex-row"; "align-items-left";"justify-content-between")):-elem(elem_container(C),container,_).
attr(elem_title(C), order, 1):-elem(elem_title(C),_,_).
attr(elem_title(C), class, ("pe-5";"fst-italic")):-elem(elem_title(C),_,_).
attr(elem_title(C), height, "28pt"):-elem(elem_title(C),label,_).
attr(elem_val(C), order, 2):-elem(elem_val(C),_,_).
attr(elem_val(C), class, ("btn-outline";"btn-small";"fw-light")):-elem(elem_val(C),_,_).
attr(elem_val(C), class, ("pe-3";"pt-1";"pb-1")):-elem(elem_val(C),label,_).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




elem(main(state), container, w).
attr(main(state), order, 1).

    % % ## Files
    % % ------------

    % elem(section(files), container, main(state)).

    %     elem(title(files), label, section(files)).
    %     attr(title(files), label, "Files").

    %     elem(content(files), container, section(files)).


    % ## Constants
    % ------------

    elem(section(constants), container, main(state)).

        elem(title(constants), label, section(constants)).
        attr(title(constants), label, "Constants").

        elem(content(constants), container, section(constants)).

            elem(elem_container(const(C)), container, content(constants)):-_clinguin_const(C,V).

                elem(elem_title(const(C)), label, elem_container(const(C))):-_clinguin_const(C,V).
                attr(elem_title(const(C)), label, @format("#const {}",C)):-_clinguin_const(C,V).

                elem(elem_val(const(C)), label, elem_container(const(C))):-_clinguin_const(C,V).
                attr(elem_val(const(C)), label,V):-_clinguin_const(C,V).
                attr(elem_val(const(C)), tooltip,@format("_clinguin_const({},{})",C,V)):-_clinguin_const(C,V).
                % attr(const_label(C), class, "w-100"):-_clinguin_const(C,V).

        elem(footer(constants), container, section(constants)).

            elem(footer_elem(constants), container, footer(constants)).

                elem(footer_item(const(name)),textfield,footer_elem(constants)).
                attr(footer_item(const(name)),placeholder,"name").
                attr(footer_item(const(name)),width,"60pt").
                when(footer_item(const(name)),input,context,(const_name,_value)).

                elem(footer_item(const(val)),textfield,footer_elem(constants)).
                attr(footer_item(const(val)),placeholder,"value").
                attr(footer_item(const(val)),width,"60pt").
                when(footer_item(const(val)),input,context,(const_value,_value)).

                elem(footer_item(const(btn)),button,footer_elem(constants)).
                attr(footer_item(const(btn)),label,"Set constant").
                attr(footer_item(const(btn)),tooltip,"▶︎▶︎ set_constant(_,_)").
                when(footer_item(const(btn)),click,call, set_constant(_context_value(const_name),_context_value(const_value))).


    % #Todo how do we pass the opt properly?


    % ## Optimization
    % -------------
    elem(section(opt), container, main(state)).

        elem(title(opt), label, section(opt)).
        attr(title(opt), label, "Optimization").


        elem(content(opt), container, section(opt)).
        elem(elem_container(opt(cost)), container, content(opt)).
        elem(elem_container(opt(optimizing)), container, content(opt)).
        elem(elem_container(opt(optimal)), container, content(opt)).

            elem(elem_title(opt(cost)), label, elem_container(opt(cost))).
            attr(elem_title(opt(cost)), label, "Cost").

            elem(elem_val(opt(cost)), label, elem_container(opt(cost))).
            attr(elem_val(opt(cost)), icon, "fa-circle-check").
            attr(elem_val(opt(cost)), label, Cost):-_clinguin_cost(Cost).
            attr(elem_val(opt(cost)), tooltip, "_clinguin_cost(_)"):-_clinguin_cost(Cost).



            elem(elem_title(opt(optimal)), label, elem_container(opt(optimal))).
            attr(elem_title(opt(optimal)), label, "Optimal").

            elem(elem_val(opt(optimal)), button, elem_container(opt(optimal))).
            attr(elem_val(opt(optimal)), icon, "fa-circle-check").
            attr(elem_val(opt(optimal)), class, ("disabled";"border-0";"opacity-100")).
            attr(elem_val(opt(optimal)), icon, "fa-circle-check"):-_clinguin_optimal.
            attr(elem_val(opt(optimal)), class, ("text-success")):-_clinguin_optimal.
            attr(elem_val(opt(optimal)), tooltip, "_clinguin_optimal"):-_clinguin_optimal.
            attr(elem_val(opt(optimal)), icon, "fa-circle-xmark"):-not _clinguin_optimal.
            attr(elem_val(opt(optimal)), class, ("text-danger")):-not _clinguin_optimal.
            attr(elem_val(opt(optimal)), tooltip, "not _clinguin_optimal"):-not _clinguin_optimal.

            elem(elem_title(opt(optimizing)), label, elem_container(opt(optimizing))).
            attr(elem_title(opt(optimizing)), label, "Optimizing").

            elem(elem_val(opt(optimizing)), button, elem_container(opt(optimizing))).
            attr(elem_val(opt(optimizing)), class, ("disabled";"border-0";"opacity-100")).
            attr(elem_val(opt(optimizing)), icon, "fa-circle-check"):-_clinguin_optimizing.
            attr(elem_val(opt(optimizing)), class, ("text-success")):-_clinguin_optimizing.
            attr(elem_val(opt(optimizing)), icon, "fa-circle-xmark"):-not _clinguin_optimizing.
            attr(elem_val(opt(optimizing)), class, ("text-danger")):-not _clinguin_optimizing.
            attr(elem_val(opt(optimizing)), tooltip, "_clinguin_optimizing"):-_clinguin_optimizing.
            attr(elem_val(opt(optimizing)), tooltip, "not _clinguin_optimizing"):-not _clinguin_optimizing.

    % ## UNSAT
    % ------------

    elem(section(unsat), container, main(state)):-_clinguin_unsat.

        elem(title(unsat), label, section(unsat)):-_clinguin_unsat.
        attr(title(unsat), label, "UNSAT"):-_clinguin_unsat.
        attr(title(unsat), class, "text-danger"):-_clinguin_unsat.

        elem(content(unsat), container, section(unsat)):-_clinguin_unsat.


        % #Todo add MUS


    % ## SAT
    % ------------

    elem(section(sat), container, main(state)):-not _clinguin_unsat.
    attr(section(sat), class, ("bg-success")):-not _clinguin_unsat.

        elem(title(sat), label, section(sat)):-not _clinguin_unsat.
        attr(title(sat), label, "SAT"):-not _clinguin_unsat.
        attr(title(sat), class, "text-success"):-not _clinguin_unsat.

        elem(content(sat), container, section(sat)):-not _clinguin_unsat.


elem(main(input), container, w).
attr(main(input), order, 2).


    %  ## Input Atoms
    %  ---------------
    elem(section(atoms), container, main(input)).

        elem(title(atoms), label, section(atoms)).
        attr(title(atoms), label, "Added atoms").

        elem(content(atoms), container, section(atoms)).

            elem(elem_container(atom(A)), container, content(atoms)):-_clinguin_atom(A).

                elem(elem_title(atom(A)), label, elem_container(atom(A))):-_clinguin_atom(A).
                attr(elem_title(atom(A)), label, A):-_clinguin_atom(A).
                attr(elem_title(atom(A)), class, "font-monospace"):-_clinguin_atom(A).
                attr(elem_title(atom(A)), tooltip, @format("_clinguin_atom({})",A)):-_clinguin_atom(A).

                elem(elem_val(atom(A)), button, elem_container(atom(A))):-_clinguin_atom(A).
                % attr(elem_val(atom(A)), label, "remove"):-_clinguin_atom(A).
                attr(elem_val(atom(A)), icon, "fa-trash"):-_clinguin_atom(A).
                attr(elem_val(atom(A)), class, ("text-danger")):-_clinguin_atom(A).
                attr(elem_val(atom(A)), tooltip, @format("▶︎▶︎ remove_atom({})",A)):-_clinguin_atom(A).
                when(elem_val(atom(A)), click, call, remove_atom(A)):-_clinguin_atom(A).

        elem(footer(atoms), container, section(atoms)).

            elem(footer_elem(atoms), container, footer(atoms)).

                elem(footer_item(atom(name)),textfield,footer_elem(atoms)).
                attr(footer_item(atom(name)),placeholder,"atom").
                when(footer_item(atom(name)),input,context,(atom_name,_value)).

                elem(footer_item(atom(btn)),button,footer_elem(atoms)).
                attr(footer_item(atom(btn)),label,"Add atom").
                attr(footer_item(atom(btn)),tooltip,"▶︎▶︎ add_atom(_)").
                when(footer_item(atom(btn)),click,call, add_atom(_context_value(atom_name))).

            elem(footer_elem(clear_atoms), container, footer(atoms)).

            elem(footer_item(clear_atoms), button, footer(atoms)).
            attr(footer_item(clear_atoms), label, "Clear").
            attr(footer_item(clear_atoms), class, "btn-danger").
            attr(footer_item(clear_atoms), icon, "fa-trash").
            attr(footer_item(clear_atoms), tooltip, "▶︎▶︎ clear_atoms()").
            when(footer_item(clear_atoms), click, call, clear_atoms).

    %  ## Input Assumptions
    %  ---------------
    elem(section(assumptions), container, main(input)).

        elem(title(assumptions), label, section(assumptions)).
        attr(title(assumptions), label, "Assumptions").

        elem(content(assumptions), container, section(assumptions)).

            elem(elem_container(assumption(A)), container, content(assumptions)):-_clinguin_assume(A,V).

                elem(elem_title(assumption(A)), label, elem_container(assumption(A))):-_clinguin_assume(A,V).
                attr(elem_title(assumption(A)), label, A):-_clinguin_assume(A,V).
                attr(elem_title(assumption(A)), class, "text-success"):-_clinguin_assume(A,true).
                attr(elem_title(assumption(A)), class, "text-danger"):-_clinguin_assume(A,false).
                attr(elem_title(assumption(A)), class, "font-monospace"):-_clinguin_assume(A,V).
                attr(elem_title(assumption(A)), tooltip, @format("_clinguin_assume({},{})",A,V)):-_clinguin_assume(A,V).

                elem(elem_val(assumption(A)), button, elem_container(assumption(A))):-_clinguin_assume(A,V).
                % attr(elem_val(assumption(A)), label, "remove"):-_clinguin_assume(A,V).
                attr(elem_val(assumption(A)), icon, "fa-trash"):-_clinguin_assume(A,V).
                attr(elem_val(assumption(A)), class, ("text-danger")):-_clinguin_assume(A,V).
                attr(elem_val(assumption(A)), tooltip, @format("▶︎▶︎ remove_assumption({})",A)):-_clinguin_assume(A,V).
                when(elem_val(assumption(A)), click, call, remove_assumption(A)):-_clinguin_assume(A,V).

        elem(footer(assumptions), container, section(assumptions)).

            elem(footer_elem(assumptions), container, footer(assumptions)).

                elem(footer_item(assumption(name)),textfield,footer_elem(assumptions)).
                attr(footer_item(assumption(name)),order,3).
                attr(footer_item(assumption(name)),placeholder,"atom").
                when(footer_item(assumption(name)),input,context,(assumption_name,_value)).

                elem(footer_item(assumption(val)),dropdown_menu,footer_elem(assumptions)).
                attr(footer_item(assumption(val)),order,2).


                    elem(footer_item(assumption(val,true)),dropdown_menu_item,footer_item(assumption(val))).
                    attr(footer_item(assumption(val,true)),label,true).
                    attr(footer_item(assumption(val,true)),class,"text-success").
                    when(footer_item(assumption(val,true)),click,context,(assumption_val,true)).
                    when(footer_item(assumption(val,true)),click, update,(footer_item(assumption(val)),selected,true)).
                    when(footer_item(assumption(val,true)),click, update,(footer_item(assumption(val)),class,"text-success")).

                    elem(footer_item(assumption(val,false)),dropdown_menu_item,footer_item(assumption(val))).
                    attr(footer_item(assumption(val,false)),class,"text-danger").
                    attr(footer_item(assumption(val,false)),label,false).
                    when(footer_item(assumption(val,false)),click,context,(assumption_val,false)).
                    when(footer_item(assumption(val,false)),click, update,(footer_item(assumption(val)),selected,false)).
                    when(footer_item(assumption(val,false)),click, update,(footer_item(assumption(val)),class,"text-danger")).

                elem(footer_item(assumption(btn)),button,footer_elem(assumptions)).
                attr(footer_item(assumption(btn)),order,1).
                attr(footer_item(assumption(btn)),label,"Add assumption").
                attr(footer_item(assumption(btn)),tooltip,"▶︎▶︎ add_assumption(_,_)").
                when(footer_item(assumption(btn)),click,call, add_assumption(_context_value(assumption_name,const),_context_value(assumption_val))).

            elem(footer_elem(clear_assumptions), container, footer(assumptions)).

            elem(footer_item(clear_assumptions), button, footer(assumptions)).
            attr(footer_item(clear_assumptions), label, "Clear").
            attr(footer_item(clear_assumptions), class, "btn-danger").
            attr(footer_item(clear_assumptions), icon, "fa-trash").
            attr(footer_item(clear_assumptions), tooltip, "▶︎▶︎ clear_assumptions()").
            when(footer_item(clear_assumptions), click, call, clear_assumptions).


    %  ## Input Externals
    %  ---------------
    elem(section(externals), container, main(input)).

        elem(title(externals), label, section(externals)).
        attr(title(externals), label, "Externals").

        elem(content(externals), container, section(externals)).

            elem(elem_container(external(A)), container, content(externals)):-_clinguin_external(A,V).

                elem(elem_title(external(A)), label, elem_container(external(A))):-_clinguin_external(A,V).
                attr(elem_title(external(A)), label, A):-_clinguin_external(A,V).
                % attr(elem_title(external(A)), class, "text-success"):-_clinguin_external(A,true).
                % attr(elem_title(external(A)), class, "text-danger"):-_clinguin_external(A,false).
                attr(elem_title(external(A)), class, "font-monospace"):-_clinguin_external(A,V).
                attr(elem_title(external(A)), tooltip, @format("_clinguin_external({},{})",A,V)):-_clinguin_external(A,V).

                elem(elem_val(external(A)), dropdown_menu, elem_container(external(A))):-_clinguin_external(A,V).
                attr(elem_val(external(A)), selected, V):-_clinguin_external(A,V).
                attr(elem_val(external(A)), class, "text-success"):-_clinguin_external(A,true).
                attr(elem_val(external(A)), class, "text-danger"):-_clinguin_external(A,false).
                % attr(elem_val(external(A)), label, "remove"):-_clinguin_external(A,V).
                % attr(elem_val(external(A)), icon, "fa-trash"):-_clinguin_external(A,V).
                % attr(elem_val(external(A)), class, ("text-danger")):-_clinguin_external(A,V).
                % attr(elem_val(external(A)), tooltip, @format("▶︎▶︎ remove_external({})",A)):-_clinguin_external(A,V).
                % when(elem_val(external(A)), click, call, remove_external(A)):-_clinguin_external(A,V).

                    elem(elem_val(external(A),true), dropdown_menu_item, elem_val(external(A))):-_clinguin_external(A,V).
                    attr(elem_val(external(A),true), label, "true"):-_clinguin_external(A,V).
                    attr(elem_val(external(A),true), class, "text-success"):-_clinguin_external(A,V).
                    when(elem_val(external(A),true), click, call, set_external(A,true)):-_clinguin_external(A,V).

                    elem(elem_val(external(A),false), dropdown_menu_item, elem_val(external(A))):-_clinguin_external(A,V).
                    attr(elem_val(external(A),false), label, "false"):-_clinguin_external(A,V).
                    attr(elem_val(external(A),false), class, "text-danger"):-_clinguin_external(A,V).
                    when(elem_val(external(A),false), click, call, set_external(A,false)):-_clinguin_external(A,V).

                    elem(elem_val(external(A),release), dropdown_menu_item, elem_val(external(A))):-_clinguin_external(A,V).
                    attr(elem_val(external(A),release), label, "release"):-_clinguin_external(A,V).
                    when(elem_val(external(A),release), click, call, set_external(A,release)):-_clinguin_external(A,V).


elem(main(model), container, w).
attr(main(model), order, 3).

    %  ## Model
    %  ---------------
    elem(section(model), container, main(model)).
    attr(section(model), order, 1):-_clinguin_browsing.
    attr(section(model), class, "bg-primary"):-_clinguin_browsing.

        elem(title(model), label, section(model)).
            attr(title(model), label, "Current model").

            elem(content(model), container, section(model)).

                elem(elem_container(model(A)), container, content(model)):-_clinguin_model(A).

                    elem(elem_title(model(A)), label, elem_container(model(A))):-_clinguin_model(A).
                    % attr(elem_title(model(A)), label, A):-_clinguin_model(A).
                    attr(elem_title(model(A)), label, A):-_clinguin_model(A).
                    attr(elem_title(model(A)), class, "font-monospace"):-_clinguin_model(A).
                    attr(elem_title(model(A)), tooltip, A):-_clinguin_model(A).
                    attr(elem_title(model(A)), class, "opacity-25"):- _all(A), _clinguin_model(A).
                    attr(elem_title(model(A)), class, "text-primary"):-  _clinguin_model(A), _clinguin_browsing.

            elem(footer(model), container, section(model)).



            elem(footer_elem(select), container, footer(model)).
            attr(footer_elem(select), order, 2).

                elem(footer_item(select(select_show)),textfield,footer_elem(select)).
                attr(footer_item(select(select_show)),order,1).
                attr(footer_item(select(select_show)),width,"315pt").
                attr(footer_item(select(select_show)),placeholder,"Optional #show").
                when(footer_item(select(select_show)),input,context,(select_show,_value)).

                elem(footer_item(select(btn)),button,footer_elem(select)).
                attr(footer_item(select(btn)),order,2).
                attr(footer_item(select(btn)),label,"Select solution").
                attr(footer_item(select(btn)),icon,"fa-hand-pointer").
                attr(footer_item(select(btn)),class,"btn-success").
                attr(footer_item(select(btn)),tooltip,"▶︎▶︎ select").
                when(footer_item(select(btn)),click,call, select(_context_value(select_show,str," "))).


            elem(footer_elem(download), container, footer(model)).
            attr(footer_elem(download), order, 3).

                elem(footer_item(download(download_show)),textfield,footer_elem(download)).
                attr(footer_item(download(download_show)),order,2).
                attr(footer_item(download(download_show)),placeholder,"Optional #show").
                when(footer_item(download(download_show)),input,context,(download_show,_value)).

                elem(footer_item(download(download_name)),textfield,footer_elem(download)).
                attr(footer_item(download(download_name)),order,1).
                attr(footer_item(download(download_name)),placeholder,"File name").
                when(footer_item(download(download_name)),input,context,(download_name,_value)).

                elem(footer_item(download(btn)),button,footer_elem(download)).
                attr(footer_item(download(btn)),order,3).
                attr(footer_item(download(btn)),label,"Download solution").
                attr(footer_item(download(btn)),icon,"fa-download").
                attr(footer_item(download(btn)),class,"btn-success").
                attr(footer_item(download(btn)),tooltip,"▶︎▶︎ download").
                when(footer_item(download(btn)),click,call, download(_context_value(download_show,str," "),_context_value(download_name,str,"file.lp"))).


            elem(footer_elem(browse), container, footer(model)).
            attr(footer_elem(browse), order, 1).

                elem(footer_item(next_solution), button, footer_elem(browse)).
                attr(footer_item(next_solution), order, 3).
                attr(footer_item(next_solution), label, "Next").
                attr(footer_item(next_solution), icon, "fa-forward-step").
                attr(footer_item(next_solution), tooltip, "▶︎▶︎ next_solution()").
                when(footer_item(next_solution), click, call, next_solution).

                elem(footer_item(next_solution_opt), button, footer_elem(browse)).
                attr(footer_item(next_solution_opt), order, 2).
                attr(footer_item(next_solution_opt), label, "Next Optimizing").
                attr(footer_item(next_solution_opt), icon, "fa-forward-fast").
                attr(footer_item(next_solution_opt), tooltip, "▶︎▶︎ next_solution(optN)").
                when(footer_item(next_solution_opt), click, call, next_solution(optN)).

                elem(footer_item(stop), button, footer_elem(browse)).
                attr(footer_item(stop), order, 1).
                attr(footer_item(stop), label, "Stop Browsing").
                attr(footer_item(stop), class, "btn-danger").
                attr(footer_item(stop), class, "disabled"):-not _clinguin_browsing.
                attr(footer_item(stop), icon, "fa-stop").
                attr(footer_item(stop), tooltip, "▶︎▶︎ stop_browsing"):-_clinguin_browsing.
                attr(footer_item(stop), tooltip, "not _clinguin_browsing"):-not _clinguin_browsing.
                when(footer_item(stop), click, call, stop_browsing).

    elem(section(brave), container, main(model)).
    attr(section(brave), order, 2).

        elem(title(brave), label, section(brave)).
            attr(title(brave), label, "In Some Model (Brave)").

            elem(content(brave), container, section(brave)).

                elem(elem_container(brave(A)), container, content(brave)):-_any(A).

                    elem(elem_title(brave(A)), label, elem_container(brave(A))):-_any(A).
                    % attr(elem_title(brave(A)), label, A):-_any(A).
                    attr(elem_title(brave(A)), label, A):-_any(A).
                    attr(elem_title(brave(A)), class, "font-monospace"):-_any(A).
                    attr(elem_title(brave(A)), class, "opacity-25"):-_any(A), _all(A).

                    attr(elem_title(brave(A)), tooltip, @format("_any({})",A)):-_any(A).
                    attr(elem_title(brave(A)), class, "text-primary"):-_any_opt(A).
                    attr(elem_title(brave(A)), class, "fw-bold"):-_all_opt(A).


                    elem(elem_val(brave(A)), dropdown_menu, elem_container(brave(A))):-_any(A).
                    attr(elem_val(brave(A)), icon, "fa-plus"):-_any(A).
                    attr(elem_val(brave(A)), tooltip, @format("▶︎▶︎ add_assumption({},_)",A)):-_any(A).

                        elem(elem_val_true(brave(A)), dropdown_menu_item, elem_val(brave(A))):-_any(A).
                        attr(elem_val_true(brave(A)), label, true):-_any(A).
                        attr(elem_val_true(brave(A)), class, "text-success"):-_any(A).
                        when(elem_val_true(brave(A)), click, call, add_assumption(A,true)):-_any(A).

                        elem(elem_val_false(brave(A)), dropdown_menu_item, elem_val(brave(A))):-_any(A).
                        attr(elem_val_false(brave(A)), label, false):-_any(A).
                        attr(elem_val_false(brave(A)), class, "text-danger"):-_any(A).
                        when(elem_val_false(brave(A)), click, call, add_assumption(A,false)):-_any(A).


                    % elem(elem_val(brave(A)), button, elem_container(brave(A))):-_any(A), not _all(A).
                    % attr(elem_val(brave(A)), icon, "fa-plus"):-_any(A), not _all(A).
                    % attr(elem_val(brave(A)), class, ("text-primary")):-_any(A), not _all(A).
                    % attr(elem_val(brave(A)), tooltip, @format("▶︎▶︎ add_assumption({},true)",A)):-_any(A), not _all(A).
                    % when(elem_val(brave(A)), click, call, add_assumption(A,true)):-_any(A), not _all(A).





    elem(section(cautious), container, main(model)).
    attr(section(cautious), order, 3).

        elem(title(cautious), label, section(cautious)).
            attr(title(cautious), label, "In All Models (Cautious)").

            elem(content(cautious), container, section(cautious)).

                elem(elem_container(cautious(A)), container, content(cautious)):-_all(A).

                    elem(elem_title(cautious(A)), label, elem_container(cautious(A))):-_all(A).
                    % attr(elem_title(cautious(A)), label, A):-_all(A).
                    attr(elem_title(cautious(A)), label, A):-_all(A).
                    attr(elem_title(cautious(A)), class, "font-monospace"):-_all(A).
                    attr(elem_title(cautious(A)), tooltip, @format("_all({})",A)):-_all(A).


% # Menu bar
% -----------
    elem(menu_bar, menu_bar, w).
    attr(menu_bar, title, "Clinguin").
    attr(menu_bar, icon, "fa-desktop").

        elem(menu_bar_restart, button, menu_bar).
        attr(menu_bar_restart, label, "Restart").
        attr(menu_bar_restart, icon, "fa-arrows-rotate").
        attr(menu_bar_restart, class, "btn-outline-danger").
        attr(menu_bar_restart, class, "border-0").
        when(menu_bar_restart, click, call, restart).
