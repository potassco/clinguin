% attr(ID,ATTRNAME,ARGVALUE,VALUE)
% menu1.title("Sudoku")
attr(window,title,0,"Sudoku").


% element(ID,TYPE,PARENT_ID).  Perhaps we want parent as another predicare if not all UIS nee it
% menu1 = menu(parent=window)
element(menu1,menu,window).

% menu1.config(bgcolor=blue,fontcolor=white)
attr(menu1,cofig,bgcolor,blue).
attr(menu1,cofig,fontcolor,white).

% menu1.config(bgcolor=blue,fontcolor=white)
attr(menu1,grid,x,1).
attr(menu1,grid,y,1).


element(opt1,option,menu).
attr(opt1,??,label,"MyOption"). 

% One of the following. Perhaps there are also other things like on_clink vs on_hover 
attr(opt1,??,command,assert(mysymbol,true)).
% callback(opt1,assert(mysymbol,true)).


% Idea for interanl representation. Perhaps we also want it to be ordered by dependency
{window:{
    attr:{
        title:{
            0: "Sudoku"
        }
    }
},
elements:{
    menu1:{
        type: menu,
        parent: window,
        attr:{
            config:{
                bgcolor:blue,
                fontcolor:white
            },
            grid:{
                x:1,
                y:1
            }
        }

    },
    opt1:{
        type:option,
        parent:menu1,
        attr:{
            label: "Myoption".
            command: "assert(mysymbol,true)"     Perhaps the solver could have a function to map a symbol into a call "def call_by_symbol(symbol)". (This might be even better)
        }
    }

}


