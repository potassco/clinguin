ds_state_input(brave,"Brave Consequences","Atoms in some model").
ds_state_input_elem(brave,_any(P)):- _any(P).

ds_state_input(cautious,"Cautious Consequences","Atoms in all models").
ds_state_input_elem(cautious,_all(P)):- _all(P).

ds_state_input(brave_optimal,"Optimal Brave Consequences","Atoms in some optimal model").
ds_state_input_elem(brave_optimal,_any_opt(P)):- _any_opt(P).

ds_state_input(cautious_optimal,"Optimal Cautious Consequences","Atoms in all optimal models").
ds_state_input_elem(cautious_optimal,_all_opt(P)):- _all_opt(P).

ds_state_input(model,"Current Model","Atoms in the current model, also provided as untagged facts").
ds_state_input_elem(model,P):- _clinguin_model(P).

ds_state_input(context,"Client Context","Keys and values submitted by the client").
ds_state_input_elem(context,_clinguin_context(K,V)):- _clinguin_context(K,V).

ds_state_input(files,"Files","Uploaded files, their contents, and currently active files").
ds_state_input_elem(files,_clinguin_optional_file(F)):- _clinguin_optional_file(F).
ds_state_input_elem(files,_clinguin_active_file(F)):- _clinguin_active_file(F).
ds_state_input_elem(files,_clinguin_file_content(F,C)):- _clinguin_file_content(F,C).

ds_state_input(constants,"Constants","Command-line constants used by the domain encoding").
ds_state_input_elem(constants,_clinguin_const(K,V)):- _clinguin_const(K,V).

ds_state_input(browsing,"Browsing State","Present while browsing solutions").
ds_state_input_elem(browsing,_clinguin_browsing):- _clinguin_browsing.

ds_state_input(optimization,"Optimization","Current model costs and optimality flags").
ds_state_input_elem(optimization,_clinguin_cost(C)):- _clinguin_cost(C).
ds_state_input_elem(optimization,_clinguin_cost(I,C)):- _clinguin_cost(I,C).
ds_state_input_elem(optimization,_clinguin_optimal):- _clinguin_optimal.
ds_state_input_elem(optimization,_clinguin_optimizing):- _clinguin_optimizing.

ds_state_input(unsat,"Unsatisfiability","Present when the domain problem is unsatisfiable").
ds_state_input_elem(unsat,_clinguin_unsat):- _clinguin_unsat.

ds_state_input(assumptions,"Assumptions","Atoms assumed true or false").
ds_state_input_elem(assumptions,_clinguin_assume(P,V)):- _clinguin_assume(P,V).

ds_state_input(externals,"External Atoms","External atoms set true, false, or released").
ds_state_input_elem(externals,_clinguin_external(P,V)):- _clinguin_external(P,V).

ds_state_input(atoms,"Added Atoms","Atoms added through backend operations").
ds_state_input_elem(atoms,_clinguin_atom(P)):- _clinguin_atom(P).

ds_state_input(messages,"Messages","Backend messages with ID, type, title, and content").
ds_state_input_elem(messages,_clinguin_message(I,T,H,C)):- _clinguin_message(I,T,H,C).

elem(dev_drawer, drawer, menubar_right).
attr(dev_drawer, direction, right).

    elem(dev_drawer_trigger, drawer(trigger), dev_drawer).

        elem(dev_drawer_trigger_button, button, dev_drawer_trigger).
        attr(dev_drawer_trigger_button, content, "Dev").
        attr(dev_drawer_trigger_button, size, "xs").
        attr(dev_drawer_trigger_button, variant, outline).

            elem(dev_drawer_trigger_button_icon, icon, dev_drawer_trigger_button).
            attr(dev_drawer_trigger_button_icon, icon, "Code").
            attr(dev_drawer_trigger_button_icon, size, "xs").

    elem(dev_drawer_content, drawer(content), dev_drawer).
    attr(dev_drawer_content, class,
        ("min-h-0"; "border-border"; "data-[vaul-drawer-direction=right]:sm:max-w-xl")).

        elem(dev_drawer_header, drawer(header), dev_drawer_content).
        attr(dev_drawer_header, order, 1).

        elem(dev_drawer_title, drawer(title), dev_drawer_header).
        attr(dev_drawer_title, content, "Dev tools").
        attr(dev_drawer_title, class, "text-lg").
        attr(dev_drawer_title, order, 1).

        elem(dev_drawer_description, drawer(description), dev_drawer_header).
        attr(dev_drawer_description, content, "See the input to the UI encoding").
        attr(dev_drawer_description, order, 2).
        attr(dev_drawer_description, class, "mb-4").



        elem(dev_drawer_div, div, dev_drawer_content).
        attr(dev_drawer_div, class,
            ("flex"; "min-h-0"; "flex-1"; "flex-col"; "gap-4";
             "overflow-y-auto"; "p-4"; "pt-0")).
        attr(dev_drawer_div, order, 4).

            elem(dev_state_card(S), details, dev_drawer_div) :-
                ds_state_input(S,_,_).
            attr(dev_state_card(S), class,
                ("group"; "min-w-0"; "shrink-0"; "rounded-xl"; "border";
                 "border-border"; "bg-card"; "text-card-foreground";
                 "shadow-sm")) :- ds_state_input(S,_,_).
            attr(dev_state_card(S), "aria-labelledby", dev_state_title(S)) :-
                ds_state_input(S,_,_).

                elem(dev_state_header(S), summary, dev_state_card(S)) :-
                    ds_state_input(S,_,_).
                attr(dev_state_header(S), class,
                    ("relative"; "list-none"; "cursor-pointer"; "space-y-1";
                     "rounded-xl"; "p-4"; "pr-10"; "hover:bg-muted/50";
                     "focus-visible:outline-none"; "focus-visible:ring-2";
                     "focus-visible:ring-ring"; "[&::-webkit-details-marker]:hidden")) :-
                    ds_state_input(S,_,_).
                attr(dev_state_header(S), order, 1) :- ds_state_input(S,_,_).
                attr(dev_state_header(S), style, "display: block; list-style: none;") :-
                    ds_state_input(S,_,_).

                    elem(dev_state_chevron(S), icon, dev_state_header(S)) :-
                        ds_state_input(S,_,_).
                    attr(dev_state_chevron(S), icon, "ChevronDown") :-
                        ds_state_input(S,_,_).
                    attr(dev_state_chevron(S), class,
                        ("absolute"; "right-4"; "top-4"; "size-4";
                         "text-muted-foreground"; "transition-transform";
                         "group-open:rotate-180")) :- ds_state_input(S,_,_).
                    attr(dev_state_chevron(S), order, 3) :- ds_state_input(S,_,_).

                    elem(dev_state_title(S), h3, dev_state_header(S)) :-
                        ds_state_input(S,_,_).
                    attr(dev_state_title(S), content, T) :- ds_state_input(S,T,_).
                    attr(dev_state_title(S), class, ("text-sm"; "font-semibold")) :-
                        ds_state_input(S,_,_).
                    attr(dev_state_title(S), order, 1) :- ds_state_input(S,_,_).

                    elem(dev_state_description(S), p, dev_state_header(S)) :-
                        ds_state_input(S,_,_).
                    attr(dev_state_description(S), content, D) :- ds_state_input(S,_,D).
                    attr(dev_state_description(S), class,
                        ("text-xs"; "text-muted-foreground")) :- ds_state_input(S,_,_).
                    attr(dev_state_description(S), order, 2) :- ds_state_input(S,_,_).

                elem(dev_state_elements(S), div, dev_state_card(S)) :-
                    ds_state_input(S,_,_).
                attr(dev_state_elements(S), class,
                    ("flex"; "flex-wrap"; "gap-2"; "px-4"; "pb-4")) :-
                    ds_state_input(S,_,_).
                attr(dev_state_elements(S), order, 2) :- ds_state_input(S,_,_).

                    elem(dev_state_badge(S,P), badge, dev_state_elements(S)) :-
                        ds_state_input(S,_,_), ds_state_input_elem(S,P).
                    attr(dev_state_badge(S,P), content, P) :-
                        ds_state_input(S,_,_), ds_state_input_elem(S,P).
                    attr(dev_state_badge(S,P), variant, secondary) :-
                        ds_state_input(S,_,_), ds_state_input_elem(S,P).
                    attr(dev_state_badge(S,P), class,
                        ("font-mono"; "text-xs"; "h-auto"; "max-w-full";
                         "whitespace-normal"; "break-all"; "rounded-md";
                         "px-2"; "py-1"; "text-left"; "justify-start")) :-
                        ds_state_input(S,_,_), ds_state_input_elem(S,P).

                    elem(dev_state_empty(S), p, dev_state_elements(S)) :-
                        ds_state_input(S,_,_), not ds_state_input_elem(S,_).
                    attr(dev_state_empty(S), content, "No elements.") :-
                        ds_state_input(S,_,_), not ds_state_input_elem(S,_).
                    attr(dev_state_empty(S), class,
                        ("text-xs"; "text-muted-foreground"; "italic")) :-
                        ds_state_input(S,_,_), not ds_state_input_elem(S,_).


dev_owned(dev_drawer).
dev_owned(ID) :- elem(ID,_,P), dev_owned(P).
dev_inspect(ID,T,P) :- elem(ID,T,P), not dev_owned(ID).
% dev_inspect_level(root,0).
% dev_inspect_level(P,L+1) :- dev_inspect_level(P,L), dev_inspect(ID,_,P).

dev_attr(ID, class,
    ("transition-shadow"; "duration-150"; "hover:ring-2";
     "hover:ring-inset"; "hover:ring-indigo-500/70"; "hover:shadow-md";
     "hover:shadow-indigo-500/20"; "dark:hover:ring-indigo-400/70";
     "dark:hover:shadow-indigo-400/20")) :- dev_inspect(ID,_,_).

% Keep inspector facts separate so its own cards and events are not inspected.
dev_elem(dev_inspector_provider, sidebar(provider), ui_app).
dev_attr(dev_inspector_provider, class,
    ("pointer-events-none"; "fixed"; "right-4"; "top-20"; "z-[60]";
     "min-h-0"; "w-[28rem]"; "max-w-[calc(100vw-2rem)]")).
dev_elem(dev_inspector_sidebar, sidebar, dev_inspector_provider).
dev_attr(dev_inspector_sidebar, side, right).
dev_attr(dev_inspector_sidebar, collapsible, none).
dev_attr(dev_inspector_sidebar, class, ("h-auto"; "w-full"; "bg-transparent")).
dev_elem(dev_inspector, sidebar(content), dev_inspector_sidebar).
dev_attr(dev_inspector, class, ("max-h-[80vh]"; "flex-none"; "gap-1"; "overflow-y-auto")).
dev_attr(dev_inspector, "aria-label", "Hovered element inspector").

dev_elem(dev_info(ID), section, dev_inspector) :- dev_inspect(ID,_,_).
dev_attr(dev_info(ID), style, "display: none;") :- dev_inspect(ID,_,_).
dev_attr(dev_info(ID), class,
    ("shrink-0"; "rounded-xl"; "border"; "border-indigo-500/40";
     "bg-card/95"; "text-card-foreground"; "shadow-lg"; "backdrop-blur";
     "p-1.5"; "space-y-0.5")) :- dev_inspect(ID,_,_).
% dev_attr(dev_info(ID), "margin-left", @concat(L,"rem")):-dev_inspect_level(ID,L).
% dev_attr(dev_info(ID), order, L):-dev_inspect_level(ID,L).
dev_when(ID, mouseenter, update, (dev_info(ID),style,"display: block;")) :-
    dev_inspect(ID,_,_).
dev_when(ID, mouseleave, update, (dev_info(ID),style,"display: none;")) :-
    dev_inspect(ID,_,_).

dev_elem(dev_info_title(ID), h3, dev_info(ID)) :- dev_inspect(ID,_,_).
dev_attr(dev_info_title(ID), content, ID) :- dev_inspect(ID,_,_).
dev_attr(dev_info_title(ID), class,
    ("font-mono"; "text-xs"; "font-semibold"; "break-all"; "text-indigo-500")) :-
    dev_inspect(ID,_,_).
dev_attr(dev_info_title(ID), order, 1) :- dev_inspect(ID,_,_).

dev_elem(dev_info_body(ID), div, dev_info(ID)) :- dev_inspect(ID,_,_).
dev_attr(dev_info_body(ID), class,
    ("flex"; "flex-col"; "gap-0"; "font-mono"; "text-xs"; "leading-tight")) :-
    dev_inspect(ID,_,_).
dev_attr(dev_info_body(ID), order, 2) :- dev_inspect(ID,_,_).

dev_line(ID,metadata,1,@concat("parent: ",P," | type: ",T)) :-
    dev_inspect(ID,T,P).
dev_line(ID,attribute(K,V),2,@concat(K," = ",V)) :-
    dev_inspect(ID,_,_), attr(ID,K,V).
dev_line(ID,action(E,A,O),3,@concat(E," -> ",A," -> ",O)) :-
    dev_inspect(ID,_,_), when(ID,E,A,O).

dev_elem(dev_info_line(ID,L), code, dev_info_body(ID)) :- dev_line(ID,L,_,_).
dev_attr(dev_info_line(ID,L), content, Text) :- dev_line(ID,L,_,Text).
dev_attr(dev_info_line(ID,L), order, N) :- dev_line(ID,L,N,_).
dev_attr(dev_info_line(ID,L), class, "break-all whitespace-pre-wrap") :-
    dev_line(ID,L,_,_).
dev_attr(dev_info_line(ID,metadata), class, "text-muted-foreground") :-
    dev_inspect(ID,_,_).

#show elem(ID,T,P):dev_elem(ID,T,P).
#show attr(ID,K,V):dev_attr(ID,K,V).
#show when(ID,E,A,O):dev_when(ID,E,A,O).

% <Card.Root class="w-full max-w-sm">
% 	<Card.Header>
% 		<Card.Title>Login to your account</Card.Title>
% 		<Card.Description>Enter your email below to login to your account</Card.Description>
% 		<Card.Action>
% 			<Button variant="link">Sign Up</Button>
% 		</Card.Action>
% 	</Card.Header>
% 	<Card.Content>
% 		<form>
% 			<div class="flex flex-col gap-6">
% 				<div class="grid gap-2">
% 					<Label for="email">Email</Label>
% 					<Input id="email" type="email" placeholder="m@example.com" required />
% 				</div>
% 				<div class="grid gap-2">
% 					<div class="flex items-center">
% 						<Label for="password">Password</Label>
% 						<a href="##" class="ml-auto inline-block text-sm underline-offset-4 hover:underline">
% 							Forgot your password?
% 						</a>
% 					</div>
% 					<Input id="password" type="password" required />
% 				</div>
% 			</div>
% 		</form>
% 	</Card.Content>
% 	<Card.Footer class="flex-col gap-2">
% 		<Button type="submit" class="w-full">Login</Button>
% 		<Button variant="outline" class="w-full">Login with Google</Button>
% 	</Card.Footer>
% </Card.Root>
% <Drawer.Root direction="left">
% 	<Drawer.Trigger class={buttonVariants({ variant: "secondary" })}>Open Left Drawer</Drawer.Trigger>
% 	<Drawer.Content>
% 		<Drawer.Header>
% 			<Drawer.Title>Move Goal</Drawer.Title>
% 			<Drawer.Description>Set your daily activity goal.</Drawer.Description>
% 		</Drawer.Header>
% 		<div class="flex-1 p-4">
% 			<div class="size-full rounded-2xl bg-muted"></div>
% 		</div>
% 		<Drawer.Footer>
% 			<Drawer.Close class={buttonVariants()}>Close</Drawer.Close>
% 		</Drawer.Footer>
% 	</Drawer.Content>
% </Drawer.Root>
