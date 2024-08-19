elem(people, container, w).

elem(person(P), button, people):- person(P,_).
attr(person(P), label, P):- person(P,_).
attr(person(P), class, ("disabled";"m-2";"btn-sm")):- person(P,_).
attr(person(P), class, ("btn-outline-secondary")):- person(P,cat).
attr(person(P), class, ("btn-outline-warning")):- person(P,dog).
attr(person(P), icon, @concat("","fa-",O)):- person(P,O).

elem(add_person, button, people).
attr(add_person, label, "Add person").
attr(add_person, icon, "fa-user-plus").
attr(add_person, class, ("btn-info";"m-2")).
when(add_person, click, update, (add_modal, visibility, shown)).

elem(add_modal, modal, w).
attr(add_modal, title, "Add person").
elem(modal_content, container, add_modal).
attr(modal_content, class, ("d-flex";"flex-column")).

elem(name_tf, textfield, modal_content).
attr(name_tf, placeholder, "Enter the name").
attr(name_tf, order, 1).
attr(name_tf, width, 250).
when(name_tf, input, context, (name, _value)).

elem(btns_container, container, modal_content).
attr(btns_container, class, ("d-flex";"flex-row";"justify-content-end")).
attr(btns_container, order, 2).

pet(cat;dog).
elem(add_btn(O), button, btns_container):- pet(O).
attr(add_btn(O), label, "Add"):- pet(O).
attr(add_btn(cat), class, ("m-1";"btn-secondary";"ml-auto")):- pet(O).
attr(add_btn(dog), class, ("m-1";"btn-warning";"ml-auto")):- pet(O).
attr(add_btn(O), icon, @concat("","fa-",O)):- pet(O).
when(add_btn(O), click, context, (pet, O)):- pet(O).
when(add_btn(O), click, call,
     add_atom(person(_context_value(name,str), _context_value(pet)))):- pet(O).
