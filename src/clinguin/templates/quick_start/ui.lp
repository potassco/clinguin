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
	show_statements_for_download_and_save("#show sudoku/3.").
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
%
% To replace the menu bar defaults from this file, add:
%     menubar_title_override("My Application").
%     menubar_subtitle_override("What this application does").
%     menubar_icon_override("Menu").
% ============================================================================
