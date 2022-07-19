from ast import arg
from clingo import Control
import clingo
import clorm
from clorm import Predicate, ConstantField, RawField, Raw
from clingo.symbol import Function, Number, String
import networkx as nx
import sys 


from tkinter import *


class Config(Predicate):
    id = RawField
    argument = RawField
    value = RawField

    class Meta:
        name = "config"

class Widget(Predicate):
    option = ConstantField
    id = RawField
    master = RawField

    class Meta:
        name = "widget"


class Option(Predicate):
    id = RawField
    value = RawField
    atom = RawField

    class Meta:
        name = "opt"

class Geo(Predicate):
    id = RawField
    option = ConstantField
    argument = RawField
    value = RawField

class Window(Predicate):
    option = ConstantField
    argument = RawField
    value = RawField

    class Meta:
        name = "window"


unifiers = [Config,Widget,Option,Geo,Window]

ctl = Control()

for f in sys.argv[1:]:
    ctl.load(str(f))

ctl.ground([("base", [])])



def get_val(s):
    if s.type == clingo.SymbolType.String:
        return s.string
    if s.type == clingo.SymbolType.Number:
        return s.number
    if s.type == clingo.SymbolType.Function:
        if s.name == "":
            return str(s)
        return s.name

def get_args(confs):
    args = {}
    kargs = {}
    for c in confs:
        arg = get_val(c.argument.symbol)
        if type(arg) == int:
            args[arg]= get_val(c.value.symbol)
        else:
            kargs[arg] = get_val(c.value.symbol)
    args_list = []
    pos = list(args.keys())
    pos.sort()
    for a in pos:
        args_list.append(args[a])

    return args_list, kargs

class ClinWidget():

    def __init__(self):
        self.brave_model = None
        self.widgets = {}
        self.assumptions = set()
        self.selected_var = {}
        self.window=Tk()
        self.update()
        self.window.mainloop()



    def set_select(self, w_id, val, ass):
        self.selected_var[w_id].set(val)
        self.assumptions.add(ass)
        self.update()


    def save_brave(self, model):
        self.brave_model= model.symbols(atoms=True,shown=True)

    def save_cautious(self, model):
        self.cautious_model= model.symbols(atoms=True,shown=True)

    def config_window(self,fb):
        q = fb.query(Window)
        q = q.group_by(Window.option)
        for name, window in q.all():
            args,kargs = get_args(window)
            getattr(self.window,name)(*args,**kargs)


    def create_widget(self, w_id, w_info, args, kargs):
        t = w_info['option']
        if str(w_info['master'].symbol)=='window':
            master = self.window
        else:
            master = self.widgets[w_info['master']]
        if t == "menu":
            self.selected_var[w_id]=StringVar(value=" ")
            widget = OptionMenu(
                master,
                self.selected_var[w_id],"")
            widget.config(**kargs)
            return widget
        if t=="frame":

            widget = Frame(master)
            widget.config(**kargs)
            # TODO this option should be general...
            widget.grid_propagate(0)
            return widget
        
        if t=="label":
            
            widget =  Label(master)
            widget.config(**kargs)
            return widget
        
        raise(RuntimeError(f"Wrong option {t}" ))


    def new_widget(self, fb, w_id, w_info):

        # Get creation options
        q = fb.query(Config).where(Config.id==w_id)
        
        args,kargs = get_args(q.all())
        widget = self.create_widget(w_id,w_info,args,kargs)

        # Place widget
        q = fb.query(Geo).where(Geo.id==w_id)
        q = q.group_by(Geo.option)
        q_list = list(q.all())
        if len(q_list)>1:
            raise(RuntimeError("Can only have one geo"))
        elif len(q_list)==0:
            widget.pack()
        else:
            for n in q.all():
                name = n[0]
                args,kargs = get_args(n[1])
                
                if name == 'grid':
                    widget.grid(*args,**kargs)
                elif name == 'place':
                    widget.place(*args,**kargs)
                elif name == 'pack':
                    widget.pack(*args,**kargs)
                else:
                    raise RuntimeError(f"Invalid geo {name}")
            
        return widget



            
    def update(self):
        self.create_layout()
        self.update_options()


    def update_options(self):
        ctl.configuration.solve.enum_mode = 'brave'
        ctl.solve(on_model=self.save_brave,assumptions=[(a,True) for a in list(self.assumptions)])
        prg = "\n".join([str(s)+"." for s in self.brave_model])
        fb = clorm.parse_fact_string(prg, unifiers)
        for id, w in self.widgets.items():
            if type(w)!=OptionMenu:
                continue
            if type(w['menu'])!=str:            
                w['menu'].delete(0,'end')
            q = fb.query(Option).where(Option.id==id)
            # Only menu
            q_list = list(q.all())
            for opt in q_list:
                v = get_val(opt.value.symbol)
                w["menu"].add_command(label=v,
                        command = lambda value=v, id=id, ass=opt.atom.symbol: 
                        self.set_select(id,value,ass))
            
            if len(q_list)==1:
                self.selected_var[id].set(get_val(q_list[0].value.symbol))

    def create_layout(self):
        # Get cautios model
        ctl.configuration.solve.enum_mode = 'cautious'
        ctl.solve(on_model=self.save_cautious,assumptions=[(a,True) for a in list(self.assumptions)])
        prg = "\n".join([str(s)+"." for s in self.cautious_model])
        fb = clorm.parse_fact_string(prg, unifiers)
        
        # Remove current widgets
        for w_id, w in self.widgets.items():
            w.destroy()
        
        self.config_window(fb)

        # Get widget dependency to define creation order
        q = fb.query(Widget)
        dependency = []
        widgets_info = {}        
        for w in fb.query(Widget).all():
            widgets_info[w.id]={'master':w.master,'option':w.option}
            dependency.append((w.id,w.master))
        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))
        
        # Create widgets in order
        for w_id in order:
            if (w_id==Raw(Function("window"))):
                continue

            w_info = widgets_info[w_id]
            #DO this with clorm class
            self.widgets[w_id] = self.new_widget(fb, w_id,w_info)
            



cw = ClinWidget()

    



