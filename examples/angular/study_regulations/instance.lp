#const n = 4.

% b, f, a, o and p               % c
in((bm1;bm2;bm3),b).             map(c,(bm1;bm2;bm3),9).
in((fm1;fm2;fm3),f).             map(c,(fm1;fm2;fm3),6).
in((am11;am12;am21),a).          map(c,(am11;am12;am21),6).
in((am22;am31;am32),a).          map(c,(am22;am31;am32),6).
in(E,o) :- in(E,(f;a)).          map(c,(pm1;pm2;pm3),12).
in((pm1;pm2;pm3),p).             map(c,im,15).
                                 map(c,msc,30).

% m                              % s
in(E,m) :- in(E,(b;f;a;p)).      map(s,bm1,w;s,bm2,s;s,bm3,w).
in((im;msc),m).                  map(s,(fm1;fm2;fm3),w).
                                 map(s,(am11;am12;am21),e).
                                 map(s,(am22;am31;am32),e).
% e                              map(s,(pm1;pm2;pm3),e).
in(fm1,e).                       map(s,(im1;msc1),e).

                                 % l and u
                                 map(l,b,27;l,o,24;l,p,24;l,m,120).
                                 map(u,b,27;u,o,24;u,p,24;u,m,120).

% global constraints
card(e,leq,2).  equal(int(s,f),e).
sum(int(H,s),c,bw,(L,U)) :- H = (b;o;p;m), map(l,H,L), map(u,H,U).
in(im,gc3). in(msc,gc3). subseteq(gc3,s).

% temporal constraints
empty(int(s(I),s(J)))       :- I = 1..n, J = 1..n, I < J.
empty(int(m(w),s(2*K  )))   :- K = 1..n, 1 <= 2*K,   2*K   <= n.
empty(int(m(s),s(2*K-1)))   :- K = 1..n, 1 <= 2*K-1, 2*K-1 <= n.
in(msc,tc4). sum(before(tc4),c,geq,90).

