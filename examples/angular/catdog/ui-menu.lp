elem(menu_bar, menu_bar, w).
attr(menu_bar, title, "Table placement").
attr(menu_bar, icon, "fa-utensils").

elem(menu_bar_next, button, menu_bar).
attr(menu_bar_next, label, "Next").
attr(menu_bar_next, icon, "fa-forward-step").
when(menu_bar_next, click, call, next_solution).

attr(seat_dd(S), selected, P):- assign(P,S), _clinguin_browsing.
attr(seat_dd(S), class, "text-success"):- _clinguin_browsing,
                        assign(P,S), not _all(assign(P,S)).
attr(seat_dd(S), class, "opacity-75"):- _all(assign(P,S)),
                        not _clinguin_assume(assign(P,S),true).



%------------------------------
% Extension from the paper
% -----------------------------


% Download action for instance (We can remove it and just comment that can be used)
elem(menu_bar_download, button, menu_bar).
attr(menu_bar_download, label, "Download instance").
attr(menu_bar_download, icon, "fa-download").
when(menu_bar_download, click, call, (download("#show person/2.","listings/dl_instance.lp"))).

% Download action for solution and multiple actions for call
elem(menu_bar_download_solution, button, menu_bar).
attr(menu_bar_download_solution, label, "Download solution").
attr(menu_bar_download_solution, icon, "fa-download").
when(menu_bar_download_solution, click, call, download("#show assign/2.","listings/dl_solution.lp")).
