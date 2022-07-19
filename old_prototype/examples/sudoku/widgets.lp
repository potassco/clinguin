% ------------------------------
% Window setup
window(minsize, width, 900).
window(minsize, height, 900).
window(title, 0, "Sudoku").
window(resizable, 0, 0).
window(resizable, 1, 0).

% ------------------------------
% Cautious models update after every change

% Make frames to define grid
widget(frame,f(X,Y),window):- pos(X,Y).
config(f(X,Y),bg,white):- subgrid(X,Y,S), S\2==0.
geo(f(X,Y),grid,row,X):- pos(X,Y).
geo(f(X,Y),grid,column,Y):- pos(X,Y).
config(f(X,Y),width,100):- pos(X,Y).
config(f(X,Y),height,100):- pos(X,Y).
config(f(X,Y),highlightbackground,black):- pos(X,Y).
config(f(X,Y),highlightthickness,1):- pos(X,Y).

% Make menu buttons
widget(menu,m(X,Y),f(X,Y)):- pos(X,Y).
config(m(X,Y),font,"Arial 16"):- pos(X,Y).
config(m(X,Y),width,1):- pos(X,Y).
config(m(X,Y),fg,gray):- pos(X,Y), initial(X,Y,_).
config(m(X,Y),bg,white):- subgrid(X,Y,S), S\2==0.
geo(m(X,Y),grid,column,X\3):- pos(X,Y).
geo(m(X,Y),grid,row,Y\3):- pos(X,Y).
geo(m(X,Y),grid,padx,25):- pos(X,Y).
geo(m(X,Y),grid,pady,37):- pos(X,Y).

% ------------------------------
% Brave models update after every chaange
opt(m(X,Y),V,sudoku(X,Y,V)):- sudoku(X,Y,V).

