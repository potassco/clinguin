% ============================================================================
% MESSAGES
% Handles clinguin messages by showing alerts to the user
%
% Enable it in ui.lp:
%     #include "ui-messages.lp".
%
%
% Edit "CUSTOMIZATION" below for the usual changes.
% ============================================================================

% ============================================================================
% CUSTOMIZATION
%
% Customize which messages to ignore below.
% ============================================================================


% ignore_message_id(download_success).
% ignore_message_id(no_optimization).
% ignore_message_id(no_more_solutions).
% ignore_message_id(no_solution).

% ignore_message_type(info).
% ignore_message_type(error).
% ignore_message_type(warning).
% ignore_message_type(success).


% ============================================================================
% CONTENT
% ============================================================================

elem(alerts, div, root).
attr(alerts, class, "fixed inset-0 z-50 flex flex-col justify-end gap-4 p-4 pointer-events-none items-start").

    elem(alert(X), alert, alerts):- _clinguin_message(X,T,_,_), not ignore_message_id(X), not ignore_message_type(T).
    attr(alert(X), class, "pointer-events-auto"):- _clinguin_message(X,_,_,_).
    attr(alert(X), class, "max-w-xl min-w-xs backdrop-blur-3xl bg-card-500/60"):- _clinguin_message(X,_,_,_).
    attr(alert(X), class, "border-destructive text-destructive dark:border-destructive dark:text-destructive"):- _clinguin_message(X,error,_,_).
    attr(alert(X), class, "border-green-600 text-green-600 dark:border-green-700 dark:text-green-700"):- _clinguin_message(X,success,_,_).
    attr(alert(X), class, "border-yellow-600 text-yellow-600 dark:border-yellow-700 dark:text-yellow-700"):- _clinguin_message(X,warning,_,_).
    attr(alert(X), class, "border-gray-600 text-gray-600 dark:border-gray-400 dark:text-gray-400"):- _clinguin_message(X,info,_,_).


        elem(alert_icon(X), icon, alert(X)):- _clinguin_message(X,_,_,_).
        attr(alert_icon(X), icon, "CircleCheckIcon"):- _clinguin_message(X,success,_,_).
        attr(alert_icon(X), icon, "CircleX"):- _clinguin_message(X,error,_,_).
        attr(alert_icon(X), class, "text-red-500"):- _clinguin_message(X,error,_,_).
        attr(alert_icon(X), icon, "InfoIcon"):- _clinguin_message(X,info,_,_).
        attr(alert_icon(X), icon, "CircleAlert"):- _clinguin_message(X,warning,_,_).
        attr(alert_icon(X), order, 1):- _clinguin_message(X,_,_,I).

        elem(alert_title(X), alert(title), alert(X)):- _clinguin_message(X,_,_,_).
        attr(alert_title(X), content, T):- _clinguin_message(X,_,T,_).
        attr(alert_title(X), order, 2):- _clinguin_message(X,_,T,_).

        elem(alert_description(X), alert(description), alert(X)):- _clinguin_message(X,_,_,_).
        attr(alert_description(X), content, D):- _clinguin_message(X,_,_,D).
        attr(alert_description(X), order, 3):- _clinguin_message(X,_,_,D).



