% ============================================================================
% # CLINGUIN UI QUICK START
%
% 1. Include the templates you want to use. (all included by default)
% 2. Customize each enabled template in its own file or just overwrite it here.
% 3. Write your application UI below "APPLICATION UI".
% ============================================================================


% ==============================================================================
% ## TEMPLATES
%
% Uncomment the templates you want to use and customize them as needed.
% Further customization can be done in their respective files.
% ==============================================================================

% ### Menu bar
% Sticky menu bar on top of the application with icon and buttons
#include "ui-menu-bar.lp".
	% menubar_title_override("My Application").
	% menubar_subtitle_override("What this application does").
	% menubar_icon_override("Menu").
% ---------------------------------------------------


% ### Messages
% Handles clinguin messages by showing alerts to the user
#include "ui-messages.lp".
	% ignore_message_id(download_success;no_optimization;no_more_solutions;no_solution).
	% ignore_message_type(info;error;warning;success).
% ---------------------------------------------------



% ============================================================================
% FIXED STRUCTURE
%
% The following elements are used by the templates and should not be removed
% or renamed since templates depend on these elements.
% ============================================================================

% DO NOT REMOVE! The root element is the top-level container for the application.
elem(ui_app, div, root).
attr(ui_app, class,
    ("min-h-screen";
     "flex";
     "flex-col";
     "bg-background";
     "text-foreground")).


	% DO NOT REMOVE!  The main content area is where the application content is displayed.
	elem(ui_content, main, ui_app).
	attr(ui_content, class,
		("flex";
		"min-h-0";
		"grow";
		"flex-col")).
	attr(ui_content, order, 100).


% ============================================================================
% APPLICATION UI
%
% Add the elements of your application below and attach top-level content to
% ui_content.
% ============================================================================

elem(main_table, div, ui_content).
attr(main_table, class,
    ("w-1/2";
     "p-4";
     "m-4")).

elem(p_table, table, main_table).
attr(p_table, class,
    ("table-fixed";
	 "border-radius")).

	elem(p_table_header, table(header), p_table).
		attr(p_table_header, class,
		    ("bg-card")).
		elem(p_table_header_row, table(row), p_table_header).

			attr(p_table_header_row(atom), class, "w-[150px]").
			attr(p_table_header_row(model;assumptions;cautious;brave), class, "w-[75px]").

			elem(p_table_header_row(atom), table(head), p_table_header_row).
			attr(p_table_header_row(atom), order, 1).

				elem(p_table_header_row_header(atom), span, p_table_header_row(atom)).
				attr(p_table_header_row_header(atom), text, "Atom").
				attr(p_table_header_row_header(atom), order, 1).

			elem(p_table_header_row(model), table(head), p_table_header_row).
			attr(p_table_header_row(model), order, 2).
				elem(p_table_header_row_header(model), span, p_table_header_row(model)).
				attr(p_table_header_row_header(model), text, "Model").
				attr(p_table_header_row_header(model), order, 1).

				elem(p_table_header_row_dd(model), dropdown_menu, p_table_header_row(model)).
				attr(p_table_header_row_dd(model), order, 2).
					elem(p_table_header_row_trigger(model), dropdown_menu(trigger), p_table_header_row_dd(model)).
						elem(p_table_header_row_button(model), button, p_table_header_row_trigger(model)).
						attr(p_table_header_row_button(model), size, xs).
						attr(p_table_header_row_button(model), variant, link).
						attr(p_table_header_row_button(model), class, "p-2").
							elem(p_table_header_row_button_icon(model), icon, p_table_header_row_button(model)).
							attr(p_table_header_row_button_icon(model), icon, "ListFilterPlus").
							attr(p_table_header_row_button_icon(model), size, xs).
					elem(p_table_header_row_content(model), dropdown_menu(content), p_table_header_row_dd(model)).
						elem(p_table_header_row_content_item(model,include), dropdown_menu(checkbox_item), p_table_header_row_content(model)).
						attr(p_table_header_row_content_item(model,include), content, "Included").
						attr(p_table_header_row_content_item(model,include), checked, true):-filter_model(include).
						attr(p_table_header_row_content_item(model,include), class, "hover:text-red-500"):-filter_model(include).
						when(p_table_header_row_content_item(model,include), click, call, add_atom(filter_model(include))):-not filter_model(include).
						when(p_table_header_row_content_item(model,include), click, call, remove_atom(filter_model(include))):-filter_model(include).
							elem(p_table_header_row_content_item_icon(model,include), icon, p_table_header_row_content_item(model,include)).
							attr(p_table_header_row_content_item_icon(model,include), icon, "ShieldCheck").
							attr(p_table_header_row_content_item_icon(model,include), size, xs).
						elem(p_table_header_row_content_item(model,exclude), dropdown_menu(checkbox_item), p_table_header_row_content(model)).
						attr(p_table_header_row_content_item(model,exclude), content, "Not included").
						attr(p_table_header_row_content_item(model,exclude), checked, true):-filter_model(exclude).
						attr(p_table_header_row_content_item(model,exclude), class, "hover:text-red-500"):-filter_model(exclude).
						when(p_table_header_row_content_item(model,exclude), click, call, add_atom(filter_model(exclude))):-not filter_model(exclude).
						when(p_table_header_row_content_item(model,exclude), click, call, remove_atom(filter_model(exclude))):-filter_model(exclude).
							elem(p_table_header_row_content_item_icon(model,exclude), icon, p_table_header_row_content_item(model,exclude)).
							attr(p_table_header_row_content_item_icon(model,exclude), icon, "ShieldCheck").
							attr(p_table_header_row_content_item_icon(model,exclude), size, xs).



			elem(p_table_header_row(assumptions), table(head), p_table_header_row).
			attr(p_table_header_row(assumptions), order, 3).
			attr(p_table_header_row(assumptions), content, "Assumptions").

			elem(p_table_header_row(brave), table(head), p_table_header_row).
			attr(p_table_header_row(brave), order, 4).
			attr(p_table_header_row(brave), content, "Brave").

			elem(p_table_header_row(cautious), table(head), p_table_header_row).
			attr(p_table_header_row(cautious), order, 5).
			attr(p_table_header_row(cautious), content, "Cautious").


	% Added as atoms from the UI
	% filter_model(include). filter_model(exclude).
	% filter_assume(true). filter_assume(false).
	% filter_brave(true). filter_brave(false).
	% filter_cautious(true). filter_cautious(false).
	possible_atom(P):-_any(P).
	include(P,model):-possible_atom(P), not filter_model(_).
	include(P,model):-possible_atom(P), _clinguin_model(P), filter_model(_), filter_model(include).
	include(P,model):-possible_atom(P), not _clinguin_model(P), filter_model(_), filter_model(exclude).

	atom(P):-_any(P),include(P,model).
	atom(P):-_clinguin_assume(P,_).

	elem(p_table_body, table(body), p_table).
		elem(p_table_body_row(P), table(row), p_table_body):-atom(P).
		attr(p_table_body_row(P), order, @to_int(P)):-atom(P).

			elem(p_table_body_row_atom(P), table(cell), p_table_body_row(P)):-atom(P).
			attr(p_table_body_row_atom(P), content, P):-atom(P).
			attr(p_table_body_row_atom(P), order, 1):-atom(P).
			attr(p_table_body_row_atom(P), class, "font-mono text-xs"):-atom(P).

			% ------- Current model

			elem(p_table_body_row_model(P), table(cell), p_table_body_row(P)):-atom(P).
			attr(p_table_body_row_model(P), order, 2):-atom(P).

				elem(p_table_body_row_model_icon(P), icon, p_table_body_row_model(P)):-atom(P),_clinguin_model(P).
				attr(p_table_body_row_model_icon(P), icon, "Star"):-atom(P),_clinguin_model(P).

			% ------- Assumptions
			elem(p_table_body_row_assumptions(P), table(cell), p_table_body_row(P)):-atom(P).
			attr(p_table_body_row_assumptions(P), order, 3):-atom(P).

				% elem(p_table_body_row_assumptions_buttong(P), button_group, p_table_body_row_assumptions(P)):-atom(P).

					elem(p_table_body_row_assumptions_button(P,true), toggle, p_table_body_row_assumptions(P)):-atom(P).
					attr(p_table_body_row_assumptions_button(P,true), size, "xs"):-atom(P).
					attr(p_table_body_row_assumptions_button(P,true), variant, "outline"):-atom(P).
					attr(p_table_body_row_assumptions_button(P,true), class, "ms-1"):-atom(P).
					attr(p_table_body_row_assumptions_button(P,true), disabled, true):-atom(P),_clinguin_assume(P,false).
					attr(p_table_body_row_assumptions_button(P,true), class, "bg-green-400 border-green-500 dark:bg-green-900/10 dark:border-green-700"):-atom(P),_clinguin_assume(P,true).
					when(p_table_body_row_assumptions_button(P,true), click, call, add_assumption(P,true)):-atom(P),not _clinguin_assume(P,true).
					when(p_table_body_row_assumptions_button(P,true), click, call, remove_assumption(P)):-atom(P),_clinguin_assume(P,true).

						elem(p_table_body_row_assumptions_button_icon(P,true), icon, p_table_body_row_assumptions_button(P,true)):-atom(P).
						attr(p_table_body_row_assumptions_button_icon(P,true), icon, "Check"):-atom(P).


					elem(p_table_body_row_assumptions_button(P,false), toggle, p_table_body_row_assumptions(P)):-atom(P).
					attr(p_table_body_row_assumptions_button(P,false), size, "xs"):-atom(P).
					attr(p_table_body_row_assumptions_button(P,false), class, "text-gray-500/80"):-atom(P), _all(P).
					attr(p_table_body_row_assumptions_button(P,false), variant, "outline"):-atom(P).
					attr(p_table_body_row_assumptions_button(P,false), class, "ms-1"):-atom(P).
					attr(p_table_body_row_assumptions_button(P,false), disabled, true):-atom(P),_clinguin_assume(P,true).
					attr(p_table_body_row_assumptions_button(P,false), class, "bg-red-400 border-red-500 dark:bg-red-900/10 dark:border-red-700"):-atom(P),_clinguin_assume(P,false).
					when(p_table_body_row_assumptions_button(P,false), click, call, add_assumption(P,false)):-atom(P),not _clinguin_assume(P,false).
					when(p_table_body_row_assumptions_button(P,false), click, call, remove_assumption(P)):-atom(P),_clinguin_assume(P,false).

						elem(p_table_body_row_assumptions_button_icon(P,false), icon, p_table_body_row_assumptions_button(P,false)):-atom(P).
						attr(p_table_body_row_assumptions_button_icon(P,false), icon, "X"):-atom(P).


			% ------- Brave
			elem(p_table_body_row_brave(P), table(cell), p_table_body_row(P)):-atom(P).
			attr(p_table_body_row_brave(P), order, 4):-atom(P).

				elem(p_table_body_row_brave_badge(P), badge, p_table_body_row_brave(P)):-atom(P),_any(P).
				elem(p_table_body_row_brave_badge_icon(P), icon, p_table_body_row_brave_badge(P)):-atom(P),_any(P).
				attr(p_table_body_row_brave_badge_icon(P), icon, "Star"):-atom(P),_any(P).

			% ------- Cautious
			elem(p_table_body_row_cautious(P), table(cell), p_table_body_row(P)):-atom(P).
			attr(p_table_body_row_cautious(P), order, 5):-atom(P).

				elem(p_table_body_row_cautious_badge(P), badge, p_table_body_row_cautious(P)):-atom(P),_all(P).
				elem(p_table_body_row_cautious_badge_icon(P), icon, p_table_body_row_cautious_badge(P)):-atom(P),_all(P).
				attr(p_table_body_row_cautious_badge_icon(P), icon, "Star"):-atom(P),_all(P).


	% <Table.Root>
	% <Table.Caption>A list of your recent invoices.</Table.Caption>
	% <Table.Header>
	% 	<Table.Row>
	% 		<Table.Head class="w-[100px]">Invoice</Table.Head>
	% 		<Table.Head>Status</Table.Head>
	% 		<Table.Head>Method</Table.Head>
	% 		<Table.Head class="text-end">Amount</Table.Head>
	% 	</Table.Row>
	% </Table.Header>
	% <Table.Body>
	% 	{#each invoices as invoice (invoice)}
	% 		<Table.Row>
	% 			<Table.Cell class="font-medium">{invoice.invoice}</Table.Cell>
	% 			<Table.Cell>{invoice.paymentStatus}</Table.Cell>
	% 			<Table.Cell>{invoice.paymentMethod}</Table.Cell>
	% 			<Table.Cell class="text-end">{invoice.totalAmount}</Table.Cell>
	% 		</Table.Row>
	% 	{/each}
	% </Table.Body>
