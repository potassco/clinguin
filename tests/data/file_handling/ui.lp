% ---------------------------------------------------------------------------
% Derived file state
% ---------------------------------------------------------------------------

available_file(F) :- _clinguin_optional_file(F).
configured_file(F) :- available_file(F), not _clinguin_file_content(F, _).
uploaded_file(F) :- _clinguin_file_content(F, _).
active_file(F) :- _clinguin_active_file(F).

has_configured_file :- configured_file(_).
has_uploaded_file :- uploaded_file(_).
has_description(F) :- file_description(F, _).

file_parent(F, configured_files) :- configured_file(F).
file_parent(F, uploaded_files) :- uploaded_file(F).

% ---------------------------------------------------------------------------
% Page
% ---------------------------------------------------------------------------

elem(app, div, root).
attr(app, class, ("mx-auto"; "flex"; "max-w-3xl"; "flex-col"; "gap-6"; "p-6")).

elem(title, text, app).
attr(title, text, "File handling test").
attr(title, class, ("text-2xl"; "font-bold")).
attr(title, order, 1).

% ---------------------------------------------------------------------------
% Upload
% ---------------------------------------------------------------------------

elem(upload_section, div, app).
attr(upload_section, class, ("flex"; "flex-col"; "gap-2")).
attr(upload_section, order, 2).

elem(upload_title, text, upload_section).
attr(upload_title, text, "Upload a file").
attr(upload_title, class, ("text-lg"; "font-semibold")).
attr(upload_title, order, 1).

elem(upload_form, form, upload_section).
attr(upload_form, class, ("flex"; "items-center"; "gap-2")).
attr(upload_form, order, 2).

when(upload_form, submit, call, update).

elem(file_input, input, upload_form).
attr(file_input, type, "file").
attr(file_input, name, "uploaded_file").
attr(file_input, accept, ".lp").
attr(file_input, required, true).
attr(file_input, order, 1).

elem(upload_button, button, upload_form).
attr(upload_button, type, "submit").
attr(upload_button, text, "Upload").
attr(upload_button, order, 2).

% ---------------------------------------------------------------------------
% Configured optional files
% ---------------------------------------------------------------------------

elem(configured_section, div, app).
attr(configured_section, class, ("flex"; "flex-col"; "gap-3")).
attr(configured_section, order, 3).

elem(configured_title, text, configured_section).
attr(configured_title, text, "Configured optional files").
attr(configured_title, class, ("text-lg"; "font-semibold")).
attr(configured_title, order, 1).

elem(configured_files, div, configured_section).
attr(configured_files, class, ("flex"; "flex-col"; "gap-3")).
attr(configured_files, order, 2).

elem(no_configured_files, text, configured_files) :- not has_configured_file.
attr(no_configured_files, text, "No files supplied with --optional-files.") :- not has_configured_file.
attr(no_configured_files, class, "text-muted-foreground") :- not has_configured_file.

% ---------------------------------------------------------------------------
% Uploaded files
% ---------------------------------------------------------------------------

elem(uploaded_section, div, app).
attr(uploaded_section, class, ("flex"; "flex-col"; "gap-3")).
attr(uploaded_section, order, 4).

elem(uploaded_title, text, uploaded_section).
attr(uploaded_title, text, "Uploaded files").
attr(uploaded_title, class, ("text-lg"; "font-semibold")).
attr(uploaded_title, order, 1).

elem(uploaded_files, div, uploaded_section).
attr(uploaded_files, class, ("flex"; "flex-col"; "gap-3")).
attr(uploaded_files, order, 2).

elem(no_uploaded_files, text, uploaded_files) :- not has_uploaded_file.
attr(no_uploaded_files, text, "No files uploaded.") :- not has_uploaded_file.
attr(no_uploaded_files, class, "text-muted-foreground") :- not has_uploaded_file.

% ---------------------------------------------------------------------------
% Shared file card
% ---------------------------------------------------------------------------

elem(file_card(F), div, Parent) :- file_parent(F, Parent).
attr(file_card(F), class, ("flex"; "flex-col"; "gap-2"; "rounded-md"; "border"; "p-3")) :- available_file(F).

elem(file_header(F), div, file_card(F)) :- available_file(F).
attr(file_header(F), class, ("flex"; "items-center"; "justify-between"; "gap-2")) :- available_file(F).
attr(file_header(F), order, 1) :- available_file(F).

elem(file_name(F), text, file_header(F)) :- available_file(F).
attr(file_name(F), text, F) :- available_file(F).
attr(file_name(F), class, "font-semibold") :- available_file(F).
attr(file_name(F), order, 1) :- available_file(F).

elem(file_status(F), text, file_header(F)) :- available_file(F).
attr(file_status(F), text, "Active") :- active_file(F).
attr(file_status(F), text, "Inactive") :- available_file(F), not active_file(F).
attr(file_status(F), order, 2) :- available_file(F).

% ---------------------------------------------------------------------------
% Actions
% ---------------------------------------------------------------------------

elem(file_actions(F), div, file_card(F)) :- available_file(F).
attr(file_actions(F), class, ("flex"; "gap-2")) :- available_file(F).
attr(file_actions(F), order, 2) :- available_file(F).

elem(toggle_file(F), button, file_actions(F)) :- available_file(F).

attr(toggle_file(F), text, "Activate") :- available_file(F), not active_file(F).
attr(toggle_file(F), text, "Deactivate") :- active_file(F).

when(toggle_file(F), click, call, activate_file(F)) :- available_file(F), not active_file(F).
when(toggle_file(F), click, call, deactivate_file(F)) :- active_file(F).

elem(remove_file_button(F), button, file_actions(F)) :- available_file(F).
attr(remove_file_button(F), text, "Remove") :- available_file(F).
attr(remove_file_button(F), variant, "destructive") :- available_file(F).

when(remove_file_button(F), click, call, remove_file(F)) :- available_file(F).

% ---------------------------------------------------------------------------
% Content display
% ---------------------------------------------------------------------------

% Uploaded content is available even while the file is inactive.
elem(raw_content(F), text, file_card(F)) :- uploaded_file(F).
attr(raw_content(F), text, Content) :- _clinguin_file_content(F, Content).
attr(raw_content(F), class, ("whitespace-pre-line"; "rounded"; "bg-muted"; "p-2"; "font-mono"; "text-sm")) :- uploaded_file(F).
attr(raw_content(F), order, 3) :- uploaded_file(F).

% Once a valid file is activated, its ASP fact becomes domain state.
elem(description(F), text, file_card(F)) :- active_file(F), file_description(F, _).
attr(description(F), text, @format("Loaded description: {}", Description)) :- active_file(F), file_description(F, Description).
attr(description(F), order, 4) :- active_file(F), file_description(F, _).

elem(missing_description(F), text, file_card(F)) :- active_file(F), not has_description(F).
attr(missing_description(F), text, "The active file does not define file_description/2.") :- active_file(F), not has_description(F).
attr(missing_description(F), class, "text-muted-foreground") :- active_file(F), not has_description(F).
attr(missing_description(F), order, 4) :- active_file(F), not has_description(F).

% ---------------------------------------------------------------------------
% Reset
% ---------------------------------------------------------------------------

elem(reset_button, button, app).
attr(reset_button, text, "Reset to initial state").
attr(reset_button, variant, "outline").
attr(reset_button, class, "w-fit").
attr(reset_button, order, 5).

when(reset_button, click, call, restart).
