elem(sb, sidebar, window).

elem(f, form, sb).

elem(name, text_field, f). 
attr(name, label, "Name").
attr(name, required, true). % Used by the parent form
when(tf, input, context, (name,_value)). % Maybe this is added automatically for all text_field

elem(last_name, text_field, f).
attr(tf, label, "Last name").
attr(last_name, required, true).
when(last_name, input, context, (last_name,_value)).

elem(gender, dropdown_menu, f).
attr(gender, label, "Gender").
attr(gender, required, true).

elem(gender_m, dropdown_menu_item, gender).
attr(gender_m, label, "He").
when(gender_m, click, context, (gender,he)).

elem(gender_w, dropdown_menu_item, gender).
attr(gender_w, label, "She").
when(gender_w, click, context, (gender,she)).

elem(gender_nb, dropdown_menu_item, gender).
attr(gender_nb, label, "They").
when(gender_nb, click, context, (gender,they)).

elem(add, submmit_button, f).
attr(add, label, "Add person").
% No need of special user input
when(add, click, call, add_atom(person(_name,_last_name,_gender))). %Checks that required fields have a value and then calls the method

