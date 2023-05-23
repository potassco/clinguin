% x(1..n)
semester(1..n).
{ in(E,x(I)) } :- in(E,m), I=1..n.

% x = x(1) cup ... cup x(n)
in(E,x) :- in(E,x(I)).

% regular constraints
subseteq(e,x).
sum(cap(       H,x),c,bw,(L,U)) :- H=(b;p), map(l,H,L), map(u,H,U).
sum(cap(cup(a,f),x),c,bw,(L,U)) :-          map(l,a,L), map(u,a,U).
in(im,rc4). in(msc,rc4). subseteq(rc4,x).

% temporal constraints
empty(cap(x(I),x(J)))       :- I=1..n, J=1..n, I < J.
empty(cap(m(w),x(2*K  )))   :- K=1..n, 2*K   <= n.
empty(cap(m(s),x(2*K-1)))   :- K=1..n, 2*K-1 <= n.
sum(tc4,c,geq,90).
in(E,tc4) :- in(E,x(I)), in(msc,x(J)), I<J.
%
% QUESTION: shall we come up with temporal constructs to write something like
%             sum(before(msc),c,eq,90)
%           instead of defining the set tc4 in ASP?
%

%
% meta-encoding
%

%  sum(A,M,bw,(L,U)) means L \leq \sum_{x \in A} M(x) \geq U
:- sum(A,M,bw,(L,U)), not L #sum{ V,E : in(E,A), map(M,E,V) } U.

%  sum(A,M,geq,   L) means L \leq \sum_{x \in A} M(x)
:- sum(A,M,geq,   L), not L #sum{ V,E : in(E,A), map(M,E,V) }.

%  subseteq(A,B) means A \subseteq B
:- subseteq(A,B), in(E,A), not in(E,B).

% empty(A) means A = \emptyset
:- empty(A), in(E,A).

% sets
set(A) :- sum(A,M,R,L).
set(A) :- empty(A).
set(A) :- subseteq(A,B).
set(B) :- subseteq(A,B).
%
set(A) :- set(cap(A,B)).
set(B) :- set(cap(A,B)).
set(A) :- set(cup(A,B)).
set(B) :- set(cup(A,B)).
set(A) :- set(sub(A,B)).
set(B) :- set(sub(A,B)).
%
in(E,cup(A,B)) :- set(cup(A,B)), in(E,A).
in(E,cup(A,B)) :- set(cup(A,B)), in(E,B).
in(E,cap(A,B)) :- set(cap(A,B)), in(E,A),     in(E,B).
in(E,sub(A,B)) :- set(sub(A,B)), in(E,A), not in(E,B).


%
% display
%
% #show.
% #show (M,I) : in(M,x(I)).

%*
%
% test
%
s'(bm1,1). s'(bm3,1). s'(am11,1). s'(am12,1).
s'(bm2,2). s'(am21,2). s'(pm1,2).
% s'(im,3). s'(pm3,3). s'(am31,3). % UNSAT
  s'(im,3). s'(pm3,2). s'(am31,3). %   SAT
s'(msc,4).
%
:- in(M,x(I)), not s'(M,I).
:- not in(M,x(I)), s'(M,I).
*%

