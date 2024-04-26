% generate
{ in(E,s(I)) } :- in(E,m), I=1..n.

% s = s(1) U ... U s(n)
in(E,s) :- in(E,s(I)).

% m(w) and m(s)
in(E,m(X)) :- X = (s;w), in(E,m), map(s,E,X).

% additional sets
set(A) :-      empty(A).
set(A) :- subseteq(A,B).    set(A) :-   equal(A,B).
set(B) :- subseteq(A,B).    set(B) :-   equal(A,B).
set(A) :-   card(A,R,L).    set(A) :- sum(A,M,R,L).
%
set(A) :- set( int(A,B)).   set(B) :- set(int(A,B)).
set(A) :- set(before(A)).
%
in( E, int(A,B)) :- set( int(A,B)), in(E,A), in(E,B).
in(E1,before(A)) :- set(before(A)), in(E1,s(I)), in(E2,A), in(E2,s(J)), I < J.

% constraints
:- empty(A), in(E,A).
%
:- subseteq(A,B), in(E,A), not in(E,B).
%
:- equal(A,B), in(E,A), not in(E,B).
:- equal(A,B), not in(E,A), in(E,B).
%
:- card(A,leq,U), not { in(E,A) } U.
%
:- sum(A,F,bw,(L,U)), not L #sum{ V,E : in(E,A), map(F,E,V) } U.
:- sum(A,F,geq,   L), not L #sum{ V,E : in(E,A), map(F,E,V) }.

% display
% #show.
% #show (M,I) : in(M,s(I)).
