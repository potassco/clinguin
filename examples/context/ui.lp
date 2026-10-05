pet(cat, 1).
pet(dog, 2).
pet(none, 3).

elem(w, div, root).
elem(main, div, w).
attr(main, class, ("flex";"flex-col";"gap-8";"p-6";"max-w-xl")).

elem(person_form, form, main).
attr(person_form, order, 1).
when(person_form, submit, call, add_atom(person(_context_value(name, "Anonymous"), _context_value(age, 0), _context_value(pet, none)))).

elem(person_fields, field(set), person_form).

elem(person_legend, field(legend), person_fields).
attr(person_legend, text, "Add a person").
attr(person_legend, order, 1).

elem(person_group, field(group), person_fields).
attr(person_group, order, 2).

input(name, "Name", 1).
input(age, "Age", 2).

elem(field(X), field, person_group) :- input(X, _, _).
attr(field(X), order, O) :- input(X, _, O).

elem(label(X), field(label), field(X)) :- input(X, _, _).
attr(label(X), text, Label) :- input(X, Label, _).
attr(label(X), for, X) :- input(X, _, _).
attr(label(X), order, 1) :- input(X, _, _).

elem(X, input, field(X)) :- input(X, _, _).
attr(X, name, X) :- input(X, _, _).
attr(X, order, 2) :- input(X, _, _).

attr(name, placeholder, "Anonymous").
attr(age, type, "number").
attr(age, min, 0).

elem(pet_field, field, person_group).
attr(pet_field, orientation, "horizontal").
attr(pet_field, order, 3).

elem(pet_title, field(title), pet_field).
attr(pet_title, text, "Pet").
attr(pet_title, order, 1).

elem(pet_dropdown, dropdown_menu, pet_field).
attr(pet_dropdown, order, 2).

elem(pet_trigger, dropdown_menu(trigger), pet_dropdown).
attr(pet_trigger, text, "Choose…").

elem(pet_menu, dropdown_menu(content), pet_dropdown).

elem(pet_item(P), dropdown_menu(item), pet_menu) :- pet(P, _).
attr(pet_item(P), text, P) :- pet(P, _).
attr(pet_item(P), order, O) :- pet(P, O).
when(pet_item(P), click, context, (pet, P)) :- pet(P, _).
when(pet_item(P), click, update, (pet_trigger, text, P)) :- pet(P, _).

elem(add_person, button, person_group).
attr(add_person, type, "submit").
attr(add_person, text, "Add person").
attr(add_person, class, "w-fit").
attr(add_person, order, 4).

% ---------- People ----------

elem(people_section, div, main).
attr(people_section, order, 2).
attr(people_section, class, ("flex";"flex-col";"gap-2")).

elem(people_title, text, people_section).
attr(people_title, text, "People").
attr(people_title, class, ("text-lg";"font-semibold")).
attr(people_title, order, 1).

elem(person_text(N, A, P), text, people_section) :- person(N, A, P).
attr(person_text(N, A, P), text, @format("{}, {} years, pet: {}, adult", N, A, P)) :- person(N, A, P), adult(N).
attr(person_text(N, A, P), text, @format("{}, {} years, pet: {}", N, A, P)) :- person(N, A, P), not adult(N).
attr(person_text(N, A, P), order, A + 2) :- person(N, A, P).

elem(no_people, text, people_section) :- not person(_, _, _).
attr(no_people, text, "No people yet.") :- not person(_, _, _).
attr(no_people, class, ("text-sm";"text-muted-foreground")) :- not person(_, _, _).
attr(no_people, order, 2) :- not person(_, _, _).

% ---------- File context ----------

elem(files_section, div, main).
attr(files_section, order, 3).
attr(files_section, class, ("flex";"flex-col";"gap-3")).

elem(files_title, text, files_section).
attr(files_title, text, "Instance files").
attr(files_title, class, ("text-lg";"font-semibold")).
attr(files_title, order, 1).

elem(file_form, form, files_section).
attr(file_form, order, 2).
attr(file_form, class, ("flex";"items-center";"gap-2")).
when(file_form, submit, call, activate_file(_context_value(instance))).

elem(file_input, input, file_form).
attr(file_input, type, "file").
attr(file_input, name, "instance").
attr(file_input, accept, ".lp").
attr(file_input, required, true).
attr(file_input, order, 1).

elem(upload_file, button, file_form).
attr(upload_file, type, "submit").
attr(upload_file, text, "Upload and activate").
attr(upload_file, order, 2).

% ---------- Uploaded files ----------

elem(file_box(N), div, files_section) :- _clinguin_file_content(N, _).
attr(file_box(N), order, 3) :- _clinguin_file_content(N, _).
attr(file_box(N), class, ("flex";"flex-col";"gap-2";"border";"rounded-md";"p-3")) :- _clinguin_file_content(N, _).

elem(file_header(N), div, file_box(N)) :- _clinguin_file_content(N, _).
attr(file_header(N), order, 1) :- _clinguin_file_content(N, _).
attr(file_header(N), class, ("flex";"items-center";"justify-between";"gap-2")) :- _clinguin_file_content(N, _).

elem(file_name(N), text, file_header(N)) :- _clinguin_file_content(N, _).
attr(file_name(N), text, N) :- _clinguin_file_content(N, _).
attr(file_name(N), class, "font-semibold") :- _clinguin_file_content(N, _).
attr(file_name(N), order, 1) :- _clinguin_file_content(N, _).

elem(file_toggle(N), button, file_header(N)) :- _clinguin_file_content(N, _).
attr(file_toggle(N), size, "sm") :- _clinguin_file_content(N, _).
attr(file_toggle(N), order, 2) :- _clinguin_file_content(N, _).
attr(file_toggle(N), text, "Deactivate") :- _clinguin_active_file(N).
attr(file_toggle(N), variant, "outline") :- _clinguin_active_file(N).
attr(file_toggle(N), text, "Activate") :- _clinguin_file_content(N, _), not _clinguin_active_file(N).
when(file_toggle(N), click, call, deactivate_file(N)) :- _clinguin_active_file(N).
when(file_toggle(N), click, call, activate_file(N)) :- _clinguin_file_content(N, _), not _clinguin_active_file(N).

elem(file_content(N), text, file_box(N)) :- _clinguin_file_content(N, _).
attr(file_content(N), text, Content) :- _clinguin_file_content(N, Content).
attr(file_content(N), class, ("whitespace-pre-line";"font-mono";"text-sm";"bg-muted";"rounded";"p-2")) :- _clinguin_file_content(N, _).
attr(file_content(N), order, 2) :- _clinguin_file_content(N, _).
