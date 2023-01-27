Customize Guide
###############

This guide is for the people, that already have a special use case in mind, where the standard clinguin framework is not enough.

Idea
====

The idea regarding the extensibility of clinguin is, that one can tailor the program to ones needs. Clinguin was designed with this in mind, therefore several default backends are provided, which can be tailored to ones needs. For example take the ClingoBackend - the basic idea here is to do meta-reasoning about logic programs in terms of cautious-brave. The problem is, that this type of reasoning is simply not enough, e.g. take the example, where one now wants reason about graphs.

Example: Extending ClingoBackend with Clingraph
======================================================

Now one wants to display graphs inside Clinguin. In general there exists the package Clingraph, where one can reason about graphs. Now the idea is to extend the ClingoBackend with some further functionality to get the ClingraphBackend. As the ClingraphBackend is already included in the `default_solvers` we show you the necessary steps that are required to implement the same functionality by yourself. 

The first step is to create a new folder any directory, **with one noteable exception**: If you downloaded the source of Clinguin **DO NOT** create the file inside any subfolder of `/clinguin` (where `/` is the root of the root of the source) and do not create the file in any parent of `/clinguin` (e.g. if you have the source located in `/home/test/my_prgs/clinguin/`, do not create the file in `/home`, `/home/test` or `/home/test/my_prgs` - but as an example something like `/home/my_backends/` would be perfectly fine). E.g. one could name this folder `test`. 

Then one creates inside this `test` folder another folder, which is now assumed to be named `backends` and then inside this folder one has to create a file. The name of the file can be chosen as you want (we will assume `your_clingraph_backend.py` from here on).
 
The next step is to open the file, to import the `ClingoBackend` and create a class that inherits from this class. One can import `ClingoBackend` by specifying `from clinguin.server.application.backends import ClingoBackend` at the beginning of the file (in the default_solvers ClingraphBackend we imported it with `from clinguin.server.application.backends.clingo_backend import ClingoBackend`, as the ClingraphBackend is also included in `backends` and we wanted to avoid cyclic imports).

The next step is to write our new backend, where we can e.g. start with:

.. code-block::

    class YourClingraphBackend(ClingoBackend):
        """
        TODO
        """

With this we get the whole functionality of ClingoBackend, to test if the class is recognised by Clinguin. For this we first navigate to the path of the file and then type:

.. code-block:: bash

    $ clinguin client-server --custom-classses "./backends" -h

Now we should get the help of the Clinguin application, where there is also the `--backend` option and in the text of this option there should now be the following line (assuming you don't have other Backends in this directory): `{ClingoBackend|ClingraphBackend|TemporalBackend|YourClingraphBackend}`.

If this is shown, then we can make our final test, that we did the above steps correctly (see below).

If this is not shown, then be sure that you are in the correct directory and that you correctly extended your own class - if this does not help, create a GitHub issue with the *EXACT* things you did, your system, etc.

Starting the Sudoku with *YourClingraphBackend*:
------------------------------------------------

For this we now assume that you copied the whole `/examples` folder into your current directory (the `test` directory from above). With these preconditions fulfilled one needs to specify one's own backend, this can be done by specifying both `--custom-classes` and `--backend`:


.. code-block:: bash

    $ clinguin client-server --custom-classes "./backends" --backend YourClingraphBackend --source-files examples/clingo/sudoku/instance.lp examples/clingo/sudoku/encoding.lp --ui-files examples/clingo/sudoku/ui.lp

Now Sudoku should open and it should work as expected. If not and you tripple checked that you did everything as specified above, create a GitHub issue with the *EXACT* things you did, your system, etc.

Extending the Class with command line arguments:
------------------------------------------------

A logical next step is to ask yourself what functionalities your extension should have and what kind of files/command line arguments you need for this. Therefore you can define custom command line options, that will get passed to your backend in the `__init__` method.

You can add additional cmd-arguments by overwriting the `register_options` method. As we want to keep the `ClingoBackend` arguments and just want to add your own arguments you can do the following:

.. code-block:: python 

    @classmethod
    def register_options(cls, parser):
        ClingoBackend.register_options(parser)

        # YOUR ARGUMENTS
        # parser is a argparse object (see https://docs.python.org/3/library/argparse.html)
        # ...
        # ...

To implement a very basic version of the ClingraphBackend you can copy-paste the following. In this version the only additional command line option is the option to specify the additional clingraph files (one can ignore most of the lines from the `__init__` method for now):

.. code-block:: python

    def __init__(self, args):
        super().__init__(args)

        self._clingraph_files = args.clingraph_files

        # Just defaults, that can be set in the ''real'' ClingraphBackend
        self._select_graph = "default"
        self._dir = "out"
        self._type = "graph"
        self._engine = "dot"
        self._disable_saved_to_file = True

        self._name_format = ""
        self._select_model = None

        # Some attributes for the automatic replacement
        self._intermediate_format = 'png'
        self._encoding = 'utf-8'
        self._attribute_image_key = 'image'
        self._attribute_image_value = 'clingraph'
        self._attribute_image_value_seperator = '__'

        # Important for later
        self._filled_model = None

    @classmethod
    def register_options(cls, parser):
        ClingoBackend.register_options(parser)

        parser.add_argument('--clingraph-files',
                        nargs='+',
                        metavar='')


As after every step you can now validate, if you did it right: Go into the directory where you executed `clinguin` previously and type the follwoing:

.. code-block:: bash

    $ clinguin client-server --custom-classes "./backends" --backend YourClingraphBackend -h

Again the help should show and now there should be a section at the bottom `YourClingraphBackend` where there are three arguments listed:

1. `--source-files` - From ClingoBackend
2. `--ui-files` - From ClingoBackend
3. `--clingraph-files` - You just added this one, congrats


Programming functionality into your class:
------------------------------------------

In order to program additional functionality, one must understand some basics of how the ClingoBackend works: ClingoBackend provides several policies (which can be extended by custom classes, for looking up what policies are look into the user guide and into the ClingoBackend-API-Documentation), where each policy de facto does the following things:

1. Execute the policy
2. Update the *model* (see below)
3. Generate the Json hierarchy (see below)

Step 1. is different for each policy, but steps 2. and 3. are basically the same for all (or most) policies. Step 2. says that it updates the *model*, where the model corresponds to an instance of the `ClinguinModel` (see also the corresponding API documentation) class, which is basically a low-level tool, which directly accesses clingo-models (one can think of it as a Clingo and CLORM (Clingo ORM) wrapper). This wrapper provides some functionality that is useful for various default Clinguin things, like computing the cautious/brave sets, etc.

So step 2. updates the ClinguinModel and depending on the policy re-computes some answer-sets if needed. This is mostly done in the `ClingoBackend` `_update_model` method (see below). Step 3. takes than this updatd model and generates a Class-Hierarchy, that is Json-convertible, i.e. it uses the classes `ElementDto`, `AttributeDto` and `CallbackDto`, where each instance of the classes are Json convertible and form a hierarchy which corresponds to the graphical user interface. Step 3. is performed in the `get` method, take a look at the API for more information.

For now step 2. is important, more specifically the `_update_model` method: So back to our idea of extending Clinguin with Clingraph. As in the `_update_model` method one computes the model which is then converted and sent back to the client, it makes sense to **overwrite/extend this method to provide further functionality**. In the normal ClingoBackend we call a ClinguinModel method which is called `from_widgets_file`, which is inturn just a wrapper for two other methods: `get_cautious_brave` and `from_widgets_file_and_program`. As we need the return value of `get_cautious_brave` we cannot just call the wrapper, therefore as a first step, we overwrite the `_update_model` with the following:

.. code-block:: python

    def _update_model(self):
        try:
            prg = ClinguinModel.get_cautious_brave(self._ctl,self._assumptions)
            self._model = ClinguinModel.from_widgets_file_and_program(self._ctl,self._ui_files,prg)
        except NoModelError:
            # Notifies the user by a popup, that this is not possible.
            self._model.add_message("Error","This operation can't be performed")


This would work the same as the default implementation, therefore now we can actually extend it: We are not going into the details of the individual methods here, so we just describe them a bit and you can copy paste them (don't forget to use the `updateModel` from below).

The method `computeClingraphGraphs` is called by `updateModel` and it takes use of the Clingraph API. It computes the graphs and saves them into an intermediate format:

.. code-block:: python

    def _compute_clingraph_graphs(self,prg):
        fbs = []
        ctl = Control("0")
        for f in self._clingraph_files:
            ctl.load(f)
        ctl.add("base",[],prg)
        ctl.ground([("base",[])],ClingraphContext())

        ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
        if self._select_model is not None:
            for m in self._select_model:
                if m>=len(fbs):
                    raise ValueError(f"Invalid model number selected {m}")
            fbs = [f if i in self._select_model else None
                        for i, f in enumerate(fbs) ]



        graphs = compute_graphs(fbs, graphviz_type=self._type)

        return graphs

There is the possibility to save a graph to a file (only makes sense if you are in control of the Clinguin-Server), which is handled by the `saveClingraphGraphsToFile` method:

.. code-block:: python
 
    def _save_clingraph_graphs_to_file(self,graphs):
        if self._select_graph is not None:
            graphs = [{g_name:g for g_name, g in graph.items() if g_name in self._select_graph} for graph in graphs]
        write_arguments = {"directory":self._dir, "name_format":self._name_format}
        paths = render(graphs,
                format='png',
                engine=self._engine,
                view=False,
                **write_arguments)
        self._logger.debug("Clingraph saved images:")
        self._logger.debug(paths)

The next method creates a binary image from a graph and returns it:

.. code-block:: python

    def _create_image_from_graph(self, graphs, position = None, key = None):
        graphs = graphs[0]

        if position is not None:
            if (len(graphs)-1) >= position:
                graph = graphs[list(graphs.keys())[position]]
            else:
                self._logger.error("Attempted to access not valid position")
                raise Exception("Attempted to access not valid position")
        elif key is not None:
            if key in graphs:
                graph = graphs[key]
            else:
                self._logger.error("Key not found in graphs: %s", str(key))
                raise Exception("Key not found in graphs: " + str(key))
        else:
            self._logger.error("Must either specify position or key!")
            raise Exception("Must either specify position or key!")

        graph.format = self._intermediate_format
        img = graph.pipe(engine=self._engine)

        return img

The next method might also interest you for other backends: It converts an image into a Base64 string encoding (which is basically just a String Encoded image, which can be send to the client, which you can use for other Graphics/Images). Note: One needs both `base64.b64encode` and `encoded.decode(self._encoding)` (where `self._encoding = utf-8`). 

.. code-block:: python

    def _convertImageToBase64String(self, img):

        encoded = base64.b64encode(img)
        decoded = encoded.decode(self._encoding)    

        return decoded

The next method searches through all attributes and looks up all the places, where the value starts with `clingraph__` and then takes everything that is after the `__` as a key for the graph. E.g. the default graph in clingraph is called `default`, so to display the default image one can specify it as `clingraph__default`. This value will then be replaced with the actual image. For the replacement the method first converts the graph into an image, then into a Base64 encoding and then replaces the value of the attribute.

.. code-block:: python

    def _get_mode_filled_with_base_64_images_from_graphs(self,graphs):
        model = self._model

        kept_symbols = list(model.get_elements()) + list(model.get_callbacks())

        filled_attributes = []

        # TODO - Improve efficiency of filling attributes
        for attribute in model.get_attributes():
            if str(attribute.key) == self._attribute_image_key:
                attribute_value = StandardTextProcessing.parse_string_with_quotes(str(attribute.value))

                if attribute_value.startswith(self._attribute_image_value) and attribute_value != "clingraph":
                    splits = attribute_value.split(self._attribute_image_value_seperator)
                    splits.pop(0)
                    rest = ""
                    for split in splits:
                        rest = rest + split

                    key_image = self._create_image_from_graph(graphs, key = rest)

                    base64_key_image = self._convertImageToBase64String(key_image)

                    filled_attributes.append(AttributeDao(Raw(Function(str(attribute.id),[])), Raw(Function(str(attribute.key),[])), Raw(String(str(base64_key_image)))))
                else:
                    filled_attributes.append(attribute)
            else:
                filled_attributes.append(attribute)

        return ClinguinModel(clorm.FactBase(copy.deepcopy(kept_symbols + filled_attributes)))

The next-to-last thing to do is to edit our `updateModel` method, as we need to call the methods above to provide the functionality. We need to add a `_filed_model` to distinfrontendsh between the models that are filled with the base64 string and those who are not (if we don't do this, we run into a mess with policies):

.. code-block:: python

    def _update_model(self):
        try:
            prg = ClinguinModel.get_cautious_brave(self._ctl,self._assumptions)
            self._model = ClinguinModel.from_widgets_file_and_program(self._ctl,self._ui_files,prg)

            graphs = self._compute_clingraph_graphs(prg)

            if not self._disable_saved_to_file:
                self._save_clingraph_graphs_to_file(graphs)

            self._filled_model = self._get_mode_filled_with_base_64_images_from_graphs(graphs)

        except NoModelError:
            self._model.add_message("Error","This operation can't be performed")

The last step is now to tell backend, that we actually want to send the `filled_model` back and not the `model`. This can be done by editing the `get` method:

.. code-block:: python

    def get(self):
        if not self._filled_model:
            self._update_model()

        json_structure = StandardJsonEncoder.encode(self._filled_model)
        return json_structure


The full example is shown at the end of the file, with this you can execute the coloring example by typing:

.. code-block:: bash
    
    $ clinguin client-server --custom-classes "./backends/" --backend YourClingraphBackend --source-files examples/clingraph/coloring/encoding.lp --ui-files examples/clingraph/coloring/ui.lp --clingraph-files examples/clingraph/coloring/viz.lp

Full Example:
-------------

.. code-block:: python

    from clinguin.server.data.attribute import AttributeDao

    from clinguin.server.data.clinguin_model import ClinguinModel
    from clinguin.server import StandardJsonEncoder

    from clinguin.server.application.backends import ClingoBackend

    from clinguin.utils import NoModelError

    class YourClingraphBackend(ClingoBackend):
        """
        TODO
        """

        def __init__(self, args):
            super().__init__(args)

            self._clingraph_files = args.clingraph_files

            # Just defaults, that can be set in the ''real'' ClingraphBackend
            self._select_graph = "default"
            self._dir = "out"
            self._type = "graph"
            self._engine = "dot"
            self._disable_saved_to_file = True

            self._name_format = ""
            self._select_model = None

            # Some attributes for the automatic replacement
            self._intermediate_format = 'png'
            self._encoding = 'utf-8'
            self._attribute_image_key = 'image'
            self._attribute_image_value = 'clingraph'
            self._attribute_image_value_seperator = '__'


            # Important for later
            self._filled_model = None

        @classmethod
        def register_options(cls, parser):
            ClingoBackend.register_options(parser)

            parser.add_argument('--clingraph-files',
                            nargs='+',
                            metavar='')

        def get(self):
            if not self._filled_model:
                self._update_model()

            json_structure = StandardJsonEncoder.encode(self._filled_model)
            return json_structure

        def _update_model(self):
            try:
                prg = ClinguinModel.get_cautious_brave(self._ctl,self._assumptions)
                self._model = ClinguinModel.from_widgets_file_and_program(self._ctl,self._ui_files,prg)

                graphs = self._compute_clingraph_graphs(prg)

                if not self._disable_saved_to_file:
                    self._save_clingraph_graphs_to_file(graphs)

                self._filled_model = self._get_mode_filled_with_base_64_images_from_graphs(graphs)

            except NoModelError:
                self._model.add_message("Error","This operation can't be performed")



        def _compute_clingraph_graphs(self,prg):
            fbs = []
            ctl = Control("0")
            for f in self._clingraph_files:
                ctl.load(f)
            ctl.add("base",[],prg)
            ctl.ground([("base",[])],ClingraphContext())

            ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
            if self._select_model is not None:
                for m in self._select_model:
                    if m>=len(fbs):
                        raise ValueError(f"Invalid model number selected {m}")
                fbs = [f if i in self._select_model else None
                            for i, f in enumerate(fbs) ]



            graphs = compute_graphs(fbs, graphviz_type=self._type)

            return graphs

        def _save_clingraph_graphs_to_file(self,graphs):
            if self._select_graph is not None:
                graphs = [{g_name:g for g_name, g in graph.items() if g_name in self._select_graph} for graph in graphs]
            write_arguments = {"directory":self._dir, "name_format":self._name_format}
            paths = render(graphs,
                    format='png',
                    engine=self._engine,
                    view=False,
                    **write_arguments)
            self._logger.debug("Clingraph saved images:")
            self._logger.debug(paths)

        def _create_image_from_graph(self, graphs, position = None, key = None):
            graphs = graphs[0]

            if position is not None:
                if (len(graphs)-1) >= position:
                    graph = graphs[list(graphs.keys())[position]]
                else:
                    self._logger.error("Attempted to access not valid position")
                    raise Exception("Attempted to access not valid position")
            elif key is not None:
                if key in graphs:
                    graph = graphs[key]
                else:
                    self._logger.error("Key not found in graphs: %s", str(key))
                    raise Exception("Key not found in graphs: " + str(key))
            else:
                self._logger.error("Must either specify position or key!")
                raise Exception("Must either specify position or key!")

            graph.format = self._intermediate_format
            img = graph.pipe(engine=self._engine)

            return img

        def _convertImageToBase64String(self, img):

            encoded = base64.b64encode(img)
            decoded = encoded.decode(self._encoding)

            return decoded
        def _get_mode_filled_with_base_64_images_from_graphs(self,graphs):
            model = self._model

            kept_symbols = list(model.get_elements()) + list(model.get_callbacks())

            filled_attributes = []

            # TODO - Improve efficiency of filling attributes
            for attribute in model.get_attributes():
                if str(attribute.key) == self._attribute_image_key:
                    attribute_value = StandardTextProcessing.parse_string_with_quotes(str(attribute.value))

                    if attribute_value.startswith(self._attribute_image_value) and attribute_value != "clingraph":
                        splits = attribute_value.split(self._attribute_image_value_seperator)
                        splits.pop(0)
                        rest = ""
                        for split in splits:
                            rest = rest + split

                        key_image = self._create_image_from_graph(graphs, key = rest)

                        base64_key_image = self._convertImageToBase64String(key_image)

                        filled_attributes.append(AttributeDao(Raw(Function(str(attribute.id),[])), Raw(Function(str(attribute.key),[])), Raw(String(str(base64_key_image)))))
                    else:
                        filled_attributes.append(attribute)
                else:
                    filled_attributes.append(attribute)

            return ClinguinModel(clorm.FactBase(copy.deepcopy(kept_symbols + filled_attributes)))


