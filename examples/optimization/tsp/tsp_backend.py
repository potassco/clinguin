from clinguin.server.application.default_backends.clingraph_backend import *
from clingo import Symbol, Number

class TspBackend(ClingraphBackend):

    # Computes the set difference between the brave and cautious model.
    def doSetDifference(self, brave_model, cautious_model):

        brave_cautious_difference = []

        for b in brave_model:
            found = False

            for c in cautious_model:
                if str(b) == str(c):
                    found = True
                    break

            if not found:
                brave_cautious_difference.append(b)

        return brave_cautious_difference

    # Very inefficient but does it's job
    def calculateCautiousCost(self, cautious_model):
        cost = 0
        for c in cautious_model:
            if str(c.name) == "selected":
                v0 = str(c.arguments[0])
                v1 = str(c.arguments[1])
                for c2 in cautious_model:
                    if str(c2.name) == "weight":
                        v0_w = str(c2.arguments[0])
                        v1_w = str(c2.arguments[1])
                        
                        if v0 == v0_w and v1 == v1_w:
                            cost = cost + int(str(c2.arguments[2]))
                            

                        
                #for c2 in cautious_model:
            #print(c)

        symb = Function("_cautious_cost", [Number(cost)])
    

        print(cost)
        print(symb)
        return symb        
        

    def _update_model(self):
        super()._update_model()
        try:

            ctl = self._ctl
            assumptions = self._assumptions

            model = ClinguinModel()
            
            cautious_model = model.compute_cautious(ctl, assumptions)
            cautious_model.append(self.calculateCautiousCost(cautious_model))

            brave_model = model.compute_brave(ctl, assumptions)
            brave_cautious_difference = self.doSetDifference(brave_model, cautious_model)
            # c_prg = self.tag_cautious_prg(cautious_model)
            c_prg = model.symbols_to_prg(cautious_model)
            b_prg = model.tag_brave_prg(brave_model)
            bcd_prg = model.tag(brave_cautious_difference, "_bcd")
            bcd_prg = model.symbols_to_prg(bcd_prg)

            atom_prg = model.tag(self._atoms, "_atom")
            atom_prg = model.symbols_to_prg(atom_prg)

            assumption_prg = model.tag(self._assumptions, "_assumption")
            assumption_prg = model.symbols_to_prg(assumption_prg)

            print("assumptions:")
            print(assumption_prg)


            #prg = ClinguinModel.getCautiosBrave(self._ctl,self._assumptions)
            prg = c_prg + b_prg + bcd_prg + atom_prg + assumption_prg

            self._model = ClinguinModel.from_widgets_file_and_program(self._ctl,self._widget_files,prg)

            graphs = self._compute_clingraph_graphs(prg)

            self._save_clingraph_graphs_to_file(graphs)

            self._filled_model = self._get_mode_filled_with_base_64_images_from_graphs(graphs)

        except NoModelError:
            self._model.add_message("Error","This operation can't be performed")

    def saveBest(self, m):
        self._best = m.symbols(shown=True, atoms=False)

    def addBestToAtoms(self, cautious, best):
        for b in best:
            if str(b.name) == "selected":
                v0 = b.arguments[0]
                v1 = b.arguments[1]
                found = False

                for c in cautious:
                    if str(c.name) == "selected":
                        v0_c = c.arguments[0]
                        v1_c = c.arguments[1]
                        if str(v0) == str(v0_c) and str(v1) == str(v1_c):
                            found = True
                            break

                # If b in best but not in cautious, then add:
                if not found:
                    self._assumptions.add(b) 

    def findMinimum(self):

        # Get Cautiuos
        ctl = self._ctl
        assumptions = self._assumptions
        model = ClinguinModel()
        cautious = model.compute_cautious(ctl, assumptions)

        # Get Best Model
        self._init_ctl()
        self._ctl.add("base",[],"#minimize{C:cost(C)}.")
        self._ground()
        self._ctl.solve(on_model=lambda m:self.saveBest(m))
        best = list(self._best)
        

        self.addBestToAtoms(cautious, best)
        print("WORKED!")

        self._init_ctl()
        self._ground()
 
        self._update_model()

        return self.get()


