pos(M,(T1,ST1),1) :- assign(T1,ST1,M), #false: assign(T2,ST2,M), seq((T2,ST2),(T1,ST1),_).
pos(M,(T2,ST2),X+1) :- assign(T1,ST1,M),  assign(T2,ST2,M), seq((T1,ST1),(T2,ST2),_), 
        pos(M,(T1,ST1),X),
        #false :  assign(T3,ST3,M), seq((T1,ST1),(T3,ST3),_), seq((T3,ST3),(T2,ST2),_).  

color(1,"bg-primary").
color(2,"bg-success").
color(3,"bg-warning").


elem(window, window, root).
attr(window, class, ("column-reverse";"justify-content-between")).

    %%%%%%%%%%%%%%%%%%%%%%%%
    % Machine containers
    %%%%%%%%%%%%%%%%%%%%%%%%
    elem(c(M), container, window):- machine(M).
    attr(c(M), class, ("border";"border-dark";"bg-secondary";"rounded";"bg-opacity-25";"m-1";"p-1")):- machine(M).
    attr(c(M), flex_direction, column):- machine(M).
    
        %%%%%%%%%%%%%%%%%%%%%%%%
        % Title
        %%%%%%%%%%%%%%%%%%%%%%%%
        elem(ctitle(M), label, c(M)):- machine(M).
        attr(ctitle(M), label, @concat( "Machine ", M)):- machine(M).
        attr(ctitle(M), class, "fw-bold"):- machine(M).
        attr(ctitle(M), order, 1):- machine(M).

        %%%%%%%%%%%%%%%%%%%%%%%%
        % Tasks per machine
        %%%%%%%%%%%%%%%%%%%%%%%%
        elem(ctasks(M), container, c(M)):- machine(M).
        attr(ctasks(M), order, 2):- machine(M).
        attr(ctasks(M), flex_direction, row):- machine(M).

            task_not_fixed((T,ST)):-  assign(T,ST,M), assign(T2,ST2,M), seq((T2,ST2),(T,ST),_), _any(seq((T,ST),(T2,ST2),_)).
            task_not_fixed((T,ST)):-  assign(T,ST,M), assign(T2,ST2,M), seq((T,ST),(T2,ST2),_), _any(seq((T2,ST2),(T,ST),_)).

            %%%%%%%%%%%%%%%%%%%%%%%%
            % Task
            %%%%%%%%%%%%%%%%%%%%%%%%
            elem(tc(T,ST), container, ctasks(M)):- assign(T,ST,M).
            attr(tc(T,ST), class, C):- assign(T,ST,M), color(T,C).
            attr(tc(T,ST), class, ("bg-opacity-50";"m-1";"justify-content-between";"align-items-start";"p-1")):- assign(T,ST,M).
            attr(tc(T,ST), order, X+1):- assign(T,ST,M), pos(M,(T,ST),X).
            attr(tc(T,ST), class, "opacity-50"):- assign(T,ST,M), task_not_fixed((T,ST)).
            attr(tc(T,ST), width, Time*25):- executionTime(T,ST,Time).
            attr(tc(T,ST), flex_direction, column):- executionTime(T,ST,Time).
            attr(tc(T,ST), class, ("border";"border-dark";"border-2")):- _clinguin_assume(seq((T,ST),_,_)).
                
                %%%%%%%%%%%%%%%%%%%%%%%%
                % Time
                %%%%%%%%%%%%%%%%%%%%%%%%
                elem(tctime(T,ST), label, tc(T,ST)):- _clinguin_assign((T,ST),Start).
                attr(tctime(T,ST), label, @concat("@",Start,"-",Start+ET)):- _clinguin_assign((T,ST),Start), executionTime(T,ST,ET).
                attr(tctime(T,ST), class, "fw-light"):- _clinguin_assign((T,ST),Start).
                attr(tctime(T,ST), fontSize, "8px"):- _clinguin_assign((T,ST),Start).
                
                %%%%%%%%%%%%%%%%%%%%%%%%
                % Label
                %%%%%%%%%%%%%%%%%%%%%%%%
                elem(tctitle(T,ST), label, tc(T,ST)):- assign(T,ST,M).
                attr(tctitle(T,ST), label, (T,ST)):- assign(T,ST,M).
                attr(tctitle(T,ST), class, "fw-bold"):- assign(T,ST,M).

                %%%%%%%%%%%%%%%%%%%%%%%%
                % Button
                %%%%%%%%%%%%%%%%%%%%%%%%
                elem(tcbtn(T,ST), button, tc(T,ST)):- assign(T,ST,M).
                attr(tcbtn(T,ST), class, ("btn-info"; "btn-sm")):- assign(T,ST,M).
                attr(tcbtn(T,ST), icon, "fa-left-long"):- assign(T,ST,M), task_not_fixed((T,ST)).
                attr(tcbtn(T,ST), icon, "fa-ban"):- assign(T,ST,M), not task_not_fixed((T,ST)), _clinguin_assume(seq((T,ST),_,_)).
                attr(tcbtn(T,ST), class, "disabled"):- assign(T,ST,M), not task_not_fixed((T,ST)), not _clinguin_assume(seq((T,ST),_,_)).
                when(tcbtn(T,ST), click, call, add_assumption(seq((T,ST),(T2,ST2),Time))):- task_not_fixed((T,ST)), assign(T,ST,M), assign(T2,ST2,M), executionTime(T,ST,Time), (T,ST)!=(T2,ST2), _any(seq((T,ST),(T2,ST2),_)).
                when(tcbtn(T,ST), click, call, remove_assumption_signature((seq((T,ST),any,any)))):- _clinguin_assume(seq((T,ST),_,_)), assign(T,ST,M).


%%%%%%%%%%%%%%%%%%%%%%%%
% Menu bar
%%%%%%%%%%%%%%%%%%%%%%%%
elem(menu_bar, menu_bar, window).
attr(menu_bar, title, "Job Shop").
attr(menu_bar, icon, "fa-chart-gantt").

    elem(menu_bar_next, button, menu_bar).
    attr(menu_bar_next, label, "Next").
    attr(menu_bar_next, icon, "fa-forward-step").
    when(menu_bar_next, click, callback, next_solution).

    elem(menu_bar_clear, button, menu_bar).
    attr(menu_bar_clear, label, "Clear").
    attr(menu_bar_clear, icon, "fa-trash").
    attr(menu_bar_clear, class, ("btn-outline-danger";"border-0")).
    when(menu_bar_clear, click, callback, clear_assumptions).

    elem(menu_bar_select, button, menu_bar).
    attr(menu_bar_select, label, "Select solution").
    attr(menu_bar_select, icon, "fa-hand-pointer").
    when(menu_bar_select, click, callback, select).