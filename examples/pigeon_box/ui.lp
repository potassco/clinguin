% TODO: test how css generation works with include statements inside this file


% ── DERIVED FACTS ────────────────────────────
shown_assignment(P,B) :- _all(in(P,B)).
shown_assignment(P,B) :- in(P,B), _clinguin_browsing.
has_assignment(P)     :- shown_assignment(P,_).
available(B,P)        :- box(B), pigeon(P), _any(in(P,B)), not _all(in(P,B)).
assumed(P,B)          :- _clinguin_assume(in(P,B), true).
locked_pigeon(P)      :- assumed(P,_).

n_locked(N)     :- N = #count { P : locked_pigeon(P) }.
n_pigeons(N)    :- N = #count { P : pigeon(P) }.
n_boxes_used(N) :- N = #count { B : shown_assignment(_, B) }.
n_boxes(N)      :- N = #count { B : box(B) }.

all_locked :- n_locked(N), n_pigeons(N), N > 0.

title_option("Pigeonhole Assignment").
title_option("Box Filler").
title_option("Example").


% ── ROOT ─────────────────────────────────────
elem(w, window, root).
attr(w, class, ("min-h-screen"; "flex"; "flex-col"; "bg-muted")).


% ── HEADER ───────────────────────────────────
elem(header, container, w).
attr(header, class, ("flex"; "items-center"; "justify-between"; "px-6"; "py-4"; "bg-card"; "border-b"; "shadow-sm")).
attr(header, style, "order: 1").

elem(header_left, container, header).
attr(header_left, class, ("flex"; "items-center"; "gap-3")).
attr(header_left, order, 1).
    elem(title_icon, icon, header_left).
    attr(title_icon, icon, "Bird").
    attr(title_icon, order, 1).
    elem(title, text, header_left).
    attr(title, text, "Pigeonhole Assignment").
    attr(title, class, ("text-xl"; "font-bold"; "text-primary")).
    attr(title, order, 2).

elem(header_right, container, header).
attr(header_right, class, ("flex"; "items-center"; "gap-3")).
attr(header_right, order, 2).

    elem(tools_menu, dropdown_menu, header_right).
    attr(tools_menu, label, "Tools").
    attr(tools_menu, class, ("border"; "rounded-md"; "px-3"; "py-2"; "text-sm"; "font-medium")).
    attr(tools_menu, order, 1).

        elem(tools_content, dropdown_menu_content, tools_menu).
        attr(tools_content, class, "w-56").

        elem(title_sub, dropdown_menu, tools_content).
        attr(title_sub, label, "Rename title").
        attr(title_sub, order, 1).
            elem(title_sub_content, dropdown_menu_content, title_sub).
                elem(title_group_menu, dropdown_menu_radio_group, title_sub_content).
                attr(title_group_menu, value, "Pigeonhole Assignment").
                    elem(title_opt(P), dropdown_menu_radio_item, title_group_menu) :- title_option(P).
                    attr(title_opt(P), label, P) :- title_option(P).
                    attr(title_opt(P), value, P) :- title_option(P).
                    when(title_opt(P), click, update, (title_group_menu, value, P)) :- title_option(P).
                    when(title_opt(P), click, update, (title, text, P)) :- title_option(P).

        elem(danger_group, dropdown_menu_group, tools_content).
        attr(danger_group, label, "Clear").
        attr(danger_group, order, 2).
            elem(clear_item, dropdown_menu_item, danger_group).
            attr(clear_item, label, "Clear assumptions").
            attr(clear_item, variant, "destructive").
            attr(clear_item, order, 1).
            when(clear_item, click, call, clear_assumptions).
                elem(clear_icon, icon, clear_item).
                attr(clear_icon, icon, "Eraser").
            elem(restart_item, dropdown_menu_item, danger_group).
            attr(restart_item, label, "Restart").
            attr(restart_item, variant, "destructive").
            attr(restart_item, order, 2).
            when(restart_item, click, call, restart).
                elem(restart_icon, icon, restart_item).
                attr(restart_icon, icon, "RotateCcw").

    elem(toggle, theme_toggle, header_right).
    attr(toggle, order, 2).
    attr(toggle, icon_dark, "Sun").
    attr(toggle, icon_light, "Moon").
    attr(toggle, variant, "outline").
    attr(toggle, class, ("p-2"; "rounded-full")).


% ── STATS BAR ────────────────────────────────
elem(stats_bar, container, w).
attr(stats_bar, class, ("flex"; "items-center"; "gap-3"; "px-6"; "py-3"; "bg-card"; "border-b")).
attr(stats_bar, style, "order: 2").

elem(stat_locked, container, stats_bar).
attr(stat_locked, class, ("flex"; "items-center"; "gap-3"; "px-4"; "py-2"; "bg-muted"; "rounded-lg"; "min-w-32")).
attr(stat_locked, order, 1).
    elem(stat_locked_icon, icon, stat_locked).
    attr(stat_locked_icon, icon, "Lock").
    attr(stat_locked_icon, order, 1).
    elem(stat_locked_info, container, stat_locked).
    attr(stat_locked_info, class, ("flex"; "flex-col")).
    attr(stat_locked_info, order, 2).
        elem(stat_locked_val, text, stat_locked_info).
        attr(stat_locked_val, text, N) :- n_locked(N).
        attr(stat_locked_val, class, ("text-2xl"; "font-bold"; "leading-none")).
        attr(stat_locked_val, order, 1).
        elem(stat_locked_lbl, text, stat_locked_info).
        attr(stat_locked_lbl, text, "Locked").
        attr(stat_locked_lbl, class, ("text-xs"; "text-muted-foreground"; "mt-0.5")).
        attr(stat_locked_lbl, order, 2).

elem(stat_total, container, stats_bar).
attr(stat_total, class, ("flex"; "items-center"; "gap-3"; "px-4"; "py-2"; "bg-muted"; "rounded-lg"; "min-w-32")).
attr(stat_total, order, 2).
    elem(stat_total_icon, icon, stat_total).
    attr(stat_total_icon, icon, "Bird").
    attr(stat_total_icon, order, 1).
    elem(stat_total_info, container, stat_total).
    attr(stat_total_info, class, ("flex"; "flex-col")).
    attr(stat_total_info, order, 2).
        elem(stat_total_val, text, stat_total_info).
        attr(stat_total_val, text, N) :- n_pigeons(N).
        attr(stat_total_val, class, ("text-2xl"; "font-bold"; "leading-none")).
        attr(stat_total_val, order, 1).
        elem(stat_total_lbl, text, stat_total_info).
        attr(stat_total_lbl, text, "Pigeons").
        attr(stat_total_lbl, class, ("text-xs"; "text-muted-foreground"; "mt-0.5")).
        attr(stat_total_lbl, order, 2).

elem(stat_boxes, container, stats_bar).
attr(stat_boxes, class, ("flex"; "items-center"; "gap-3"; "px-4"; "py-2"; "bg-muted"; "rounded-lg"; "min-w-32")).
attr(stat_boxes, order, 3).
    elem(stat_boxes_icon, icon, stat_boxes).
    attr(stat_boxes_icon, icon, "Package").
    attr(stat_boxes_icon, order, 1).
    elem(stat_boxes_info, container, stat_boxes).
    attr(stat_boxes_info, class, ("flex"; "flex-col")).
    attr(stat_boxes_info, order, 2).
        elem(stat_boxes_val, text, stat_boxes_info).
        attr(stat_boxes_val, text, @concat(N, @concat("/", M))) :- n_boxes_used(N), n_boxes(M).
        attr(stat_boxes_val, class, ("text-2xl"; "font-bold"; "leading-none")).
        attr(stat_boxes_val, order, 1).
        elem(stat_boxes_lbl, text, stat_boxes_info).
        attr(stat_boxes_lbl, text, "Boxes used").
        attr(stat_boxes_lbl, class, ("text-xs"; "text-muted-foreground"; "mt-0.5")).
        attr(stat_boxes_lbl, order, 2).

elem(stat_mode, container, stats_bar).
attr(stat_mode, class, ("flex"; "items-center"; "gap-3"; "px-4"; "py-2"; "bg-muted"; "rounded-lg"; "min-w-32")).
attr(stat_mode, order, 4).
    elem(stat_mode_icon, icon, stat_mode).
    attr(stat_mode_icon, icon, "Eye")    :- _clinguin_browsing.
    attr(stat_mode_icon, icon, "EyeOff") :- not _clinguin_browsing.
    attr(stat_mode_icon, order, 1).
    elem(stat_mode_info, container, stat_mode).
    attr(stat_mode_info, class, ("flex"; "flex-col")).
    attr(stat_mode_info, order, 2).
        elem(stat_mode_val, text, stat_mode_info).
        attr(stat_mode_val, text, "Browsing") :- _clinguin_browsing.
        attr(stat_mode_val, text, "Idle")     :- not _clinguin_browsing.
        attr(stat_mode_val, class, ("text-2xl"; "font-bold"; "leading-none")).
        attr(stat_mode_val, order, 1).
        elem(stat_mode_lbl, text, stat_mode_info).
        attr(stat_mode_lbl, text, "Mode").
        attr(stat_mode_lbl, class, ("text-xs"; "text-muted-foreground"; "mt-0.5")).
        attr(stat_mode_lbl, order, 2).


% ── MAIN ─────────────────────────────────────
elem(main, container, w).
attr(main, class, ("flex"; "flex-row"; "gap-6"; "p-6"; "grow"; "items-start")).
attr(main, style, "order: 3").

% ── LEFT: Box card grid ───────────────────────
elem(box_grid, container, main).
attr(box_grid, class, ("flex"; "flex-row"; "flex-wrap"; "gap-4"; "flex-1")).
attr(box_grid, order, 1).

elem(box_card(B), container, box_grid) :- box(B).
attr(box_card(B), class, ("flex"; "flex-col"; "gap-2"; "p-3"; "bg-card"; "border"; "rounded-lg"; "shadow-sm"; "w-44")) :- box(B).
attr(box_card(B), order, B) :- box(B).

    elem(box_header(B), container, box_card(B)) :- box(B).
    attr(box_header(B), class, ("flex"; "items-center"; "justify-between"; "gap-2")) :- box(B).

        elem(box_title(B), container, box_header(B)) :- box(B).
        attr(box_title(B), class, ("flex"; "items-center"; "gap-2")) :- box(B).
            elem(box_icon(B), icon, box_title(B)) :- box(B).
            attr(box_icon(B), icon, "Package") :- box(B).
            elem(box_label(B), text, box_title(B)) :- box(B).
            attr(box_label(B), text, @concat("Box ", B)) :- box(B).
            attr(box_label(B), class, ("text-sm"; "font-semibold")) :- box(B).

        elem(box_dd(B), dropdown_menu, box_header(B)) :- box(B).
        attr(box_dd(B), label, "+") :- box(B).
        attr(box_dd(B), class, ("h-7"; "w-7"; "p-0"; "text-sm"; "rounded-full"; "border")) :- box(B).
            elem(box_dd_content(B), dropdown_menu_content, box_dd(B)) :- box(B).
            attr(box_dd_content(B), class, "w-48") :- box(B).
            elem(box_dd_group(B), dropdown_menu_group, box_dd_content(B)) :- box(B).
            attr(box_dd_group(B), label, "Assign pigeon") :- box(B).
                elem(box_ddi(B,P), dropdown_menu_item, box_dd_group(B)) :- available(B,P).
                attr(box_ddi(B,P), label, @concat("Pigeon ", P)) :- available(B,P).
                attr(box_ddi(B,P), order, P) :- available(B,P).
                when(box_ddi(B,P), click, call, add_assumption(in(P,B),true)) :- available(B,P).
                    elem(box_ddi_icon(B,P), icon, box_ddi(B,P)) :- available(B,P).
                    attr(box_ddi_icon(B,P), icon, "Plus") :- available(B,P).

    elem(box_pigeons(B), container, box_card(B)) :- box(B).
    attr(box_pigeons(B), class, ("flex"; "flex-col"; "gap-1"; "min-h-6")) :- box(B).

        elem(chip(B,P), container, box_pigeons(B)) :- shown_assignment(P,B).
        attr(chip(B,P), class, ("flex"; "items-center"; "justify-between"; "gap-1"; "px-2"; "py-1"; "rounded"; "text-xs"; "transition-colors")) :- shown_assignment(P,B).
        attr(chip(B,P), class, ("bg-primary"; "text-primary-foreground")) :- shown_assignment(P,B), locked_pigeon(P).
        attr(chip(B,P), class, ("bg-accent";  "text-accent-foreground"))  :- shown_assignment(P,B), not locked_pigeon(P).

        attr(chip(B,P), class, ("group"; "cursor-pointer"; "hover:bg-destructive"; "hover:text-destructive-foreground")) :- assumed(P,B).
        when(chip(B,P), click, call, remove_assumption(in(P,B))) :- assumed(P,B).

            elem(chip_label(B,P), text, chip(B,P)) :- shown_assignment(P,B).
            attr(chip_label(B,P), text, @concat("Pigeon ", P)) :- shown_assignment(P,B).
            attr(chip_label(B,P), order, 1) :- shown_assignment(P,B).

            elem(chip_icon_hover(B,P), icon, chip(B,P)) :- assumed(P,B).
            attr(chip_icon_hover(B,P), icon, "X") :- assumed(P,B).
            attr(chip_icon_hover(B,P), class, ("hidden"; "group-hover:inline-block")) :- assumed(P,B).
            attr(chip_icon_hover(B,P), order, 2) :- assumed(P,B).


% ── RIGHT: Pigeon roster table ────────────────
elem(roster, container, main).
attr(roster, class, ("flex"; "flex-col"; "bg-card"; "border"; "rounded-lg"; "shadow-sm"; "overflow-hidden"; "min-w-72")).
attr(roster, order, 2).

    elem(roster_title_row, container, roster).
    attr(roster_title_row, class, ("flex"; "items-center"; "gap-2"; "px-4"; "py-3"; "border-b"; "bg-muted/50")).
    attr(roster_title_row, order, 1).
        elem(roster_title_icon, icon, roster_title_row).
        attr(roster_title_icon, icon, "ClipboardList").
        elem(roster_title_text, text, roster_title_row).
        attr(roster_title_text, text, "Pigeon Roster").
        attr(roster_title_text, class, ("text-sm"; "font-semibold")).

    elem(roster_head, container, roster).
    attr(roster_head, class, ("flex"; "items-center"; "px-4"; "py-2"; "text-xs"; "font-semibold"; "uppercase"; "tracking-wider"; "text-muted-foreground"; "border-b")).
    attr(roster_head, order, 2).
        elem(rh_pigeon, text, roster_head).
        attr(rh_pigeon, text, "Pigeon").
        attr(rh_pigeon, class, "flex-1").
        attr(rh_pigeon, order, 1).
        elem(rh_box, text, roster_head).
        attr(rh_box, text, "Box").
        attr(rh_box, class, "flex-1").
        attr(rh_box, order, 2).
        elem(rh_status, text, roster_head).
        attr(rh_status, text, "Status").
        attr(rh_status, class, "w-24").
        attr(rh_status, order, 3).

    elem(roster_body, container, roster).
    attr(roster_body, class, ("flex"; "flex-col")).
    attr(roster_body, order, 3).

    elem(roster_row(P), container, roster_body) :- pigeon(P).
    attr(roster_row(P), class, ("flex"; "items-center"; "px-4"; "py-2"; "border-b"; "text-sm"; "gap-3")) :- pigeon(P).
    attr(roster_row(P), order, P) :- pigeon(P).

        elem(rr_pigeon(P), container, roster_row(P)) :- pigeon(P).
        attr(rr_pigeon(P), class, ("flex"; "items-center"; "gap-2"; "flex-1")) :- pigeon(P).
        attr(rr_pigeon(P), order, 1) :- pigeon(P).
            elem(rr_pigeon_icon(P), icon, rr_pigeon(P)) :- pigeon(P).
            attr(rr_pigeon_icon(P), icon, "Bird") :- pigeon(P).
            elem(rr_pigeon_name(P), text, rr_pigeon(P)) :- pigeon(P).
            attr(rr_pigeon_name(P), text, @concat("Pigeon ", P)) :- pigeon(P).
            attr(rr_pigeon_name(P), class, "font-medium") :- pigeon(P).

        elem(rr_box(P), container, roster_row(P)) :- pigeon(P).
        attr(rr_box(P), class, "flex-1") :- pigeon(P).
        attr(rr_box(P), order, 2) :- pigeon(P).
            elem(rr_box_val(P), text, rr_box(P)) :- shown_assignment(P,B).
            attr(rr_box_val(P), text, @concat("Box ", B)) :- shown_assignment(P,B).
            attr(rr_box_val(P), class, "font-medium") :- shown_assignment(P,B).
            elem(rr_box_empty(P), text, rr_box(P)) :- pigeon(P), not has_assignment(P).
            attr(rr_box_empty(P), text, "—") :- pigeon(P), not has_assignment(P).
            attr(rr_box_empty(P), class, "text-muted-foreground") :- pigeon(P), not has_assignment(P).

        elem(rr_status(P), container, roster_row(P)) :- pigeon(P).
        attr(rr_status(P), class, "w-24") :- pigeon(P).
        attr(rr_status(P), order, 3) :- pigeon(P).
            elem(rr_badge_locked(P), text, rr_status(P)) :- locked_pigeon(P).
            attr(rr_badge_locked(P), text, "Locked") :- locked_pigeon(P).
            attr(rr_badge_locked(P), class, ("px-2"; "py-0.5"; "bg-green-100"; "text-green-800"; "dark:bg-green-900"; "dark:text-green-200"; "rounded-full"; "text-xs"; "font-medium")) :- locked_pigeon(P).
            elem(rr_badge_suggested(P), text, rr_status(P)) :- has_assignment(P), not locked_pigeon(P).
            attr(rr_badge_suggested(P), text, "Suggested") :- has_assignment(P), not locked_pigeon(P).
            attr(rr_badge_suggested(P), class, ("px-2"; "py-0.5"; "bg-blue-100"; "text-blue-800"; "dark:bg-blue-900"; "dark:text-blue-200"; "rounded-full"; "text-xs"; "font-medium")) :- has_assignment(P), not locked_pigeon(P).
            elem(rr_badge_free(P), text, rr_status(P)) :- pigeon(P), not has_assignment(P).
            attr(rr_badge_free(P), text, "Free") :- pigeon(P), not has_assignment(P).
            attr(rr_badge_free(P), class, ("px-2"; "py-0.5"; "bg-muted"; "text-muted-foreground"; "rounded-full"; "text-xs")) :- pigeon(P), not has_assignment(P).


% ── FOOTER ───────────────────────────────────
elem(footer, container, w).
attr(footer, class, ("flex"; "items-center"; "justify-between"; "px-6"; "py-4"; "bg-card"; "border-t")).
attr(footer, style, "order: 4").

elem(footer_left, container, footer).
attr(footer_left, class, ("flex"; "items-center"; "gap-2")).
    elem(status_icon, icon, footer_left).
    attr(status_icon, icon, "CircleCheck")  :- not _clinguin_unsat, not all_locked.
    attr(status_icon, icon, "PartyPopper")  :- all_locked.
    attr(status_icon, icon, "CircleX")      :- _clinguin_unsat.
    elem(status_text, text, footer_left).
    attr(status_text, text, "Ready — use dropdowns to assign pigeons") :- not _clinguin_unsat, not all_locked.
    attr(status_text, text, "All pigeons locked in!")                  :- all_locked, not _clinguin_unsat.
    attr(status_text, text, "Unsatisfiable — contradicting assumptions") :- _clinguin_unsat.
    attr(status_text, class, ("text-sm"; "text-muted-foreground"))              :- not _clinguin_unsat, not all_locked.
    attr(status_text, class, ("text-sm"; "font-semibold"; "text-green-700"))    :- all_locked, not _clinguin_unsat.
    attr(status_text, class, ("text-sm"; "font-semibold"; "text-destructive"))  :- _clinguin_unsat.

elem(footer_right, container, footer).
attr(footer_right, class, ("flex"; "items-center"; "gap-3")).
    elem(next_btn, button, footer_right).
    attr(next_btn, label, "Next solution").
    attr(next_btn, variant, "outline").
    attr(next_btn, order, 1).
    when(next_btn, click, call, next_solution).
        elem(next_btn_icon, icon, next_btn).
        attr(next_btn_icon, icon, "ArrowRight").
    elem(select_btn, button, footer_right).
    attr(select_btn, label, "Lock in solution").
    attr(select_btn, order, 2).
    when(select_btn, click, call, select).
        elem(select_btn_icon, icon, select_btn).
        attr(select_btn_icon, icon, "Lock").


% ── TOASTS ───────────────────────────────────
elem(unsat_msg, sonner, w) :- _clinguin_unsat.
attr(unsat_msg, title, "Unsatisfiable!") :- _clinguin_unsat.
attr(unsat_msg, description, "No valid assignment exists with current constraints.") :- _clinguin_unsat.
attr(unsat_msg, type, success) :- _clinguin_unsat.

elem(complete_msg, sonner, w) :- all_locked.
attr(complete_msg, title, "Assignment complete!") :- all_locked.
attr(complete_msg, description, "All pigeons have been locked into their boxes.") :- all_locked.
attr(complete_msg, type, success) :- all_locked.
