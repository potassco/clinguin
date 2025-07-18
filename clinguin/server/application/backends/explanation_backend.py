"""
Module that contains the Explanation Backend.
"""

import textwrap
from functools import cached_property

from clingexplaid.mus import CoreComputer
from clingexplaid.preprocessors import AssumptionPreprocessor, FilterSignature
from clingo.script import enable_python

from clinguin.server.application.backends.clingo_backend import (
    ClingoBackend,
)
from clinguin.utils.annotations import extends


enable_python()


class ExplanationBackend(ClingoBackend):
    """
    Extends ClingoBackend. This backend will treat an UNSAT result by adding the
    Minimal Unsatisfiable Core (MUC) to the domain-state, thus allowing the UI to show
    the faulty assumptions.
    """

    # ---------------------------------------------
    # Properties
    # ---------------------------------------------

    @property
    def _assumption_list(self):
        """
        Gets the set of assumptions used for solving.
        It includes the assumptions from the assumption signatures provided.

        Warning:

            Overwrites :meth:`ClingoBackend._assumption_list`
        """
        return self._assumptions.union(self._assumptions_from_signature)

    # ---------------------------------------------
    # Initialization
    # ---------------------------------------------

    @extends(ClingoBackend)
    def _init_command_line(self):
        """
        Sets the assumption signature and the transformer used for the input files

        Attributes:
            _assumption_sig (List[Tuple[str, int]]): The list of assumption signatures
            _assumption_transformer (clingexplaid.AssumptionTransformer): The transformer used for the input files
        """
        super()._init_command_line()
        # pylint: disable= attribute-defined-outside-init
        self._assumption_sig = []
        for a in self._args.assumption_signature or []:
            try:
                name, arity = a.split(",")
                self._assumption_sig.append((name, int(arity)))
            except Exception as ex:
                raise ValueError(
                    "Argument assumption_signature must have format name,arity"
                ) from ex

    def _create_ctl(self) -> None:
        """
        Initializes the control object (domain-control).
        It is used when the server is started or after a restart.

        See Also:
            :func:`~_load_file`
        """
        super()._create_ctl()
        filters = {FilterSignature(s, a) for s, a in self._assumption_sig}
        # pylint: disable=attribute-defined-outside-init
        self._assumption_transformer = AssumptionPreprocessor(
            control=self._ctl,
            filters=filters,
        )

    @extends(ClingoBackend)
    def _init_ds_constructors(self):
        super()._init_ds_constructors()
        self._add_domain_state_constructor("_ds_mus")

    @extends(ClingoBackend)
    def _load_file(self, f):
        """
        Loads a file into the control. Transforms the program to add choices around assumption signatures.

        Arguments:
            f (str): The file path

        """
        self._logger.debug("Assumption transformer will process file %s", f)
        self._assumption_transformer.process_files([f])

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------
    @extends(ClingoBackend)
    def _ground(self, program="base", arguments=None):
        """
        Sets the list of assumptions that were taken from the input files using the assumption_signature.

        Attributes:
            _assumptions_from_signature (Set[Tuple(str,bool)]): The set of assumptions from the assumption signatures
            arguments (list, optional): The list of arguments to ground the program. Defaults to an empty list.
        """
        super()._ground(program, arguments)
        # pylint: disable= attribute-defined-outside-init
        self._assumptions_from_signature = list(
            self._assumption_transformer.assumptions
        )

    # ---------------------------------------------
    # Class methods
    # ---------------------------------------------

    @classmethod
    @extends(ClingoBackend)
    def register_options(cls, parser):
        """
        Registers command line options for ClingraphBackend.
        """
        ClingoBackend.register_options(parser)

        parser.add_argument(
            "--assumption-signature",
            help=textwrap.dedent(
                """\
                            Signatures that will be considered as true assumptions. Must be have format name,arity"""
            ),
            nargs="+",
            metavar="",
        )

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

    @cached_property
    def _ds_mus(self):
        """
        Adds information about the Minimal Unsatisfiable Set (MUS)
        Includes predicate ``_clinguin_mus/1`` for every assumption in the MUC
        It uses a cache that is erased after an operation makes changes in the control.
        """
        prg = "#defined _clinguin_mus/1. "
        if self._unsat_core is not None:
            self._logger.info("UNSAT Answer, will add explanation")
            mus_core = CoreComputer(self._ctl, self._assumption_list).shrink()
            prg += " ".join([f"_clinguin_mus({str(s)})." for s, _ in mus_core]) + "\n"
        return prg
