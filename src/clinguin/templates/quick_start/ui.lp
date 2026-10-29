% ============================================================================
% CLINGUIN UI QUICK START
%
% 1. Uncomment the templates you want to use.
% 2. Customize each enabled template in its own file.
% 3. Write your application UI below "APPLICATION UI".
%
% Reusable templates attach to one of these stable elements:
%     ui_app      - the complete application
%     ui_content  - the main application content
% ============================================================================


% ==============================================================================
% TEMPLATES
%
% Uncomment the templates you want to use. Customize each template in
% its own file.
% ==============================================================================

% Sticky menu bar. Customize it in menu-bar.lp.
#include "menu-bar.lp".



% ============================================================================
% FIXED STRUCTURE
%
% The following elements are used by the templates and should not be removed
% or renamed.
% ============================================================================

% The root element is the top-level container for the application.
elem(ui_app, div, root).
attr(ui_app, class,
    ("min-h-screen";
     "flex";
     "flex-col";
     "bg-background";
     "text-foreground")).


	% The main content area is where the application content is displayed.
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
