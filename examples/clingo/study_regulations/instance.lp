% m
in((bm1;bm2;bm3),m).
in((fm1;fm2;fm3),m).
in((am11;am12;am21;am22;am31;am32),m).
in((pm1;pm2;pm3),m).
in(im,m).
in(msc,m).

% b, f, a and p
in((bm1;bm2;bm3),b).
in((fm1;fm2;fm3),f).
in((am11;am12;am21;am22;am31;am32),a).
in((pm1;pm2;pm3),p).

% c
map(c,(bm1;bm2;bm3),9).
map(c,(fm1;fm2;fm3),6).
map(c,(am11;am12;am21;am22;am31;am32),6).
map(c,(pm1;pm2;pm3),12).
map(c,im,15).
map(c,msc,30).

% s
map(s,bm1,w).
map(s,bm2,s).
map(s,bm3,w).
map(s,fm1,w).
map(s,fm2,w).
map(s,fm3,w).
map(s,am11,e).
map(s,am12,e).
map(s,am21,e).
map(s,am22,e).
map(s,am31,e).
map(s,am32,e).
map(s,pm1,s).
map(s,pm2,s).
map(s,pm3,s).
map(s,im1,e).
map(s,msc1,e).

% m_w and m_s (s_w and s_s in the current draft)
in(E,m(X)) :- X=(s;w), in(E,m), map(s,E,X).

% l and u
map(l,b,27). map(l,a,24). map(l,p,24).
map(u,b,27). map(u,a,24). map(u,p,24).

% e
% in(fm1,e).

% n
#const n=4.