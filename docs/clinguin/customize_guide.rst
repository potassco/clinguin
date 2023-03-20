Customize Guide
###############

This guide is for the people, that already have a special use case in mind, where the standard clinguin framework is not enough.

Idea
====

The idea regarding the extensibility of clinguin is, that one can tailor the program to ones needs. Clinguin was designed with this in mind, therefore several default backends are provided, which can be tailored to ones needs. For example take the ClingoBackend - the basic idea here is to do meta-reasoning about logic programs in terms of cautious-brave. The problem is, that this type of reasoning is simply not enough, e.g. take the example, where one now wants reason about graphs.

Example: Extending ClingoBackend with Clingraph
================================================

Now one wants to display graphs inside Clinguin. In general there exists the package Clingraph, where one can reason about graphs. Now the idea is to extend the ClingoBackend with some further functionality to get the ClingraphBackend. As the ClingraphBackend is already included in the `default_backends` we show you the necessary steps that are required to implement the same functionality by yourself.

The first step is to create a new folder any directory, **with one noteable exception**: If you downloaded the source of Clinguin **DO NOT** create the file inside any subfolder of `/clinguin` (where `/` is the root of the root of the source) and do not create the file in any parent of `/clinguin` (e.g. if you have the source located in `/home/test/my_prgs/clinguin/`, do not create the file in `/home`, `/home/test` or `/home/test/my_prgs` - but as an example something like `/home/my_backends/` would be perfectly fine). E.g. one could name this folder `test`.

Then one creates inside this `test` folder another folder, which is now assumed to be named `backends` and then inside this folder one has to create a file. The name of the file can be chosen as you want (we will assume `your_clingraph_backend.py` from here on).

The next step is to open the file, to import the `ClingoBackend` and create a class that inherits from this class. One can import `ClingoBackend` by specifying `from clinguin.server.application.backends import ClingoBackend` at the beginning of the file (in the default_backends ClingraphBackend we imported it with `from clinguin.server.application.backends.clingo_backend import ClingoBackend`, as the ClingraphBackend is also included in `backends` and we wanted to avoid cyclic imports).

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
2. Update the *uifb* (UI Factbase) (see below)
3. Generate the Json hierarchy (see below)

Step 1. is different for each policy, but steps 2. and 3. are basically the same for all (or most) policies. Step 2. says that it updates the *uifb*, where the uifb corresponds to an instance of the `UIFB` (see also the corresponding API documentation) class, which is basically a low-level tool, which directly accesses clingo-consequences to generate a factbase with the UI (one can think of it as a Clingo and CLORM (Clingo ORM) wrapper). This wrapper provides some functionality that is useful for various default Clinguin things, like computing the cautious/brave sets, etc.

So step 2. updates the UIFB and depending on the policy re-computes some answer-sets if needed. This is mostly done in the `ClingoBackend` `_update_uifb` method (see below). Step 3. takes than this updatd factbase and generates a Class-Hierarchy, that is Json-convertible, i.e. it uses the classes `ElementDto`, `AttributeDto` and `CallbackDto`, where each instance of the classes are Json convertible and form a hierarchy which corresponds to the graphical user interface. Step 3. is performed in the `get` method, take a look at the API for more information.

For now step 2. is important, more specifically the `_update_uifb_ui` method: So back to our idea of extending Clinguin with Clingraph. As in the `_update_uifb_ui` method one computes the ui facts with the the `ui-files` provided, it makes sense to **overwrite/extend this method to provide further functionality**. Note that the consequences of the source files used as inputwere previously calculated in the call to `_update_uifb_consequences`. What we do differently is we extract the consequences from the uifb object and use them to compute the graph with clingraph and then update the UI factbase with the base64 of the images as shown bellow.

.. code-block:: python

    def _update_uifb_ui(self):
        super()._update_uifb_ui()
        graphs = self._compute_clingraph_graphs(self._uifb.conseq_facts)
        if not self._disable_saved_to_file:
            self._save_clingraph_graphs_to_file(graphs)

        self._replace_uifb_with_b64_images(graphs)

The method `_compute_clingraph_graphs` takes use of the Clingraph API. It computes the graphs and saves them into an intermediate format:

.. code-block:: python

    def _compute_clingraph_graphs(self,prg):
        fbs = []
        ctl = Control("0")
        for f in self._clingraph_files:
            ctl.load(f)
        ctl.add("base",[],prg)
        ctl.add("base",[],self._backend_state_prg)
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

There is the possibility to save a graph to a file (only makes sense if you are in control of the Clinguin-Server), which is handled by the `_save_clingraph_graphs_to_file` method:

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

    def _image_to_b64(self, img):

        encoded = base64.b64encode(img)
        decoded = encoded.decode(self._encoding)

        return decoded

The next method searches through all attributes and looks up all the places, where the value starts with `clingraph__` and then takes everything that is after the `__` as a key for the graph. E.g. the default graph in clingraph is called `default`, so to display the default image one can specify it as `clingraph__default`. This value will then be replaced with the actual image. For the replacement the method first converts the graph into an image, then into a Base64 encoding and then replaces the value of the attribute.

.. code-block:: python

    def _replace_uifb_with_b64_images(self,graphs):
        for attribute in attributes:
            if str(attribute.key) != self._attribute_image_key:
                continue
            attribute_value = StandardTextProcessing.parse_string_with_quotes(str(attribute.value))
            is_cg_image = attribute_value.startswith(self._attribute_image_value) and attribute_value != "clingraph"
            if not is_cg_image:
                continue
            splits = attribute_value.split(self._attribute_image_value_seperator,1)
            if len(splits)<2:
                raise ValueError(f"The images for clingraph should have format {self._attribute_image_value}{self._attribute_image_value_seperator}name")
            graph_name = splits[1]
            key_image = self._create_image_from_graph(graphs, key = graph_name)
            base64_key_image = self._image_to_b64(key_image)
            new_attribute = AttributeDao(Raw(Function(str(attribute.id),[])), Raw(Function(str(attribute.key),[])), Raw(String(str(base64_key_image))))
            self._uifb._factbase.remove(attribute)
            self._uifb._factbase.add(new_attribute)

The full example can be found in `GitHub`_

.. _GitHub: <https://github.com/potassco/clinguin/tree/master/examples/clingraph/coloring>`
