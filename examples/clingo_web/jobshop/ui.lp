pos(M,(T1,ST1),1) :- assign(T1,ST1,M), #false: assign(T2,ST2,M), seq((T2,ST2),(T1,ST1),_).
pos(M,(T2,ST2),X+1) :- assign(T1,ST1,M),  assign(T2,ST2,M), seq((T1,ST1),(T2,ST2),_), 
        pos(M,(T1,ST1),X),
        #false :  assign(T3,ST3,M), seq((T1,ST1),(T3,ST3),_), seq((T3,ST3),(T2,ST2),_).  

color(1,"bg-primary").
color(2,"bg-success").
color(3,"bg-warning").
elem(window, window, root).
attr(window, flex_direction, row).
attr(window, class, ("flex-row-reverse";"justify-content-between")).

    elem(c(M), container, window):- machine(M).
    attr(c(M), class, ("border";"border-dark";"bg-secondary";"rounded";"bg-opacity-25";"m-2";"p-2")):- machine(M).
    attr(c(M), width, 200):- machine(M).
    
        elem(ctitle(M), label, c(M)):- machine(M).
        attr(ctitle(M), label, @concat("", "Machine ", M)):- machine(M).
        attr(ctitle(M), class, "fw-bold"):- machine(M).
        attr(ctitle(M), order, 1):- machine(M).

        elem(ctasks(M), container, c(M)):- machine(M).
        attr(ctasks(M), order, 2):- machine(M).

            elem(tc(T,ST), container, ctasks(M)):- assign(T,ST,M).
            attr(tc(T,ST), class, C):- assign(T,ST,M), color(T,C).
            attr(tc(T,ST), class, ("bg-opacity-50";"border";"mb-1";"justify-content-between";"align-items-start";"p-1")):- assign(T,ST,M).
            attr(tc(T,ST), order, X+1):- assign(T,ST,M), pos(M,(T,ST),X).
            attr(tc(T,ST), class, "opacity-50"):- assign(T,ST,M), not _clinguin_assume(seq((T,ST),_,_)).
            attr(tc(T,ST), height, Time*20):- executionTime(T,ST,Time).
            attr(tc(T,ST), flex_direction, row):- executionTime(T,ST,Time).
                
                elem(tctime(T,ST), label, tc(T,ST)):- _clinguin_assign((T,ST),Start).
                attr(tctime(T,ST), label, @concat("","@",Start,"-",Start+ET)):- _clinguin_assign((T,ST),Start), executionTime(T,ST,ET).
                attr(tctime(T,ST), class, "fw-light"):- _clinguin_assign((T,ST),Start).
                
                elem(tctitle(T,ST), label, tc(T,ST)):- assign(T,ST,M).
                attr(tctitle(T,ST), label, (T,ST)):- assign(T,ST,M).
                attr(tctitle(T,ST), class, "fw-bold"):- assign(T,ST,M).

                elem(tcbtn(T,ST), button, tc(T,ST)):- assign(T,ST,M).
                attr(tcbtn(T,ST), class, "disabled"):- assign(T,ST,M), _clinguin_assume(seq((T,ST),_,_)).
                attr(tcbtn(T,ST), class, "btn-sm"):- assign(T,ST,M).
                attr(tcbtn(T,ST), class, "btn-secondary"):- assign(T,ST,M).
                attr(tcbtn(T,ST), icon, "fa-circle-up"):- assign(T,ST,M).
                when(tcbtn(T,ST), click, call, add_assumption(seq((T,ST),(T2,ST2),Time))):- assign(T,ST,M), assign(T2,ST2,M), executionTime(T,ST,Time), (T,ST)!=(T2,ST2), _b(seq((T,ST),(T2,ST2),_)).

% ---------
% Menu bar
% ---------
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