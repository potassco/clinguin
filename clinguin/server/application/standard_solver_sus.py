import networkx as nx
from typing import Sequence, Any

from clinguin.server.application.standard_json_encoder import StandardJsonEncoder
from clinguin.server.application.standard_json_encoder import StandardJsonEncoder
from clinguin.server.data.standard_clingo_solver.standard_clingo_solver import StandardClingoSolver

# Like an interface
class ClinguinBackend:

    @classmethod
    def _registerOptions(cls, parser):
        pass

    def _get(self):
        pass
    

class ClingoBackend(ClinguinBackend):

    def __init__(self, files):
        self.files = files
        self.ictl = InteractiveCtl()
        self.setUp()
        # self._instance = instance

        # self._clingo_solver = StandardClingoSolver(logic_programs, instance)
        # self._json_encoder = StandardJsonEncoder(instance)
        
        
    def _setUp(self):
        self.model = ClinguinModel()
        self.assumptions = set()
    
        # Maybe this part goes somewhere else, in an init
        self.ctl = Control()
        for f in files:
            self.ctl.load(str(f))
        self.ctl.ground([("base", [])])
        
        # self.brave_elements = ['dropdownmenuitem']

    @classmethod
    def _registerOptions(cls, parser):
        parser.add_argument('files', nargs = '+', help = 'Files')
        # any argument passsed here will be passed to the init on creation
        return ["files"] 
        # clinguin server -h
        # server --   
        # ClingoBackend:
        #     files: laksjsakds

        # ConfigBackend:
        #      name: sss

        # clinguin server --server=ClingoBackend filesl
        # clinguin server --server=ConfigBackend --name

        # clinguin client -h
        # server --   
        # TkinterUI:
        #     ksjaksjfklsa s s
        


    # becomes an endpoint option is the basic default one! instead of solve just get
    def _get(self) ->  Class_hierarchy:
        if self.model:
            return standard_json_encoder.encode(self.model)
        
        # Option 1
        # s = clt.solve(assumtions = self.assumptions)
        # self.model = ClinguinModel()
        # self.model.load_brave(s:SolveHandle)
        # self.model.load_cautious(s:SolveHandle)
        # s.close()

        self.model = ClinguinModel()
        self.model.computeBrave(ctrl, self.assumptions, lambda:s.name=='element' and s.args[0].name=='dropdownmenuitem')
        self.model.load_cautious(s:SolveHandle)
        s.close()



        # # Option 2
        # self.model = ClinguinModel()
        # self.model.load_tagged_brave_cautions(ctl, **kwargs)


        # # Option 3
        # self.model = ClinguinModel()
        # self.model.load_args_brave_cautions(ctl, ,brave_elements, **kwargs)

        return standard_json_encoder.encode(self.model)



    # becomes an endpoint option
    def assume(self, predicate) -> bool:
        # self._instance.logger.debug("assume(" + str(predicate) + ")")
        if predicate not in self.assumptions:
            self.assumptions.add(predicate)
        return self._get()
    
    # becomes an endpoint option
    def solve(self, predicate) -> bool:
        self.model = None
        return self._get()

    # becomes an endpoint option
    def remove(self, predicate) -> bool:
        self._instance.logger.debug("remove(" + str(predicate) + ")")
        if predicate in self.assumptions:
            self.assumptions.remove(predicate)
            self.assumptions.remove("assume(" + predicate + ")")
            self.model=None
        return self._get()

  

class ConfigBackend(ClingoBackend):

    def __init__(self, files, root_name):
        self.files = files
        self.root_name = root_name
        self.config_control = ConfigControl(files,root_name)
        return super(files)        

    @classmethod
    def _registerOptions(cls, parser):
        parser.add_argument('files', nargs = '+', help = 'Files')
        parser.add_argument('root_name', type = str, help = 'Name of the config')
        # any argument passsed here will be passed to the init on creation
        return ["files","root_name"] 

    # becomes an endpoint option is the basic default one! instead of solve just get
    def _get(self) ->  Class_hierarchy:
        
        if self.model:
            return standard_json_encoder.encode(self.model)
        
        self.model = ClinguinModel()
        model = self.config_control.get_ui()
        self.model.load_model(model)
        

        return standard_json_encoder.encode(self.model)
