% Instance
node(1..4).
edge(1,2).
edge(1,3).
color(red; green).

% Encoding
{ assign(N, C) : color(C) } = 1 :- node(N).
:- edge(N, M), assign(N, C), assign(M, C).


% My labeled code
_cautious(paint(N,C)):-assign(N,C). %Cautious
_brave(option(N,C)):-assign(N,C). %Brave

% Exptected output
% paint(1,red).
% paint(2,green).
% paint(3,green).
% option(1,red).
% option(2,green).
% option(3,green).
% option(4,green).
% option(4,red).