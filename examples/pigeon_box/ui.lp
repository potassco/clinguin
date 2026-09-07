% ══════════════════════════════════════════════════════════════
% DERIVED FACTS
% ══════════════════════════════════════════════════════════════

shown_assignment(P,B) :- _all(in(P,B)).
shown_assignment(P,B) :- in(P,B), _clinguin_browsing.
has_assignment(P)     :- shown_assignment(P,_).
available(B,P)        :- box(B), pigeon(P), _any(in(P,B)), not _all(in(P,B)).
assumed(P,B)          :- _clinguin_assume(in(P,B), true).
locked_pigeon(P)      :- assumed(P,_).

n_locked(N)     :- N = #count { P : locked_pigeon(P) }.
n_pigeons(N)    :- N = #count { P : pigeon(P) }.
n_boxes_used(N) :- N = #count { B : shown_assignment(_, B) }.

all_locked :- n_locked(N), n_pigeons(N), N > 0.

status(unsat)    :- _clinguin_unsat.
status(complete) :- all_locked, not _clinguin_unsat.
status(ready)    :- not _clinguin_unsat, not all_locked.


% ══════════════════════════════════════════════════════════════
% ROOT
% ══════════════════════════════════════════════════════════════

elem(w, window, root).
attr(w, class, ("min-h-screen"; "flex"; "flex-col"; "bg-muted")).


% ══════════════════════════════════════════════════════════════
% HEADER
% ══════════════════════════════════════════════════════════════

elem(header, container, w).
attr(header, class, ("flex"; "items-center"; "justify-between"; "px-6"; "py-4"; "bg-card"; "border-b")).
attr(header, order, 1).

elem(header_left, container, header).
attr(header_left, class, ("flex"; "items-center"; "gap-2")).
attr(header_left, order, 1).
    elem(title_icon, icon, header_left).
    attr(title_icon, icon, "Bird").
    attr(title_icon, order, 1).
    elem(title, text, header_left).
    attr(title, text, "Pigeonhole Assignment").
    attr(title, class, ("text-xl"; "font-bold"; "text-primary")).
    attr(title, order, 2).

elem(header_right, container, header).
attr(header_right, class, ("flex"; "items-center"; "gap-2")).
attr(header_right, order, 2).

    elem(tools_menu, dropdown_menu, header_right).
    attr(tools_menu, order, 1).

        elem(tools_trigger, dropdown_menu(trigger), tools_menu).
        attr(tools_trigger, content, "Tools").
        attr(tools_trigger, class, ("inline-flex"; "items-center"; "gap-2"; "border"; "rounded-md"; "px-3"; "py-2"; "text-sm"; "font-medium")).
            elem(tools_trigger_icon, icon, tools_trigger).
            attr(tools_trigger_icon, icon, "Settings").
            attr(tools_trigger_icon, order, 1).

        elem(tools_content, dropdown_menu(content), tools_menu).
        attr(tools_content, align, "end").
        attr(tools_content, class, "w-52").

            elem(tools_label, dropdown_menu(label), tools_content).
            attr(tools_label, content, "Actions").
            attr(tools_label, order, 1).

            elem(clear_item, dropdown_menu(item), tools_content).
            attr(clear_item, content, "Clear assumptions").
            attr(clear_item, variant, "destructive").
            attr(clear_item, order, 2).
            when(clear_item, click, call, clear_assumptions).
                elem(clear_icon, icon, clear_item).
                attr(clear_icon, icon, "Eraser").
                attr(clear_icon, order, 1).

            elem(restart_item, dropdown_menu(item), tools_content).
            attr(restart_item, content, "Restart").
            attr(restart_item, variant, "destructive").
            attr(restart_item, order, 3).
            when(restart_item, click, call, restart).
                elem(restart_icon, icon, restart_item).
                attr(restart_icon, icon, "RotateCcw").
                attr(restart_icon, order, 1).

    elem(toggle, theme_toggle, header_right).
    attr(toggle, order, 2).
    attr(toggle, icon_dark, "Sun").
    attr(toggle, icon_light, "Moon").
    attr(toggle, variant, "outline").
    attr(toggle, class, ("p-2"; "rounded-full")).


% ══════════════════════════════════════════════════════════════
% STATS BAR
% ══════════════════════════════════════════════════════════════

stat(locked,  "Lock",    "Locked",     1).
stat(pigeons, "Bird",    "Pigeons",    2).
stat(boxes,   "Package", "Boxes used", 3).

attr(stat_val(locked),  text, N) :- n_locked(N).
attr(stat_val(pigeons), text, N) :- n_pigeons(N).
attr(stat_val(boxes),   text, N) :- n_boxes_used(N).

elem(stats_bar, container, w).
attr(stats_bar, class, ("flex"; "items-center"; "gap-3"; "px-6"; "py-3"; "bg-card"; "border-b")).
attr(stats_bar, order, 2).

elem(stat_card(K), container, stats_bar) :- stat(K, _, _, _).
attr(stat_card(K), class, ("flex"; "items-center"; "gap-3"; "px-4"; "py-2"; "bg-muted"; "rounded-lg"; "min-w-32")) :- stat(K, _, _, _).
attr(stat_card(K), order, Order) :- stat(K, _, _, Order).

    elem(stat_icon(K), icon, stat_card(K)) :- stat(K, Icon, _, _).
    attr(stat_icon(K), icon, Icon)         :- stat(K, Icon, _, _).
    attr(stat_icon(K), order, 1)           :- stat(K, _, _, _).

    elem(stat_info(K), container, stat_card(K)) :- stat(K, _, _, _).
    attr(stat_info(K), class, ("flex"; "flex-col")) :- stat(K, _, _, _).
    attr(stat_info(K), order, 2) :- stat(K, _, _, _).

        elem(stat_val(K), text, stat_info(K)) :- stat(K, _, _, _).
        attr(stat_val(K), class, ("text-2xl"; "font-bold"; "leading-none")) :- stat(K, _, _, _).
        attr(stat_val(K), order, 1) :- stat(K, _, _, _).

        elem(stat_lbl(K), text, stat_info(K)) :- stat(K, _, Label, _).
        attr(stat_lbl(K), text, Label) :- stat(K, _, Label, _).
        attr(stat_lbl(K), class, ("text-xs"; "text-muted-foreground")) :- stat(K, _, Label, _).
        attr(stat_lbl(K), order, 2) :- stat(K, _, Label, _).


% ══════════════════════════════════════════════════════════════
% MAIN
% ══════════════════════════════════════════════════════════════

elem(main, container, w).
attr(main, class, ("flex"; "flex-row"; "flex-wrap"; "gap-4"; "p-6"; "grow"; "content-start")).
attr(main, order, 3).

elem(box_card(B), container, main) :- box(B).
attr(box_card(B), class, ("flex"; "flex-col"; "gap-2"; "p-3"; "bg-card"; "border"; "rounded-lg"; "shadow-sm"; "w-44")) :- box(B).
attr(box_card(B), order, B) :- box(B).

    elem(box_header(B), container, box_card(B)) :- box(B).
    attr(box_header(B), class, ("flex"; "items-center"; "justify-between"; "gap-2")) :- box(B).
    attr(box_header(B), order, 1) :- box(B).

        elem(box_title(B), container, box_header(B)) :- box(B).
        attr(box_title(B), class, ("flex"; "items-center"; "gap-2")) :- box(B).
        attr(box_title(B), order, 1) :- box(B).
            elem(box_icon(B), icon, box_title(B)) :- box(B).
            attr(box_icon(B), icon, "Package") :- box(B).
            attr(box_icon(B), order, 1) :- box(B).
            elem(box_label(B), text, box_title(B)) :- box(B).
            attr(box_label(B), text, @concat("Box ", B)) :- box(B).
            attr(box_label(B), class, ("text-sm"; "font-semibold")) :- box(B).
            attr(box_label(B), order, 2) :- box(B).

        % Assign-pigeon dropdown
        elem(box_dd(B), dropdown_menu, box_header(B)) :- box(B).
        attr(box_dd(B), order, 2) :- box(B).

            elem(box_dd_trigger(B), dropdown_menu(trigger), box_dd(B)) :- box(B).
            attr(box_dd_trigger(B), content, "+") :- box(B).
            attr(box_dd_trigger(B), class, ("inline-flex"; "items-center"; "justify-center"; "h-7"; "w-7"; "text-sm"; "rounded-full"; "border")) :- box(B).

            elem(box_dd_content(B), dropdown_menu(content), box_dd(B)) :- box(B).
            attr(box_dd_content(B), class, "w-44") :- box(B).

                elem(box_dd_label(B), dropdown_menu(label), box_dd_content(B)) :- box(B).
                attr(box_dd_label(B), content, "Assign pigeon") :- box(B).
                attr(box_dd_label(B), order, 1) :- box(B).

                elem(box_ddi(B,P), dropdown_menu(item), box_dd_content(B)) :- available(B,P).
                attr(box_ddi(B,P), content, @concat("Pigeon ", P)) :- available(B,P).
                attr(box_ddi(B,P), order, P + 1) :- available(B,P).
                when(box_ddi(B,P), click, call, add_assumption(in(P,B),true)) :- available(B,P).
                    elem(box_ddi_icon(B,P), icon, box_ddi(B,P)) :- available(B,P).
                    attr(box_ddi_icon(B,P), icon, "Plus") :- available(B,P).
                    attr(box_ddi_icon(B,P), order, 1) :- available(B,P).

    elem(box_pigeons(B), container, box_card(B)) :- box(B).
    attr(box_pigeons(B), class, ("flex"; "flex-col"; "gap-1"; "min-h-6")) :- box(B).
    attr(box_pigeons(B), order, 2) :- box(B).

        elem(chip(B,P), container, box_pigeons(B)) :- shown_assignment(P,B).
        attr(chip(B,P), class, ("flex"; "items-center"; "justify-between"; "gap-1"; "px-2"; "py-1"; "rounded"; "text-xs")) :- shown_assignment(P,B).
        attr(chip(B,P), class, ("bg-primary"; "text-primary-foreground")) :- shown_assignment(P,B), locked_pigeon(P).
        attr(chip(B,P), class, ("bg-accent"; "text-accent-foreground"))   :- shown_assignment(P,B), not locked_pigeon(P).
        attr(chip(B,P), class, ("group"; "cursor-pointer"; "hover:bg-destructive"; "hover:text-destructive-foreground")) :- assumed(P,B).
        attr(chip(B,P), order, P) :- shown_assignment(P,B).
        when(chip(B,P), click, call, remove_assumption(in(P,B))) :- assumed(P,B).

            elem(chip_label(B,P), text, chip(B,P)) :- shown_assignment(P,B).
            attr(chip_label(B,P), text, @concat("Pigeon ", P)) :- shown_assignment(P,B).
            attr(chip_label(B,P), order, 1) :- shown_assignment(P,B).

            elem(chip_x(B,P), icon, chip(B,P)) :- assumed(P,B).
            attr(chip_x(B,P), icon, "X") :- assumed(P,B).
            attr(chip_x(B,P), class, ("hidden"; "group-hover:inline-block")) :- assumed(P,B).
            attr(chip_x(B,P), order, 2) :- assumed(P,B).


% ══════════════════════════════════════════════════════════════
% STATUS ALERT
% ══════════════════════════════════════════════════════════════

elem(status_bar, container, w).
attr(status_bar, class, ("flex"; "items-center"; "gap-4"; "px-6"; "pb-4")).
attr(status_bar, order, 4).

elem(status_alert, alert, status_bar).
attr(status_alert, variant, "default")     :- status(ready).
attr(status_alert, variant, "default")     :- status(complete).
attr(status_alert, variant, "destructive") :- status(unsat).
attr(status_alert, class, "flex-1").
attr(status_alert, order, 1).

    elem(status_icon, icon, status_alert).
    attr(status_icon, icon, "CircleCheck") :- status(ready).
    attr(status_icon, icon, "PartyPopper") :- status(complete).
    attr(status_icon, icon, "CircleX")     :- status(unsat).
    attr(status_icon, order, 1).

    elem(status_title, alert(title), status_alert).
    attr(status_title, content, "Ready")          :- status(ready).
    attr(status_title, content, "All locked in!") :- status(complete).
    attr(status_title, content, "Unsatisfiable")  :- status(unsat).
    attr(status_title, order, 2).

    elem(status_desc, alert(description), status_alert).
    attr(status_desc, content, "Use the + on each box to assign a pigeon.")       :- status(ready).
    attr(status_desc, content, "Every pigeon has been locked into a box.")        :- status(complete).
    attr(status_desc, content, "The current assumptions contradict each other.")  :- status(unsat).
    attr(status_desc, order, 3).

elem(help_dialog, dialog, status_bar).
attr(help_dialog, open, false).
attr(help_dialog, order, 2).

    elem(help_trigger, dialog(trigger), help_dialog).
    attr(help_trigger, content, "How it works").
    attr(help_trigger, class, ("inline-flex"; "items-center"; "gap-2"; "h-9"; "px-4"; "rounded-md"; "border"; "bg-background"; "text-sm"; "font-medium")).
        elem(help_trigger_icon, icon, help_trigger).
        attr(help_trigger_icon, icon, "CircleHelp").
        attr(help_trigger_icon, order, 1).

    elem(help_content, dialog(content), help_dialog).
    attr(help_content, class, "sm:max-w-md").

        elem(help_header, dialog(header), help_content).
        attr(help_header, order, 1).
            elem(help_title, dialog(title), help_header).
            attr(help_title, content, "The pigeonhole principle").
            attr(help_title, order, 1).
            elem(help_desc, dialog(description), help_header).
            attr(help_desc, content, "With one spare box, a full assignment always exists. Pick one and lock it in.").
            attr(help_desc, order, 2).

        elem(help_footer, dialog(footer), help_content).
        attr(help_footer, order, 2).
            elem(help_close, dialog(close), help_footer).
            attr(help_close, content, "Got it").
            attr(help_close, class, ("inline-flex"; "h-9"; "items-center"; "px-4"; "rounded-md"; "bg-primary"; "text-primary-foreground"; "text-sm"; "font-medium")).


% ══════════════════════════════════════════════════════════════
% FOOTER
% ══════════════════════════════════════════════════════════════

elem(footer, container, w).
attr(footer, class, ("flex"; "items-center"; "justify-end"; "gap-3"; "px-6"; "py-4"; "bg-card"; "border-t")).
attr(footer, order, 5).

    elem(next_btn, button, footer).
    attr(next_btn, content, "Next solution").
    attr(next_btn, variant, "outline").
    attr(next_btn, order, 1).
    when(next_btn, click, call, next_solution).
        elem(next_btn_icon, icon, next_btn).
        attr(next_btn_icon, icon, "ArrowRight").
        attr(next_btn_icon, order, 1).

    elem(select_btn, button, footer).
    attr(select_btn, content, "Lock in solution").
    attr(select_btn, order, 2).
    when(select_btn, click, call, select).
        elem(select_btn_icon, icon, select_btn).
        attr(select_btn_icon, icon, "Lock").
        attr(select_btn_icon, order, 1).


% ══════════════════════════════════════════════════════════════
% TOASTS
% ══════════════════════════════════════════════════════════════

elem(unsat_msg, sonner, w) :- status(unsat).
attr(unsat_msg, title, "Unsatisfiable!") :- status(unsat).
attr(unsat_msg, description, "No valid assignment with current assumptions.") :- status(unsat).
attr(unsat_msg, type, error) :- status(unsat).

elem(complete_msg, sonner, w) :- status(complete).
attr(complete_msg, title, "Assignment complete!") :- status(complete).
attr(complete_msg, description, "All pigeons are locked into boxes.") :- status(complete).
attr(complete_msg, type, success) :- status(complete).
