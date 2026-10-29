% ============================================================================
% MENU BAR TEMPLATE
%
% Enable it in ui.lp:
%     #include "menu-bar.lp".
%
% The template requires ui_app and provides three insertion points:
%     menubar_left    - application identity
%     menubar_center  - navigation or status information
%     menubar_right   - buttons and menus
%
% Edit "CUSTOMIZATION" below for the usual changes.
% Optional elements are available at the end.
% ============================================================================


% ============================================================================
% CUSTOMIZATION
%
% Change the text and icon below. Comment out a menubar_show/1 fact to hide
% the corresponding element.
% ============================================================================

menubar_title("My Application").
menubar_subtitle("Interactive ASP application").
menubar_icon("Menu").

menubar_show(icon).
menubar_show(subtitle).
menubar_show(theme).


% ============================================================================
% STRUCTURE
% ============================================================================

elem(menubar, header, ui_app).
attr(menubar, order, 10).

% Remove "sticky" and "top-0" to let the menu bar scroll with the page.
attr(menubar, class,
    ("sticky";
     "top-0";
     "z-50";
     "w-full";
     "border-b";
     "border-border";
     "bg-background/95";
     "text-foreground";
     "shadow-sm";
     "backdrop-blur")).

    elem(menubar_inner, div, menubar).
    attr(menubar_inner, class,
        ("mx-auto";
         "flex";
         "h-14";
         "w-full";
         "max-w-screen-2xl";
         "items-center";
         "gap-3";
         "px-4";
         "sm:px-6")).
    attr(menubar_inner, order, 1).


        % --------------------------------------------------------------------
        % LEFT
        % Icon, title and subtitle.
        % --------------------------------------------------------------------

        elem(menubar_left, div, menubar_inner).
        attr(menubar_left, class,
            ("flex";
             "min-w-0";
             "flex-1";
             "items-center";
             "gap-3")).
        attr(menubar_left, order, 1).

            elem(menubar_title_icon, icon, menubar_left) :-
                menubar_show(icon).
            attr(menubar_title_icon, icon, Icon) :-
                menubar_icon(Icon),
                menubar_show(icon).
            attr(menubar_title_icon, icon_size, "size-5") :-
                menubar_show(icon).
            attr(menubar_title_icon, class, "text-primary") :-
                menubar_show(icon).
            attr(menubar_title_icon, order, 1) :-
                menubar_show(icon).

            elem(menubar_heading, div, menubar_left).
            attr(menubar_heading, class,
                ("flex";
                 "min-w-0";
                 "flex-col";
                 "leading-tight")).
            attr(menubar_heading, order, 2).

                elem(menubar_title_text, span, menubar_heading).
                attr(menubar_title_text, text, Title) :-
                    menubar_title(Title).
                attr(menubar_title_text, class,
                    ("truncate";
                     "text-sm";
                     "font-semibold";
                     "sm:text-base")).
                attr(menubar_title_text, order, 1).

                elem(menubar_subtitle_text, span, menubar_heading) :-
                    menubar_show(subtitle).
                attr(menubar_subtitle_text, text, Subtitle) :-
                    menubar_subtitle(Subtitle),
                    menubar_show(subtitle).
                attr(menubar_subtitle_text, class,
                    ("hidden";
                     "truncate";
                     "text-xs";
                     "text-muted-foreground";
                     "sm:block")) :-
                    menubar_show(subtitle).
                attr(menubar_subtitle_text, order, 2) :-
                    menubar_show(subtitle).


        % --------------------------------------------------------------------
        % CENTER
        % --------------------------------------------------------------------

        elem(menubar_center, div, menubar_inner).
        attr(menubar_center, class,
            ("hidden";
             "items-center";
             "justify-center";
             "gap-2";
             "md:flex")).
        attr(menubar_center, order, 2).


        % --------------------------------------------------------------------
        % RIGHT
        % Optional actions followed by the theme toggle.
        % --------------------------------------------------------------------

        elem(menubar_right, div, menubar_inner).
        attr(menubar_right, class,
            ("flex";
             "min-w-0";
             "flex-1";
             "items-center";
             "justify-end";
             "gap-2")).
        attr(menubar_right, order, 3).

            elem(menubar_theme, theme_toggle, menubar_right) :-
                menubar_show(theme).
            attr(menubar_theme, variant, "ghost") :-
                menubar_show(theme).
            attr(menubar_theme, size, "icon") :-
                menubar_show(theme).
            attr(menubar_theme, order, 100) :-
                menubar_show(theme).


% ============================================================================
% OPTIONAL ELEMENTS
% ============================================================================


% -----------------------------------------------------------------------------
% SOLVER ACTIONS
% Edit or remove their when/4 atoms as needed.
% -----------------------------------------------------------------------------

%*
            elem(menubar_next_button, button, menubar_right).
            attr(menubar_next_button, text, "Next solution").
            attr(menubar_next_button, variant, "outline").
            attr(menubar_next_button, size, "sm").
            attr(menubar_next_button, order, 1).
            when(menubar_next_button, click, call, next_solution).

            elem(menubar_clear_button, button, menubar_right).
            attr(menubar_clear_button, text, "Clear").
            attr(menubar_clear_button, variant, "ghost").
            attr(menubar_clear_button, size, "sm").
            attr(menubar_clear_button, order, 2).
            when(menubar_clear_button, click, call, clear_assumptions).
*%
