% DATA

% demo(Id,  Key,  MenuLabel,  ButtonLabel,  Variant,  TailwindClass,  Icon).
demo(1, "demo_1", "Pill", "Get started", "outline", "rounded-full bg-sky-100 text-sky-900 border-sky-200 shadow-sm px-8", "Rocket").
demo(2, "demo_2", "Compact", "ADD ITEM", "secondary", "rounded-lg tracking-wide font-semibold bg-slate-100 text-slate-900 shadow-sm", "Plus").
demo(3, "demo_3", "Border", "Confirm", "outline", "border-4 border-sky-300 rounded-xl bg-white shadow-sm", "Check").
demo(4, "demo_4", "Warning", "Warning", "outline", "bg-amber-100 text-amber-900 border-amber-200 shadow-sm rounded-xl", "AlertTriangle").
demo(5, "demo_5", "Click", "Click me", "ghost", "rounded-md px-3 py-1 text-sm border border-slate-200 bg-white", "MousePointerClick").

demo_line(1, 1, "elem(preview_btn,  button,  preview_card).").
demo_line(1, 2, "attr(preview_btn,  text,  'Get started').").
demo_line(1, 3, "attr(preview_btn,  variant,  'outline').").
demo_line(1, 4, "attr(preview_btn,  class,  ('rounded-full'; 'bg-sky-100';").
demo_line(1, 5, "    'text-sky-900'; 'border-sky-200'; 'shadow-sm'; 'px-8')).").
demo_line(1, 6, "elem(preview_icon,  icon,  preview_btn).").
demo_line(1, 7, "attr(preview_icon,  icon,  'Rocket').").

demo_line(2, 1, "elem(preview_btn,  button,  preview_card).").
demo_line(2, 2, "attr(preview_btn,  text,  'ADD ITEM').").
demo_line(2, 3, "attr(preview_btn,  variant,  'secondary').").
demo_line(2, 4, "attr(preview_btn,  class,  ('rounded-lg'; 'tracking-wide';").
demo_line(2, 5, "    'font-semibold'; 'bg-slate-100'; 'text-slate-900'; 'shadow-sm')).").
demo_line(2, 6, "elem(preview_icon,  icon,  preview_btn).").
demo_line(2, 7, "attr(preview_icon,  icon,  'Plus').").

demo_line(3, 1, "elem(preview_btn,  button,  preview_card).").
demo_line(3, 2, "attr(preview_btn,  text,  'Confirm').").
demo_line(3, 3, "attr(preview_btn,  variant,  'outline').").
demo_line(3, 4, "attr(preview_btn,  class,  ('border-4'; 'border-sky-300';").
demo_line(3, 5, "    'rounded-xl'; 'bg-white'; 'shadow-sm')).").
demo_line(3, 6, "elem(preview_icon,  icon,  preview_btn).").
demo_line(3, 7, "attr(preview_icon,  icon,  'Check').").

demo_line(4, 1, "elem(preview_btn,  button,  preview_card).").
demo_line(4, 2, "attr(preview_btn,  text,  'Warning').").
demo_line(4, 3, "attr(preview_btn,  variant,  'outline').").
demo_line(4, 4, "attr(preview_btn,  class,  ('bg-amber-100'; 'text-amber-900';").
demo_line(4, 5, "    'border-amber-200'; 'shadow-sm'; 'rounded-xl')).").
demo_line(4, 6, "elem(preview_icon,  icon,  preview_btn).").
demo_line(4, 7, "attr(preview_icon,  icon,  'AlertTriangle').").

demo_line(5, 1, "elem(preview_btn,  button,  preview_card).").
demo_line(5, 2, "attr(preview_btn,  text,  'Click me').").
demo_line(5, 3, "attr(preview_btn,  variant,  'ghost').").
demo_line(5, 4, "attr(preview_btn,  class,  ('rounded-md'; 'px-3'; 'py-1';").
demo_line(5, 5, "    'text-sm'; 'border'; 'border-slate-200'; 'bg-white')).").
demo_line(5, 6, "elem(preview_icon,  icon,  preview_btn).").
demo_line(5, 7, "attr(preview_icon,  icon,  'MousePointerClick').").
demo_line(5, 8, "when(preview_btn,  click,  update,  (status,  text,  'Clicked!')).").

visible_panel_class("grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch").
hidden_panel_class("hidden").

card(typography, "Typography", "Type").
card(colors, "Colors", "Palette").
card(buttons, "Buttons", "MousePointerClick").
card(radius, "Radius", "Circle").
card(borders, "Borders", "Square").
card(shadows, "Shadows", "Layers").
card(opacity, "Opacity", "Eye").
card(spacing, "Padding and gap", "Ruler").
card(flex, "Flex justify", "AlignLeft").
card(grid, "CSS grid", "Grid3x3").
card(width, "Fractional widths", "Columns3").
card(checkbox, "Checkbox", "Check").
card(field, "Field", "Form").
card(theme, "Theme tokens", "SunMoon").
card(states, "Control states", "SlidersHorizontal").
card(forms, "Form controls", "ListChecks").
card(feedback, "Feedback and loading", "Activity").

dash_col(1..4).

card_col(typography, 1, 1).
card_col(radius, 1, 2).
card_col(borders, 1, 3).
card_col(flex, 1, 4).
card_col(colors, 2, 1).
card_col(shadows, 2, 2).
card_col(opacity, 2, 3).
card_col(width, 2, 4).
card_col(buttons, 3, 1).
card_col(spacing, 3, 2).
card_col(grid, 3, 3).
card_col(checkbox, 4, 1).
card_col(field, 4, 2).
card_col(theme, 1, 5).
card_col(states, 2, 5).
card_col(forms, 3, 4).
card_col(feedback, 4, 3).

caption(typography, 2, "text-{value}").
caption(typography, 4, "font-{value}").
caption(colors, 2, "bg-{value}").
caption(colors, 4, "bg-emerald-{value}").
caption(colors, 6, "text-{value}").
caption(buttons, 2, "variant-{value}").
caption(buttons, 4, "size-{value}").
caption(radius, 2, "rounded-{value}").
caption(borders, 2, "border-{value}").
caption(shadows, 2, "shadow-{value}").
caption(opacity, 2, "opacity-{value}").
caption(spacing, 2, "p-{value}").
caption(spacing, 4, "gap-{value}").
caption(flex, 2, "justify-{value}").
caption(grid, 2, "grid-cols-{value}").
caption(grid, 4, "col-span-{value}").
caption(width, 2, "w-{value}").
caption(field, 3, "field(set) + field(label) + field(description)").
caption(field, 6, "field(group) + field(error)").
caption(theme, 2, "semantic colors + dark mode").
caption(states, 2, "hover / focus / selected / disabled / loading").
caption(forms, 2, "input + textarea + select").
caption(feedback, 2, "alert + skeleton + spinner").

typo(1, "xs", "text-xs").
typo(2, "sm", "text-sm").
typo(3, "base", "text-base").
typo(4, "lg", "text-lg").
typo(5, "xl", "text-xl").
typo(6, "2xl", "text-2xl").
typo(7, "3xl", "text-3xl").

weight(1, "light", "font-light").
weight(2, "normal", "font-normal").
weight(3, "medium", "font-medium").
weight(4, "semibold", "font-semibold").
weight(5, "bold", "font-bold").
weight(6, "black", "font-black").

palette(1, "red-200", "bg-red-200", "text-red-950").
palette(2, "orange-200", "bg-orange-200", "text-orange-950").
palette(3, "amber-200", "bg-amber-200", "text-amber-950").
palette(4, "lime-200", "bg-lime-200", "text-lime-950").
palette(5, "emerald-200", "bg-emerald-200", "text-emerald-950").
palette(6, "teal-200", "bg-teal-200", "text-teal-950").
palette(7, "cyan-200", "bg-cyan-200", "text-cyan-950").
palette(8, "sky-200", "bg-sky-200", "text-sky-950").
palette(9, "violet-200", "bg-violet-200", "text-violet-950").
palette(10, "rose-200", "bg-rose-200", "text-rose-950").

shade(1, "50", "bg-emerald-50", "text-emerald-950").
shade(2, "100", "bg-emerald-100", "text-emerald-950").
shade(3, "200", "bg-emerald-200", "text-emerald-950").
shade(4, "300", "bg-emerald-300", "text-emerald-950").
shade(5, "400", "bg-emerald-400", "text-emerald-950").

text_color(1, "slate-950", "text-slate-950").
text_color(2, "slate-500", "text-slate-500").
text_color(3, "sky-500", "text-sky-500").
text_color(4, "rose-500", "text-rose-500").
text_color(5, "violet-500", "text-violet-500").
text_color(6, "emerald-500", "text-emerald-500").

btn_demo(1, "default", "Default", "Sparkles").
btn_demo(2, "secondary", "Secondary", "Layers").
btn_demo(3, "outline", "Outline", "Shield").
btn_demo(4, "ghost", "Ghost", "Zap").
btn_demo(5, "destructive", "Destructive", "Flame").
btn_demo(6, "link", "Link", "Link2").

rounding(1, "none", "rounded-none", "bg-sky-200").
rounding(2, "sm", "rounded-sm", "bg-sky-200").
rounding(3, "md", "rounded-md", "bg-sky-200").
rounding(4, "lg", "rounded-lg", "bg-sky-200").
rounding(5, "xl", "rounded-xl", "bg-sky-200").
rounding(6, "full", "rounded-full", "bg-sky-200").

border_demo(1, "2", "border-2 border-violet-200").
border_demo(2, "4", "border-4 border-violet-300").
border_demo(3, "dashed", "border-4 border-dashed border-violet-300").
border_demo(4, "dotted", "border-4 border-dotted border-violet-300").

shadow_demo(1, "none", "shadow-none").
shadow_demo(2, "base", "shadow").
shadow_demo(3, "md", "shadow-md").
shadow_demo(4, "lg", "shadow-lg").
shadow_demo(5, "xl", "shadow-xl").
shadow_demo(6, "2xl", "shadow-2xl").

opacity_demo(1, "100", "opacity-100").
opacity_demo(2, "75", "opacity-75").
opacity_demo(3, "50", "opacity-50").
opacity_demo(4, "30", "opacity-30").

padding_demo(1, "1", "p-1").
padding_demo(2, "2", "p-2").
padding_demo(3, "4", "p-4").
padding_demo(4, "6", "p-6").

gap_demo(1, "1", "gap-1").
gap_demo(2, "2", "gap-2").
gap_demo(3, "4", "gap-4").
gap_demo(4, "6", "gap-6").

align_row(1, "start", "justify-start").
align_row(2, "center", "justify-center").
align_row(3, "between", "justify-between").
align_row(4, "end", "justify-end").
flex_item(1, "A").
flex_item(2, "B").
flex_item(3, "C").

grid_variant(1, "2", "grid-cols-2").
grid_variant(2, "3", "grid-cols-3").
grid_variant(3, "4", "grid-cols-4").
grid_cell(1..8).

span_demo_cell(1, 1, "2", "col-span-2", "bg-sky-200", "text-sky-950", "order-1").
span_demo_cell(1, 2, "", "", "bg-slate-300", "text-slate-950", "order-2").
span_demo_cell(1, 3, "", "", "bg-slate-300", "text-slate-950", "order-3").
span_demo_cell(2, 1, "3", "col-span-3", "bg-violet-200", "text-violet-950", "order-1").
span_demo_cell(2, 2, "", "", "bg-slate-300", "text-slate-950", "order-2").

width_demo(1, "1/4", "w-1/4").
width_demo(2, "1/3", "w-1/3").
width_demo(3, "1/2", "w-1/2").
width_demo(4, "2/3", "w-2/3").
width_demo(5, "3/4", "w-3/4").
width_demo(6, "full", "w-full").

checkbox_demo(1, "checked", "Default").
checkbox_demo(2, "disabled", "Disabled").
checkbox_demo(3, "indeterminate", "Indeterminate").

theme_token(1, "background", "bg-background text-foreground border-border").
theme_token(2, "card", "bg-card text-card-foreground border-border").
theme_token(3, "primary", "bg-primary text-primary-foreground border-primary").
theme_token(4, "secondary", "bg-secondary text-secondary-foreground border-secondary").
theme_token(5, "accent", "bg-accent text-accent-foreground border-accent").
theme_token(6, "muted", "bg-muted text-muted-foreground border-border").
theme_token(7, "destructive", "bg-destructive text-white border-destructive").

control_state(1, "Default", "Ready", "default", "", false).
control_state(2, "Hover + focus", "Interact", "outline", "hover:bg-primary hover:text-primary-foreground focus-visible:ring-primary/40", false).
control_state(3, "Selected", "Selected", "secondary", "ring-2 ring-primary ring-offset-2", false).
control_state(4, "Destructive", "Delete", "destructive", "", false).
control_state(5, "Disabled", "Unavailable", "outline", "", true).
control_state(6, "Loading", "Saving…", "secondary", "", true).

select_option(1, "compact", "Compact").
select_option(2, "comfortable", "Comfortable").
select_option(3, "spacious", "Spacious").

class(caption, "w-fit rounded-md bg-slate-100 px-2 py-1 text-xs font-mono text-slate-500").
class(card, "flex flex-col gap-4 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm h-fit min-w-0").
class(icon_box, "w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center shrink-0").
class(panel, "bg-slate-50 rounded-xl p-4").

% PAGE SHELL

elem(ui_app, div, root).
attr(ui_app, class, ("min-h-screen";"flex";"flex-col";"bg-slate-50";"text-slate-950")).

elem(header, header, ui_app).
attr(header, class, ("bg-white";"border-b";"border-slate-200";"sticky";"top-0";"z-20";"shadow-sm")).
attr(header, order, 1).

elem(header_inner, div, header).
attr(header_inner, class, ("max-w-screen-2xl";"mx-auto";"w-full";"px-4";"sm:px-8";"py-3";"flex";"items-center";"justify-start";"gap-4")).
attr(header_inner, order, 1).

elem(brand, div, header_inner).
attr(brand, class, ("flex";"items-center";"gap-3";"min-w-0")).
attr(brand, order, 1).

elem(brand_icon_wrap, div, brand).
attr(brand_icon_wrap, class, ("flex";"items-center";"justify-center";"w-9";"h-9";"rounded-xl";"bg-slate-100";"border";"border-slate-200";"shrink-0")).
attr(brand_icon_wrap, order, 1).

elem(brand_icon, icon, brand_icon_wrap).
attr(brand_icon, icon, "Layers").
attr(brand_icon, class, "text-slate-700").
attr(brand_icon, order, 1).

elem(brand_text, div, brand).
attr(brand_text, class, ("flex";"flex-col";"leading-tight";"min-w-0")).
attr(brand_text, order, 2).

elem(brand_name, text, brand_text).
attr(brand_name, text, "Clinguin v3").
attr(brand_name, class, ("text-base";"font-bold";"truncate")).
attr(brand_name, order, 1).

elem(brand_sub, text, brand_text).
attr(brand_sub, text, "Tailwind Component Showcase").
attr(brand_sub, class, ("text-xs";"text-slate-500";"truncate")).
attr(brand_sub, order, 2).

elem(ui_content, main, ui_app).
attr(ui_content, class, ("flex";"min-h-0";"grow";"flex-col")).
attr(ui_content, order, 100).

elem(hero, section, ui_content).
attr(hero, class, ("bg-slate-50";"border-b";"border-slate-200";"shrink-0")).
attr(hero, order, 2).

elem(hero_inner, div, hero).
attr(hero_inner, class, ("max-w-screen-2xl";"mx-auto";"w-full";"px-4";"sm:px-8";"pt-5";"pb-6";"flex";"flex-col";"gap-4")).
attr(hero_inner, order, 1).

elem(demo_panel(I), div, hero_inner) :- demo(I, _, _, _, _, _, _).
attr(demo_panel(1), class, C) :- visible_panel_class(C).
attr(demo_panel(I), class, C) :- demo(I, _, _, _, _, _, _), I!=1, hidden_panel_class(C).
attr(demo_panel(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(code_card(I), article, demo_panel(I)) :- demo(I, _, _, _, _, _, _).
attr(code_card(I), class, ("bg-white";"border";"border-slate-200";"rounded-2xl";"p-5";"shadow-sm";"flex";"flex-col";"min-w-0";"overflow-hidden")) :- demo(I, _, _, _, _, _, _).
attr(code_card(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(code_caption(I), text, code_card(I)) :- demo(I, _, _, _, _, _, _).
attr(code_caption(I), text, "CODE SNIPPET") :- demo(I, _, _, _, _, _, _).
attr(code_caption(I), class, ("text-xs";"font-semibold";"tracking-widest";"text-slate-500";"mb-3")) :- demo(I, _, _, _, _, _, _).
attr(code_caption(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(code_box(I), div, code_card(I)) :- demo(I, _, _, _, _, _, _).
attr(code_box(I), class, ("bg-slate-50";"rounded-xl";"p-4";"flex";"flex-col";"gap-1";"overflow-hidden")) :- demo(I, _, _, _, _, _, _).
attr(code_box(I), order, 2) :- demo(I, _, _, _, _, _, _).

elem(code_line(I, N), text, code_box(I)) :- demo_line(I, N, _).
attr(code_line(I, N), text, Text) :- demo_line(I, N, Text).
attr(code_line(I, N), class, ("text-xs";"font-mono";"text-slate-600";"whitespace-pre-wrap";"break-words";"leading-5")) :- demo_line(I, N, _).
attr(code_line(I, N), order, N) :- demo_line(I, N, _).

elem(preview_card(I), article, demo_panel(I)) :- demo(I, _, _, _, _, _, _).
attr(preview_card(I), class, ("bg-white";"border";"border-slate-200";"rounded-2xl";"p-5";"shadow-sm";"flex";"flex-col";"gap-4";"min-h-56")) :- demo(I, _, _, _, _, _, _).
attr(preview_card(I), order, 2) :- demo(I, _, _, _, _, _, _).

elem(preview_header(I), div, preview_card(I)) :- demo(I, _, _, _, _, _, _).
attr(preview_header(I), class, ("flex";"items-center";"justify-between";"gap-3";"min-w-0")) :- demo(I, _, _, _, _, _, _).
attr(preview_header(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(preview_label(I), text, preview_header(I)) :- demo(I, _, _, _, _, _, _).
attr(preview_label(I), text, "LIVE PREVIEW") :- demo(I, _, _, _, _, _, _).
attr(preview_label(I), class, ("text-xs";"font-semibold";"uppercase";"tracking-widest";"text-slate-500";"truncate")) :- demo(I, _, _, _, _, _, _).
attr(preview_label(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(example_menu(I), dropdown_menu, preview_header(I)) :- demo(I, _, _, _, _, _, _).
attr(example_menu(I), order, 2) :- demo(I, _, _, _, _, _, _).

elem(example_trigger(I), dropdown_menu(trigger), example_menu(I)) :- demo(I, _, _, _, _, _, _).
attr(example_trigger(I), text, "Change example") :- demo(I, _, _, _, _, _, _).
attr(example_trigger(I), class, ("rounded-lg";"border";"border-slate-200";"bg-white";"px-3";"py-2";"text-sm";"font-medium";"shadow-sm")) :- demo(I, _, _, _, _, _, _).
attr(example_trigger(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(example_content(I), dropdown_menu(content), example_menu(I)) :- demo(I, _, _, _, _, _, _).
attr(example_content(I), order, 2) :- demo(I, _, _, _, _, _, _).

elem(example_group(I), dropdown_menu(radio_group), example_content(I)) :- demo(I, _, _, _, _, _, _).
attr(example_group(I), value, "demo_1") :- demo(I, _, _, _, _, _, _).
attr(example_group(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(example_item(P, I), dropdown_menu(radio_item), example_group(P)) :- demo(P, _, _, _, _, _, _), demo(I, _, _, _, _, _, _).
attr(example_item(P, I), text, L) :- demo(P, _, _, _, _, _, _), demo(I, _, L, _, _, _, _).
attr(example_item(P, I), value, K) :- demo(P, _, _, _, _, _, _), demo(I, K, _, _, _, _, _).
attr(example_item(P, I), order, I) :- demo(P, _, _, _, _, _, _), demo(I, _, _, _, _, _, _).
when(example_item(P, I), click, update, (example_group(Q), value, K)) :- demo(P, _, _, _, _, _, _), demo(Q, _, _, _, _, _, _), demo(I, K, _, _, _, _, _).
when(example_item(P, I), click, update, (demo_panel(I), class, C)) :- demo(P, _, _, _, _, _, _), demo(I, _, _, _, _, _, _), visible_panel_class(C).
when(example_item(P, I), click, update, (demo_panel(J), class, C)) :- demo(P, _, _, _, _, _, _), demo(I, _, _, _, _, _, _), demo(J, _, _, _, _, _, _), I!=J, hidden_panel_class(C).

elem(preview_stage(I), div, preview_card(I)) :- demo(I, _, _, _, _, _, _).
attr(preview_stage(I), class, ("w-full";"flex-1";"min-h-32";"bg-slate-50";"rounded-xl";"flex";"items-center";"justify-center";"p-6")) :- demo(I, _, _, _, _, _, _).
attr(preview_stage(I), order, 2) :- demo(I, _, _, _, _, _, _).

elem(preview_btn(I), button, preview_stage(I)) :- demo(I, _, _, _, _, _, _).
attr(preview_btn(I), text, L) :- demo(I, _, _, L, _, _, _).
attr(preview_btn(I), variant, V) :- demo(I, _, _, _, V, _, _).
attr(preview_btn(I), class, C) :- demo(I, _, _, _, _, C, _).
attr(preview_btn(I), order, 1) :- demo(I, _, _, _, _, _, _).
when(preview_btn(I), click, update, (preview_status(I), text, "Clicked!")) :- demo(I, _, _, _, _, _, _).

elem(preview_icon(I), icon, preview_btn(I)) :- demo(I, _, _, _, _, _, _).
attr(preview_icon(I), icon, Icon) :- demo(I, _, _, _, _, _, Icon).
attr(preview_icon(I), order, 1) :- demo(I, _, _, _, _, _, _).

elem(preview_status(I), text, preview_card(I)) :- demo(I, _, _, _, _, _, _).
attr(preview_status(I), text, "click it →") :- demo(I, _, _, _, _, _, _).
attr(preview_status(I), class, ("text-xs";"text-slate-500";"italic";"text-center")) :- demo(I, _, _, _, _, _, _).
attr(preview_status(I), order, 3) :- demo(I, _, _, _, _, _, _).

elem(main, div, ui_content).
attr(main, class, ("max-w-screen-2xl";"mx-auto";"w-full";"px-4";"sm:px-8";"py-6";"flex";"flex-col";"gap-5")).
attr(main, order, 3).

elem(dashboard, div, main).
attr(dashboard, class, ("grid";"grid-cols-1";"lg:grid-cols-2";"xl:grid-cols-3";"gap-6";"items-start")).
attr(dashboard, order, 1).

elem(dash_col(C), div, dashboard) :- dash_col(C).
attr(dash_col(C), class, ("flex";"flex-col";"gap-6";"min-w-0")) :- dash_col(C).
attr(dash_col(C), order, C) :- dash_col(C).

elem(card(Key), section, dash_col(C)) :- card_col(Key, C, _).
attr(card(Key), class, C) :- card(Key, _, _), class(card, C).
attr(card(Key), order, O) :- card_col(Key, _, O).

elem(card_h(Key), div, card(Key)) :- card(Key, _, _).
attr(card_h(Key), class, ("flex";"items-center";"gap-3";"min-w-0")) :- card(Key, _, _).
attr(card_h(Key), order, 1) :- card(Key, _, _).

elem(card_h_icon_wrap(Key), div, card_h(Key)) :- card(Key, _, _).
attr(card_h_icon_wrap(Key), class, C) :- card(Key, _, _), class(icon_box, C).
attr(card_h_icon_wrap(Key), order, 1) :- card(Key, _, _).

elem(card_h_icon(Key), icon, card_h_icon_wrap(Key)) :- card(Key, _, _).
attr(card_h_icon(Key), icon, Icon) :- card(Key, _, Icon).
attr(card_h_icon(Key), class, "text-slate-700") :- card(Key, _, _).
attr(card_h_icon(Key), order, 1) :- card(Key, _, _).

elem(card_h_title(Key), text, card_h(Key)) :- card(Key, _, _).
attr(card_h_title(Key), text, Title) :- card(Key, Title, _).
attr(card_h_title(Key), class, ("font-semibold";"text-base";"truncate")) :- card(Key, _, _).
attr(card_h_title(Key), order, 2) :- card(Key, _, _).

elem(caption(Card, Order), text, card(Card)) :- caption(Card, Order, _).
attr(caption(Card, Order), text, Text) :- caption(Card, Order, Text).
attr(caption(Card, Order), class, C) :- caption(Card, Order, _), class(caption, C).
attr(caption(Card, Order), order, Order) :- caption(Card, Order, _).

% TYPOGRAPHY

elem(typo_scale, div, card(typography)).
attr(typo_scale, class, ("flex";"flex-col";"items-center";"text-center";"gap-1";"rounded-xl";"bg-slate-50";"p-4")).
attr(typo_scale, order, 3).

elem(ty(I), text, typo_scale) :- typo(I, _, _).
attr(ty(I), text, V) :- typo(I, V, _).
attr(ty(I), class, C) :- typo(I, _, C).
attr(ty(I), class, ("w-full";"text-center")) :- typo(I, _, _).
attr(ty(I), order, I) :- typo(I, _, _).

elem(weight_grid, div, card(typography)).
attr(weight_grid, class, ("grid";"grid-cols-2";"gap-2";"rounded-xl";"bg-slate-50";"p-3")).
attr(weight_grid, order, 5).

elem(wr(I), div, weight_grid) :- weight(I, _, _).
attr(wr(I), class, ("bg-white";"rounded-lg";"px-3";"py-2";"flex";"items-center";"justify-center";"min-w-0";"shadow-sm")) :- weight(I, _, _).
attr(wr(I), order, I) :- weight(I, _, _).

elem(ws(I), text, wr(I)) :- weight(I, _, _).
attr(ws(I), text, V) :- weight(I, V, _).
attr(ws(I), class, C) :- weight(I, _, C).
attr(ws(I), class, ("text-sm";"truncate")) :- weight(I, _, _).
attr(ws(I), order, 1) :- weight(I, _, _).

% COLORS

elem(palette_grid, div, card(colors)).
attr(palette_grid, class, ("grid";"grid-cols-2";"gap-2";"rounded-xl";"bg-slate-50";"p-3")).
attr(palette_grid, order, 3).

elem(sw(I), div, palette_grid) :- palette(I, _, _, _).
attr(sw(I), class, ("flex";"items-center";"justify-center";"px-3";"py-3";"rounded-xl";"text-xs";"font-mono";"font-semibold";"min-w-0";"shadow-sm")) :- palette(I, _, _, _).
attr(sw(I), class, BG) :- palette(I, _, BG, _).
attr(sw(I), order, I) :- palette(I, _, _, _).

elem(sw_lbl(I), text, sw(I)) :- palette(I, _, _, _).
attr(sw_lbl(I), text, V) :- palette(I, V, _, _).
attr(sw_lbl(I), class, TC) :- palette(I, _, _, TC).
attr(sw_lbl(I), class, "truncate") :- palette(I, _, _, _).
attr(sw_lbl(I), order, 1) :- palette(I, _, _, _).

elem(shade_grid, div, card(colors)).
attr(shade_grid, class, ("grid";"grid-cols-5";"gap-2";"rounded-xl";"bg-slate-50";"p-3")).
attr(shade_grid, order, 5).

elem(sh(I), div, shade_grid) :- shade(I, _, _, _).
attr(sh(I), class, ("flex";"items-center";"justify-center";"h-12";"rounded-xl";"shadow-sm";"min-w-0")) :- shade(I, _, _, _).
attr(sh(I), class, BG) :- shade(I, _, BG, _).
attr(sh(I), order, I) :- shade(I, _, _, _).

elem(sh_lbl(I), text, sh(I)) :- shade(I, _, _, _).
attr(sh_lbl(I), text, V) :- shade(I, V, _, _).
attr(sh_lbl(I), class, TC) :- shade(I, _, _, TC).
attr(sh_lbl(I), class, ("text-xs";"font-mono";"font-semibold")) :- shade(I, _, _, _).
attr(sh_lbl(I), order, 1) :- shade(I, _, _, _).

elem(text_grid, div, card(colors)).
attr(text_grid, class, ("grid";"grid-cols-2";"gap-2";"rounded-xl";"bg-slate-50";"p-3")).
attr(text_grid, order, 7).

elem(tc(I), div, text_grid) :- text_color(I, _, _).
attr(tc(I), class, ("bg-white";"rounded-lg";"px-3";"py-2";"min-w-0";"shadow-sm")) :- text_color(I, _, _).
attr(tc(I), order, I) :- text_color(I, _, _).

elem(tc_lbl(I), text, tc(I)) :- text_color(I, _, _).
attr(tc_lbl(I), text, V) :- text_color(I, V, _).
attr(tc_lbl(I), class, C) :- text_color(I, _, C).
attr(tc_lbl(I), class, ("text-sm";"font-mono";"font-semibold";"truncate")) :- text_color(I, _, _).
attr(tc_lbl(I), order, 1) :- text_color(I, _, _).

% BUTTONS

elem(btn_variants, div, card(buttons)).
attr(btn_variants, class, ("flex";"flex-wrap";"items-center";"gap-2";"rounded-xl";"bg-slate-50";"p-3")).
attr(btn_variants, order, 3).

elem(bd(I), button, btn_variants) :- btn_demo(I, _, _, _).
attr(bd(I), text, L) :- btn_demo(I, _, L, _).
attr(bd(I), variant, V) :- btn_demo(I, V, _, _).
attr(bd(I), order, I) :- btn_demo(I, _, _, _).
when(bd(I), click, update, (btn_status, text, L)) :- btn_demo(I, _, L, _).

elem(bd_icon(I), icon, bd(I)) :- btn_demo(I, _, _, Ico).
attr(bd_icon(I), icon, Ico) :- btn_demo(I, _, _, Ico).
attr(bd_icon(I), order, 1) :- btn_demo(I, _, _, _).

elem(btn_sizes, div, card(buttons)).
attr(btn_sizes, class, ("flex";"items-center";"gap-2";"flex-wrap";"rounded-xl";"bg-slate-50";"p-3")).
attr(btn_sizes, order, 5).

elem(bsm, button, btn_sizes).
attr(bsm, text, "Small").
attr(bsm, variant, "outline").
attr(bsm, size, "sm").
attr(bsm, order, 1).

elem(bmd, button, btn_sizes).
attr(bmd, text, "Default").
attr(bmd, variant, "outline").
attr(bmd, order, 2).

elem(blg, button, btn_sizes).
attr(blg, text, "Large").
attr(blg, variant, "outline").
attr(blg, size, "lg").
attr(blg, order, 3).

elem(btn_feedback, div, card(buttons)).
attr(btn_feedback, class, ("flex";"items-center";"gap-2";"text-sm";"text-slate-500";"bg-slate-50";"rounded-xl";"px-3";"py-2")).
attr(btn_feedback, order, 6).

elem(btn_feedback_lbl, text, btn_feedback).
attr(btn_feedback_lbl, text, "Last clicked:").
attr(btn_feedback_lbl, order, 1).

elem(btn_status, text, btn_feedback).
attr(btn_status, text, "—").
attr(btn_status, class, ("font-medium";"text-slate-950")).
attr(btn_status, order, 2).

% RADIUS / BORDERS / SHADOWS / OPACITY

elem(round_grid, div, card(radius)).
attr(round_grid, class, ("grid";"grid-cols-3";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(round_grid, order, 3).

elem(rd(I), div, round_grid) :- rounding(I, _, _, _).
attr(rd(I), class, ("min-w-0")) :- rounding(I, _, _, _).
attr(rd(I), order, I) :- rounding(I, _, _, _).

elem(rd_box(I), div, rd(I)) :- rounding(I, _, _, _).
attr(rd_box(I), class, ("h-16";"w-full";"shadow-sm";"flex";"items-center";"justify-center")) :- rounding(I, _, _, _).
attr(rd_box(I), class, R) :- rounding(I, _, R, _).
attr(rd_box(I), class, Color) :- rounding(I, _, _, Color).
attr(rd_box(I), order, 1) :- rounding(I, _, _, _).

elem(rd_lbl(I), text, rd_box(I)) :- rounding(I, _, _, _).
attr(rd_lbl(I), text, V) :- rounding(I, V, _, _).
attr(rd_lbl(I), class, ("text-[10px]";"font-mono";"font-medium";"text-slate-700";"text-center")) :- rounding(I, _, _, _).
attr(rd_lbl(I), order, 1) :- rounding(I, _, _, _).

elem(border_grid, div, card(borders)).
attr(border_grid, class, ("grid";"grid-cols-4";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(border_grid, order, 3).

elem(brd(I), div, border_grid) :- border_demo(I, _, _).
attr(brd(I), class, ("min-w-0")) :- border_demo(I, _, _).
attr(brd(I), order, I) :- border_demo(I, _, _).

elem(brd_box(I), div, brd(I)) :- border_demo(I, _, _).
attr(brd_box(I), class, ("h-14";"w-full";"bg-white";"rounded-xl";"flex";"items-center";"justify-center";"shadow-sm")) :- border_demo(I, _, _).
attr(brd_box(I), class, B) :- border_demo(I, _, B).
attr(brd_box(I), order, 1) :- border_demo(I, _, _).

elem(brd_lbl(I), text, brd_box(I)) :- border_demo(I, _, _).
attr(brd_lbl(I), text, V) :- border_demo(I, V, _).
attr(brd_lbl(I), class, ("text-[10px]";"font-mono";"font-semibold";"text-slate-950";"text-center";"truncate")) :- border_demo(I, _, _).
attr(brd_lbl(I), order, 1) :- border_demo(I, _, _).

elem(shadow_grid, div, card(shadows)).
attr(shadow_grid, class, ("grid";"grid-cols-3";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(shadow_grid, order, 3).

elem(sd(I), div, shadow_grid) :- shadow_demo(I, _, _).
attr(sd(I), class, ("min-w-0")) :- shadow_demo(I, _, _).
attr(sd(I), order, I) :- shadow_demo(I, _, _).

elem(sd_box(I), div, sd(I)) :- shadow_demo(I, _, _).
attr(sd_box(I), class, ("h-16";"w-full";"bg-white";"rounded-xl";"flex";"items-center";"justify-center")) :- shadow_demo(I, _, _).
attr(sd_box(I), class, S) :- shadow_demo(I, _, S).
attr(sd_box(I), order, 1) :- shadow_demo(I, _, _).

elem(sd_lbl(I), text, sd_box(I)) :- shadow_demo(I, _, _).
attr(sd_lbl(I), text, V) :- shadow_demo(I, V, _).
attr(sd_lbl(I), class, ("text-xs";"font-mono";"font-medium";"text-slate-600";"text-center")) :- shadow_demo(I, _, _).
attr(sd_lbl(I), order, 1) :- shadow_demo(I, _, _).

elem(opacity_row, div, card(opacity)).
attr(opacity_row, class, ("grid";"grid-cols-4";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(opacity_row, order, 3).

elem(op(I), div, opacity_row) :- opacity_demo(I, _, _).
attr(op(I), class, "min-w-0") :- opacity_demo(I, _, _).
attr(op(I), order, I) :- opacity_demo(I, _, _).

elem(op_box(I), div, op(I)) :- opacity_demo(I, _, _).
attr(op_box(I), class, ("h-14";"w-full";"flex";"items-center";"justify-center";"bg-violet-300";"rounded-xl";"shadow-sm")) :- opacity_demo(I, _, _).
attr(op_box(I), class, O) :- opacity_demo(I, _, O).
attr(op_box(I), order, 1) :- opacity_demo(I, _, _).

elem(op_lbl(I), text, op_box(I)) :- opacity_demo(I, _, _).
attr(op_lbl(I), text, V) :- opacity_demo(I, V, _).
attr(op_lbl(I), class, ("text-xs";"font-mono";"font-semibold";"text-violet-950")) :- opacity_demo(I, _, _).
attr(op_lbl(I), order, 1) :- opacity_demo(I, _, _).

% SPACING

elem(padding_rows, div, card(spacing)).
attr(padding_rows, class, ("grid";"grid-cols-4";"gap-3";"bg-slate-50";"rounded-xl";"p-4";"items-start";"overflow-hidden")).
attr(padding_rows, order, 3).

elem(pd(I), div, padding_rows) :- padding_demo(I, _, _).
attr(pd(I), class, ("flex";"flex-col";"items-center";"gap-2";"min-w-0")) :- padding_demo(I, _, _).
attr(pd(I), order, I) :- padding_demo(I, _, _).

elem(pd_val(I), text, pd(I)) :- padding_demo(I, _, _).
attr(pd_val(I), text, V) :- padding_demo(I, V, _).
attr(pd_val(I), class, ("w-8";"h-6";"rounded-md";"bg-slate-100";"flex";"items-center";"justify-center";"text-xs";"font-mono";"font-semibold";"text-slate-500")) :- padding_demo(I, _, _).
attr(pd_val(I), order, 1) :- padding_demo(I, _, _).

elem(pd_pad(I), div, pd(I)) :- padding_demo(I, _, _).
attr(pd_pad(I), class, ("rounded-lg";"bg-violet-100";"shadow-inner";"inline-flex";"items-center";"justify-center";"mx-auto";"shrink-0")) :- padding_demo(I, _, _).
attr(pd_pad(I), class, P) :- padding_demo(I, _, P).
attr(pd_pad(I), order, 2) :- padding_demo(I, _, _).

elem(pd_inner(I), div, pd_pad(I)) :- padding_demo(I, _, _).
attr(pd_inner(I), class, ("bg-violet-300";"rounded-full";"w-3";"h-3";"shadow-sm")) :- padding_demo(I, _, _).
attr(pd_inner(I), order, 1) :- padding_demo(I, _, _).

elem(gap_rows, div, card(spacing)).
attr(gap_rows, class, ("flex";"flex-col";"items-start";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(gap_rows, order, 5).

elem(gp(I), div, gap_rows) :- gap_demo(I, _, _).
attr(gp(I), class, ("flex";"items-center";"bg-white";"rounded-xl";"p-3";"shadow-sm";"w-fit";"min-w-0")) :- gap_demo(I, _, _).
attr(gp(I), class, G) :- gap_demo(I, _, G).
attr(gp(I), order, I) :- gap_demo(I, _, _).

elem(gp_lbl(I), div, gp(I)) :- gap_demo(I, _, _).
attr(gp_lbl(I), class, ("w-10";"h-8";"rounded-md";"bg-slate-100";"flex";"items-center";"justify-center";"shrink-0")) :- gap_demo(I, _, _).
attr(gp_lbl(I), order, 1) :- gap_demo(I, _, _).

elem(gp_lbl_text(I), text, gp_lbl(I)) :- gap_demo(I, _, _).
attr(gp_lbl_text(I), text, V) :- gap_demo(I, V, _).
attr(gp_lbl_text(I), class, ("text-xs";"font-mono";"font-semibold";"text-slate-500")) :- gap_demo(I, _, _).
attr(gp_lbl_text(I), order, 1) :- gap_demo(I, _, _).

elem(gp_dot(I, N), div, gp(I)) :- gap_demo(I, _, _), flex_item(N, _).
attr(gp_dot(I, N), class, ("w-4";"h-4";"rounded-full";"bg-sky-300";"shadow-sm")) :- gap_demo(I, _, _), flex_item(N, _).
attr(gp_dot(I, N), order, O) :- gap_demo(I, _, _), flex_item(N, _), O=N+1.

% LAYOUT

elem(flex_rows, div, card(flex)).
attr(flex_rows, class, ("flex";"flex-col";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(flex_rows, order, 3).

elem(ar(I), div, flex_rows) :- align_row(I, _, _).
attr(ar(I), class, ("flex";"flex-col";"gap-2")) :- align_row(I, _, _).
attr(ar(I), order, I) :- align_row(I, _, _).

elem(ar_lbl(I), text, ar(I)) :- align_row(I, V, _).
attr(ar_lbl(I), text, V) :- align_row(I, V, _).
attr(ar_lbl(I), class, ("text-xs";"font-mono";"text-slate-500")) :- align_row(I, _, _).
attr(ar_lbl(I), order, 1) :- align_row(I, _, _).

elem(ar_track(I), div, ar(I)) :- align_row(I, _, _).
attr(ar_track(I), class, ("flex";"flex-row";"items-center";"gap-2";"w-full";"h-14";"bg-white";"rounded-xl";"p-2";"shadow-sm")) :- align_row(I, _, _).
attr(ar_track(I), class, JC) :- align_row(I, _, JC).
attr(ar_track(I), order, 2) :- align_row(I, _, _).

elem(ar_item(I, N), div, ar_track(I)) :- align_row(I, _, _), flex_item(N, _).
attr(ar_item(I, N), class, ("w-9";"h-9";"rounded-md";"bg-sky-300";"flex";"items-center";"justify-center";"shrink-0")) :- align_row(I, _, _), flex_item(N, _).
attr(ar_item(I, N), order, N) :- align_row(I, _, _), flex_item(N, _).

elem(ar_item_lbl(I, N), text, ar_item(I, N)) :- align_row(I, _, _), flex_item(N, _).
attr(ar_item_lbl(I, N), text, L) :- align_row(I, _, _), flex_item(N, L).
attr(ar_item_lbl(I, N), class, ("text-xs";"font-bold";"text-sky-950")) :- align_row(I, _, _), flex_item(N, _).
attr(ar_item_lbl(I, N), order, 1) :- align_row(I, _, _), flex_item(N, _).

elem(grid_variants, div, card(grid)).
attr(grid_variants, class, ("flex";"flex-col";"gap-2";"bg-slate-50";"rounded-xl";"p-4")).
attr(grid_variants, order, 3).

elem(gv(I), div, grid_variants) :- grid_variant(I, _, _).
attr(gv(I), class, ("flex";"flex-col";"gap-1")) :- grid_variant(I, _, _).
attr(gv(I), order, I) :- grid_variant(I, _, _).

elem(gv_lbl(I), text, gv(I)) :- grid_variant(I, V, _).
attr(gv_lbl(I), text, V) :- grid_variant(I, V, _).
attr(gv_lbl(I), class, ("text-xs";"font-mono";"text-slate-500")) :- grid_variant(I, _, _).
attr(gv_lbl(I), order, 1) :- grid_variant(I, _, _).

elem(gv_grid(I), div, gv(I)) :- grid_variant(I, _, _).
attr(gv_grid(I), class, ("grid";"gap-2";"w-full";"bg-white";"rounded-xl";"p-2";"shadow-sm")) :- grid_variant(I, _, _).
attr(gv_grid(I), class, C) :- grid_variant(I, _, C).
attr(gv_grid(I), order, 2) :- grid_variant(I, _, _).

elem(gc(I, N), div, gv_grid(I)) :- grid_variant(I, _, _), grid_cell(N).
attr(gc(I, N), class, ("h-7";"bg-slate-300";"border";"border-slate-300";"rounded-md";"shadow-inner")) :- grid_variant(I, _, _), grid_cell(N).
attr(gc(I, N), order, N) :- grid_variant(I, _, _), grid_cell(N).

elem(span_demo, div, card(grid)).
attr(span_demo, class, ("flex";"flex-col";"gap-2";"bg-slate-50";"rounded-xl";"p-4")).
attr(span_demo, order, 5).

elem(span_track(R), div, span_demo) :- span_demo_cell(R, _, _, _, _, _, _).
attr(span_track(R), class, ("grid";"grid-cols-4";"gap-2";"bg-white";"rounded-xl";"p-3";"shadow-sm")) :- span_demo_cell(R, _, _, _, _, _, _).
attr(span_track(R), order, R) :- span_demo_cell(R, _, _, _, _, _, _).

elem(span_cell(R, N), div, span_track(R)) :- span_demo_cell(R, N, _, _, _, _, _).
attr(span_cell(R, N), class, ("h-7";"rounded-lg";"flex";"items-center";"justify-center";"shadow-sm")) :- span_demo_cell(R, N, _, _, _, _, _).
attr(span_cell(R, N), class, Span) :- span_demo_cell(R, N, _, Span, _, _, _), Span!="".
attr(span_cell(R, N), class, Bg) :- span_demo_cell(R, N, _, _, Bg, _, _).
attr(span_cell(R, N), class, Text) :- span_demo_cell(R, N, _, _, _, Text, _).
attr(span_cell(R, N), class, Order) :- span_demo_cell(R, N, _, _, _, _, Order).

elem(span_cell_lbl(R, N), text, span_cell(R, N)) :- span_demo_cell(R, N, L, _, _, _, _), L!="".
attr(span_cell_lbl(R, N), text, L) :- span_demo_cell(R, N, L, _, _, _, _), L!="".
attr(span_cell_lbl(R, N), class, ("text-[10px]";"font-semibold";"font-mono")) :- span_demo_cell(R, N, L, _, _, _, _), L!="".
attr(span_cell_lbl(R, N), order, 1) :- span_demo_cell(R, N, L, _, _, _, _), L!="".

elem(width_rows, div, card(width)).
attr(width_rows, class, ("flex";"flex-col";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(width_rows, order, 3).

elem(wd(I), div, width_rows) :- width_demo(I, _, _).
attr(wd(I), class, ("flex";"flex-col";"gap-2")) :- width_demo(I, _, _).
attr(wd(I), order, I) :- width_demo(I, _, _).

elem(wd_track(I), div, wd(I)) :- width_demo(I, _, _).
attr(wd_track(I), class, ("w-full";"h-10";"bg-white";"rounded-full";"overflow-hidden";"p-1";"shadow-sm")) :- width_demo(I, _, _).
attr(wd_track(I), order, 1) :- width_demo(I, _, _).

elem(wd_bar(I), div, wd_track(I)) :- width_demo(I, _, _).
attr(wd_bar(I), class, ("h-full";"bg-sky-300";"rounded-full";"flex";"items-center";"justify-center";"min-w-12";"shadow-sm")) :- width_demo(I, _, _).
attr(wd_bar(I), class, W) :- width_demo(I, _, W).
attr(wd_bar(I), order, 1) :- width_demo(I, _, _).

elem(wd_lbl(I), text, wd_bar(I)) :- width_demo(I, _, _).
attr(wd_lbl(I), text, V) :- width_demo(I, V, _).
attr(wd_lbl(I), class, ("text-xs";"font-mono";"font-semibold";"text-sky-950")) :- width_demo(I, _, _).
attr(wd_lbl(I), order, 1) :- width_demo(I, _, _).



elem(checkbox_rows, div, card(checkbox)).
attr(checkbox_rows, class, ("flex";"flex-col";"gap-3";"bg-slate-50";"rounded-xl";"p-4")).
attr(checkbox_rows, order, 3).

elem(cb_row(I), div, checkbox_rows) :- checkbox_demo(I, _, _).
attr(cb_row(I), class, ("flex";"items-center";"gap-2")) :- checkbox_demo(I, _, _).
attr(cb_row(I), order, I) :- checkbox_demo(I, _, _).

elem(cb(I), checkbox, cb_row(I)) :- checkbox_demo(I, _, _).
attr(cb(I), order, 1) :- checkbox_demo(I, _, _).

attr(cb(I), checked, true) :- checkbox_demo(I, "checked", _).
attr(cb(I), disabled, true) :- checkbox_demo(I, "disabled", _).
attr(cb(I), indeterminate, true) :- checkbox_demo(I, "indeterminate", _).

elem(cb_lbl(I), text, cb_row(I)) :- checkbox_demo(I, _, _).
attr(cb_lbl(I), text, L) :- checkbox_demo(I, _, L).
attr(cb_lbl(I), class, ("text-sm";"text-slate-950")) :- checkbox_demo(I, _, _).
attr(cb_lbl(I), order, 2) :- checkbox_demo(I, _, _).



elem(field_set_demo, field(set), card(field)).
attr(field_set_demo, class, ("bg-slate-50";"rounded-xl";"p-4")).
attr(field_set_demo, order, 4).

elem(field_legend_demo, field(legend), field_set_demo).
attr(field_legend_demo, text, "Account").
attr(field_legend_demo, variant, "legend").
attr(field_legend_demo, order, 1).

elem(field_set_group, field(group), field_set_demo).
attr(field_set_group, order, 2).

% vertical field: label + description + input-ish placeholder
elem(fld_vertical, field, field_set_group).
attr(fld_vertical, orientation, "vertical").
attr(fld_vertical, order, 1).

elem(fld_v_label, field(label), fld_vertical).
attr(fld_v_label, text, "Username").
attr(fld_v_label, for, "fld_v_input").
attr(fld_v_label, order, 1).

elem(fld_v_input, input, fld_vertical).
attr(fld_v_input, id, "fld_v_input").
attr(fld_v_input, placeholder, "e.g. mariia").
attr(fld_v_input, order, 2).

elem(fld_v_desc, field(description), fld_vertical).
attr(fld_v_desc, text, "Shown on your public profile.").
attr(fld_v_desc, order, 3).

% horizontal field: label beside control
elem(fld_horizontal, field, field_set_group).
attr(fld_horizontal, orientation, "horizontal").
attr(fld_horizontal, order, 2).
attr(fld_horizontal, class, ("border-t";"border-slate-200";"pt-3")).

elem(fld_h_check, checkbox, fld_horizontal).
attr(fld_h_check, checked, true).
attr(fld_h_check, order, 1).

elem(fld_h_label, field(label), fld_horizontal).
attr(fld_h_label, text, "Enable notifications").
attr(fld_h_label, order, 2).

elem(field_group_demo, field(group), card(field)).
attr(field_group_demo, class, ("bg-slate-50";"rounded-xl";"p-4")).
attr(field_group_demo, order, 7).

elem(fld_invalid, field, field_group_demo).
attr(fld_invalid, orientation, "vertical").
attr(fld_invalid, order, 1).

elem(fld_i_label, field(label), fld_invalid).
attr(fld_i_label, text, "Email").
attr(fld_i_label, for, "fld_i_input").
attr(fld_i_label, order, 1).

elem(fld_i_input, input, fld_invalid).
attr(fld_i_input, id, "fld_i_input").
attr(fld_i_input, type, "email").
attr(fld_i_input, placeholder, "you@example.com").
attr(fld_i_input, order, 2).

% error hidden until submit
elem(fld_i_error, field(error), fld_invalid).
attr(fld_i_error, text, "Enter a valid email address.").
attr(fld_i_error, class, "hidden").
attr(fld_i_error, order, 3).

% submit reveals the error state (static demo — no real validation)
elem(fld_submit, button, field_group_demo).
attr(fld_submit, text, "Submit").
attr(fld_submit, variant, "outline").
attr(fld_submit, class, ("mt-3";"w-fit")).
attr(fld_submit, order, 2).
when(fld_submit, click, update, (fld_invalid, class, "text-destructive")).
when(fld_submit, click, update, (fld_i_error, class, "")).

% THEME TOKENS

elem(theme_toolbar, div, card(theme)).
attr(theme_toolbar, class, ("flex";"items-center";"justify-between";"gap-3";"rounded-xl";"border";"border-border";"bg-background";"p-3")).
attr(theme_toolbar, order, 3).

elem(theme_hint, p, theme_toolbar).
attr(theme_hint, text, "Toggle the theme to see semantic colors adapt.").
attr(theme_hint, class, ("text-sm";"text-muted-foreground")).
attr(theme_hint, order, 1).

elem(theme_switch, theme_toggle, theme_toolbar).
attr(theme_switch, variant, "outline").
attr(theme_switch, size, "icon").
attr(theme_switch, order, 2).

elem(theme_grid, div, card(theme)).
attr(theme_grid, class, ("grid";"grid-cols-2";"gap-2")).
attr(theme_grid, order, 4).

elem(theme_swatch(I), div, theme_grid) :- theme_token(I, _, _).
attr(theme_swatch(I), class, ("flex";"min-h-16";"items-end";"rounded-xl";"border";"p-3";"shadow-xs")) :- theme_token(I, _, _).
attr(theme_swatch(I), class, C) :- theme_token(I, _, C).
attr(theme_swatch(I), order, I) :- theme_token(I, _, _).

elem(theme_swatch_label(I), span, theme_swatch(I)) :- theme_token(I, _, _).
attr(theme_swatch_label(I), text, L) :- theme_token(I, L, _).
attr(theme_swatch_label(I), class, ("text-xs";"font-mono";"font-semibold")) :- theme_token(I, _, _).
attr(theme_swatch_label(I), order, 1) :- theme_token(I, _, _).

% CONTROL STATES

elem(state_grid, div, card(states)).
attr(state_grid, class, ("grid";"grid-cols-2";"gap-3";"rounded-xl";"bg-muted/40";"p-4")).
attr(state_grid, order, 3).

elem(state_demo(I), div, state_grid) :- control_state(I, _, _, _, _, _).
attr(state_demo(I), class, ("flex";"min-w-0";"flex-col";"gap-2")) :- control_state(I, _, _, _, _, _).
attr(state_demo(I), order, I) :- control_state(I, _, _, _, _, _).

elem(state_label(I), span, state_demo(I)) :- control_state(I, _, _, _, _, _).
attr(state_label(I), text, L) :- control_state(I, L, _, _, _, _).
attr(state_label(I), class, ("text-xs";"font-mono";"text-muted-foreground";"truncate")) :- control_state(I, _, _, _, _, _).
attr(state_label(I), order, 1) :- control_state(I, _, _, _, _, _).

elem(state_button(I), button, state_demo(I)) :- control_state(I, _, _, _, _, _).
attr(state_button(I), text, T) :- control_state(I, _, T, _, _, _).
attr(state_button(I), variant, V) :- control_state(I, _, _, V, _, _).
attr(state_button(I), class, C) :- control_state(I, _, _, _, C, _), C!="".
attr(state_button(I), disabled, true) :- control_state(I, _, _, _, _, true).
attr(state_button(I), order, 2) :- control_state(I, _, _, _, _, _).

elem(state_loading_spinner, spinner, state_button(6)).
attr(state_loading_spinner, class, "size-4").
attr(state_loading_spinner, order, 1).

% FORM CONTROLS

elem(form_showcase, field(group), card(forms)).
attr(form_showcase, class, ("rounded-xl";"border";"border-border";"bg-muted/40";"p-4")).
attr(form_showcase, order, 3).

elem(form_name, field, form_showcase).
attr(form_name, orientation, "vertical").
attr(form_name, order, 1).

elem(form_name_label, field(label), form_name).
attr(form_name_label, text, "Display name").
attr(form_name_label, for, "showcase-name").
attr(form_name_label, order, 1).

elem(form_name_input, input, form_name).
attr(form_name_input, id, "showcase-name").
attr(form_name_input, name, "display_name").
attr(form_name_input, placeholder, "Ada Lovelace").
attr(form_name_input, order, 2).

elem(form_name_description, field(description), form_name).
attr(form_name_description, text, "A standard text input with focus styling.").
attr(form_name_description, order, 3).

elem(form_bio, field, form_showcase).
attr(form_bio, orientation, "vertical").
attr(form_bio, order, 2).

elem(form_bio_label, field(label), form_bio).
attr(form_bio_label, text, "Bio").
attr(form_bio_label, for, "showcase-bio").
attr(form_bio_label, order, 1).

elem(form_bio_input, textarea, form_bio).
attr(form_bio_input, id, "showcase-bio").
attr(form_bio_input, name, "bio").
attr(form_bio_input, placeholder, "Tell us a little about yourself…").
attr(form_bio_input, rows, 3).
attr(form_bio_input, order, 2).

elem(form_density, field, form_showcase).
attr(form_density, orientation, "vertical").
attr(form_density, order, 3).

elem(form_density_label, field(label), form_density).
attr(form_density_label, text, "Interface density").
attr(form_density_label, for, "showcase-density").
attr(form_density_label, order, 1).

elem(form_density_select, select, form_density).
attr(form_density_select, type, "single").
attr(form_density_select, value, "comfortable").
attr(form_density_select, name, "density").
attr(form_density_select, order, 2).

elem(form_density_trigger, select(trigger), form_density_select).
attr(form_density_trigger, id, "showcase-density").
attr(form_density_trigger, text, "Comfortable").
attr(form_density_trigger, class, "w-full").
attr(form_density_trigger, order, 1).

elem(form_density_content, select(content), form_density_select).
attr(form_density_content, order, 2).

elem(form_density_item(I), select(item), form_density_content) :- select_option(I, _, _).
attr(form_density_item(I), text, L) :- select_option(I, _, L).
attr(form_density_item(I), value, V) :- select_option(I, V, _).
attr(form_density_item(I), order, I) :- select_option(I, _, _).
when(form_density_item(I), click, update, (form_density_trigger, text, L)) :- select_option(I, _, L).

elem(form_disabled, field, form_showcase).
attr(form_disabled, orientation, "vertical").
attr(form_disabled, order, 4).

elem(form_disabled_label, field(label), form_disabled).
attr(form_disabled_label, text, "Generated identifier").
attr(form_disabled_label, for, "showcase-id").
attr(form_disabled_label, order, 1).

elem(form_disabled_input, input, form_disabled).
attr(form_disabled_input, id, "showcase-id").
attr(form_disabled_input, value, "usr_01J8K4").
attr(form_disabled_input, disabled, true).
attr(form_disabled_input, order, 2).

% FEEDBACK AND LOADING

elem(feedback_alerts, div, card(feedback)).
attr(feedback_alerts, class, ("flex";"flex-col";"gap-3")).
attr(feedback_alerts, order, 3).

elem(feedback_info, alert, feedback_alerts).
attr(feedback_info, order, 1).

elem(feedback_info_icon, icon, feedback_info).
attr(feedback_info_icon, icon, "Info").
attr(feedback_info_icon, order, 1).

elem(feedback_info_title, alert(title), feedback_info).
attr(feedback_info_title, text, "Settings saved").
attr(feedback_info_title, order, 2).

elem(feedback_info_description, alert(description), feedback_info).
attr(feedback_info_description, text, "Your preferences are available on every device.").
attr(feedback_info_description, order, 3).

elem(feedback_error, alert, feedback_alerts).
attr(feedback_error, variant, "destructive").
attr(feedback_error, order, 2).

elem(feedback_error_icon, icon, feedback_error).
attr(feedback_error_icon, icon, "CircleAlert").
attr(feedback_error_icon, order, 1).

elem(feedback_error_title, alert(title), feedback_error).
attr(feedback_error_title, text, "Could not connect").
attr(feedback_error_title, order, 2).

elem(feedback_error_description, alert(description), feedback_error).
attr(feedback_error_description, text, "Check the server and try again.").
attr(feedback_error_description, order, 3).

elem(loading_preview, div, card(feedback)).
attr(loading_preview, class, ("flex";"flex-col";"gap-4";"rounded-xl";"border";"border-border";"bg-muted/40";"p-4")).
attr(loading_preview, order, 4).

elem(skeleton_row, div, loading_preview).
attr(skeleton_row, class, ("flex";"items-center";"gap-3")).
attr(skeleton_row, order, 1).

elem(skeleton_avatar, skeleton, skeleton_row).
attr(skeleton_avatar, class, ("size-10";"shrink-0";"rounded-full")).
attr(skeleton_avatar, order, 1).

elem(skeleton_lines, div, skeleton_row).
attr(skeleton_lines, class, ("flex";"min-w-0";"flex-1";"flex-col";"gap-2")).
attr(skeleton_lines, order, 2).

elem(skeleton_line_primary, skeleton, skeleton_lines).
attr(skeleton_line_primary, class, ("h-3";"w-3/4")).
attr(skeleton_line_primary, order, 1).

elem(skeleton_line_secondary, skeleton, skeleton_lines).
attr(skeleton_line_secondary, class, ("h-3";"w-1/2")).
attr(skeleton_line_secondary, order, 2).

elem(spinner_row, div, loading_preview).
attr(spinner_row, class, ("flex";"items-center";"gap-4";"border-t";"border-border";"pt-4";"text-sm";"text-muted-foreground")).
attr(spinner_row, order, 2).

elem(spinner_small, spinner, spinner_row).
attr(spinner_small, class, "size-4").
attr(spinner_small, order, 1).

elem(spinner_large, spinner, spinner_row).
attr(spinner_large, class, ("size-7";"text-primary")).
attr(spinner_large, order, 2).

elem(spinner_label, span, spinner_row).
attr(spinner_label, text, "Loading states").
attr(spinner_label, order, 3).
