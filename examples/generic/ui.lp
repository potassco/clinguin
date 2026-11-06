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

#script(python)
from clingo.symbol import String, Function, Number
def signature_name(s):
    return Function(s.name,[])
def signature_arity(s):
    return Number(len(s.arguments))
#end.


elem(main_table, div, ui_content).
attr(main_table, class,
    ("w-[800px]";
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

			attr(p_table_header_row(atom), class, "w-[200px]").
			attr(p_table_header_row(model;assumptions;cautious;brave), class, "w-[125px]").

			% elem(p_table_header_row(atom), table(head), p_table_header_row).
			% attr(p_table_header_row(atom), order, 1).

			% 	elem(p_table_header_row_header(atom), span, p_table_header_row(atom)).
			% 	attr(p_table_header_row_header(atom), text, "Atom").
			% 	attr(p_table_header_row_header(atom), order, 1).

			row_name(atom;model;assumptions;brave;cautious).
			row_header(atom, "Atom", 1).
			row_header(model, "Model", 2).
			row_header(assumptions, "Assumptions", 3).
			row_header(brave, "Brave", 4).
			row_header(cautious, "Cautious", 5).

			elem(p_table_header_row(R), table(head), p_table_header_row):-row_name(R).
			attr(p_table_header_row(R), order, O):-row_header(R,_,O).
				elem(p_table_header_row_header(R), span, p_table_header_row(R)):-row_name(R).
				attr(p_table_header_row_header(R), text, T):-row_header(R,T,_).
				attr(p_table_header_row_header(R), order, 1):-row_name(R).

				elem(p_table_header_row_dd(R), dropdown_menu, p_table_header_row(R)):-row_name(R).
				attr(p_table_header_row_dd(R), order, 2):-row_name(R).
					elem(p_table_header_row_trigger(R), dropdown_menu(trigger), p_table_header_row_dd(R)):-row_name(R).
						elem(p_table_header_row_button(R), button, p_table_header_row_trigger(R)):-row_name(R).
						attr(p_table_header_row_button(R), size, xs):-row_name(R).
						attr(p_table_header_row_button(R), variant, ghost):-row_name(R), not filter(R,_).
						attr(p_table_header_row_button(R), variant, link):-row_name(R), filter(R,_).
						attr(p_table_header_row_button(R), class, "p-2"):-row_name(R).
							elem(p_table_header_row_button_icon(R), icon, p_table_header_row_button(R)):-row_name(R).
							attr(p_table_header_row_button_icon(R), icon, "Sparkle"):-row_name(R), not filter(R,_).
							attr(p_table_header_row_button_icon(R), icon, "Sparkles"):-row_name(R),filter(R,_).
							attr(p_table_header_row_button_icon(R), size, xs):-row_name(R).
					elem(p_table_header_row_content(R), dropdown_menu(content), p_table_header_row_dd(R)):-row_name(R).
					attr(p_table_header_row_content(R), class, "w-[200px]"):-row_name(R).

						elem(p_table_header_row_content_item(R,V), dropdown_menu(checkbox_item), p_table_header_row_content(R)):-row_option(R,V,_,_,_,_).
						attr(p_table_header_row_content_item(R,V), content, T):-row_option(R,V,T,_,_,_).
						attr(p_table_header_row_content_item(R,V), order, O):-row_option(R,V,_,_,_,O).
						attr(p_table_header_row_content_item(R,V), checked, true):-filter(R,V).
						attr(p_table_header_row_content_item(R,V), class, "hover:text-red-500"):-filter(R,V).
						when(p_table_header_row_content_item(R,V), click, call, add_atom(F)):-row_option(R,V,_,_,F,_),not filter(R,V).
						when(p_table_header_row_content_item(R,V), click, call, remove_atom(F)):-row_option(R,V,_,_,F,_),filter(R,V).
							elem(p_table_header_row_content_item_icon(R,V), icon, p_table_header_row_content_item(R,V)):-row_option(R,V,_,_,_,_).
							attr(p_table_header_row_content_item_icon(R,V), icon, I):-row_option(R,V,_,I,_,_).
							attr(p_table_header_row_content_item_icon(R,V), size, xs):-row_option(R,V,_,_,_,_).

	% Options map shared dropdowns to the atoms added and removed by the UI.
	row_option(atom,(N,A),@concat(N,"/",A),"CircleLarge",filter(atom,(N,A)),1):-atom_signature(_,(N,A)).
	row_option(model,true,"Included","Star",filter(model,true),1).
	row_option(model,false,"Not included","StarOff",filter(model,false),2).
	row_option(assumptions,true,"True","Check",filter(assumptions,true),1).
	row_option(assumptions,false,"False","X",filter(assumptions,false),2).
	row_option(assumptions,none,"No assumption","Minus",filter(assumptions,none),3).
	row_option(brave,true,"Included","Star",filter(brave,true),1).
	row_option(brave,false,"Not included","StarOff",filter(brave,false),2).
	row_option(cautious,true,"Included","Star",filter(cautious,true),1).
	row_option(cautious,false,"Not included","StarOff",filter(cautious,false),2).

	possible_atom(P):-_any(P).
	possible_atom(P):-_clinguin_assume(P,_).
	atom_signature(P,(@signature_name(P),@signature_arity(P))):-possible_atom(P).


	shown(R,P):- row_option(R,_,_,_,_,_), not filter(R,_), possible_atom(P).
	shown(atom,P):- filter(atom,(N,A)), atom_signature(P,(N,A)), possible_atom(P).
	shown(model,P):- filter(model,true), _clinguin_model(P), possible_atom(P).
	shown(model,P):- filter(model,false), not _clinguin_model(P), possible_atom(P).
	shown(assumptions,P):- filter(assumptions,true), _clinguin_assume(P,true),possible_atom(P).
	shown(assumptions,P):- filter(assumptions,false), _clinguin_assume(P,false),possible_atom(P).
	shown(assumptions,P):- filter(assumptions,none), not _clinguin_assume(P,_),possible_atom(P).
	shown(brave,P):- filter(brave,true), _any(P),possible_atom(P).
	shown(brave,P):- filter(brave,false), not _any(P),possible_atom(P).
	shown(cautious,P):- filter(cautious,true), _all(P),possible_atom(P).
	shown(cautious,P):- filter(cautious,false), not _all(P),possible_atom(P).

	atom(P):-possible_atom(P), shown(model,P), shown(assumptions,P), shown(brave,P), shown(cautious,P), shown(atom,P).

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
				elem(p_table_body_row_model_badge(P), badge, p_table_body_row_model(P)):-atom(P),_clinguin_model(P).

				elem(p_table_body_row_model_icon(P), icon, p_table_body_row_model_badge(P)):-atom(P),_clinguin_model(P).
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
					attr(p_table_body_row_assumptions_button(P,true), class, "bg-green-400 border-green-500 dark:bg-green-800/30 dark:border-green-700"):-atom(P),_clinguin_assume(P,true).
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
					attr(p_table_body_row_assumptions_button(P,false), class, "bg-red-400 border-red-500 dark:bg-red-800/30 dark:border-red-700"):-atom(P),_clinguin_assume(P,false).
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
