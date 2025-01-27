"""
Unsat Constraint Utilities
"""

import re
from typing import Dict, Optional, Sequence

import clingo
from clingo.ast import Location

from ..transformers import ConstraintTransformer, FactTransformer, OptimizationRemover
from ..utils import get_signatures_from_model_string
from .constants import UNSAT_CONSTRAINT_SIGNATURE


class UnsatConstraintComputer:
    """
    A container class that allows for a passed unsatisfiable program_string to identify the underlying constraints
    making it unsatisfiable
    """

    def __init__(
        self,
        control: Optional[clingo.Control] = None,
    ):
        self.control = control if control is not None else clingo.Control()
        self.program_transformed: Optional[str] = None
        self.initialized: bool = False

        self._file_constraint_lookup: Dict[int, clingo.ast.Location] = {}

    def parse_string(self, program_string: str) -> None:
        """
        Method to parse a provided program string
        """
        ct = ConstraintTransformer(UNSAT_CONSTRAINT_SIGNATURE, include_id=True)
        self.program_transformed = ct.parse_string(program_string)
        self._file_constraint_lookup = ct.constraint_location_lookup
        self.initialized = True

    def parse_files(self, files: Sequence[str]) -> None:
        """
        Method to parse a provided sequence of filenames
        """
        ct = ConstraintTransformer(UNSAT_CONSTRAINT_SIGNATURE, include_id=True)
        if not files:
            program_transformed = ct.parse_files("-")  # nocoverage
        else:
            program_transformed = ct.parse_files(files)

        # remove optimization statements
        optr = OptimizationRemover()
        program_transformed = optr.parse_string(program_transformed)

        self.program_transformed = program_transformed
        self._file_constraint_lookup = ct.constraint_location_lookup
        self.initialized = True

    def get_constraint_location(self, constraint_id: int) -> Optional[Location]:
        """
        Method to get the file that a constraint (identified by its `constraint_id`) is located in.
        """
        return self._file_constraint_lookup.get(constraint_id)

    def get_unsat_constraints(self, assumption_string: Optional[str] = None) -> Dict[int, str]:
        """
        Method to get the unsat constraints of an initialized `UnsatConstraintComputer` Object.
        """

        # only execute if the UnsatConstraintComputer was properly initialized
        if not self.initialized:
            raise ValueError(
                "UnsatConstraintComputer is not properly initialized. To do so call either `parse_files` "
                "or `parse_string`."
            )

        program_string = str(self.program_transformed)
        # if an assumption string is provided use a FactTransformer to remove interfering facts
        if assumption_string is not None and len(assumption_string) > 0:
            assumptions_signatures = get_signatures_from_model_string(assumption_string)
            ft = FactTransformer(signatures=assumptions_signatures)
            # first remove all facts from the programs matching the assumption signatures from the assumption_string
            program_string = ft.parse_string(program_string)
            # then add the assumed atoms as the only remaining facts
            program_string += "\n" + ". ".join(assumption_string.split()) + "."

        # add minimization soft constraint to optimize for the smallest set of unsat constraints
        minimizer_rule = f"#minimize {{1,X : {UNSAT_CONSTRAINT_SIGNATURE}(X)}}."
        program_string = program_string + "\n" + minimizer_rule

        # create a rule lookup for every constraint in the program associated with it's unsat id
        constraint_lookup = {}
        for line in program_string.split("\n"):
            id_re = re.compile(f"{UNSAT_CONSTRAINT_SIGNATURE}[(]([1-9][0-9]*)[)]")
            match_result = id_re.match(line)
            if match_result is None:
                continue
            constraint_id = match_result.group(1)
            constraint_lookup[int(constraint_id)] = (
                str(line).replace(f"{UNSAT_CONSTRAINT_SIGNATURE}({constraint_id})", "").strip()
            )

        self.control.add("base", [], program_string)
        self.control.ground([("base", [])])

        with self.control.solve(yield_=True) as solve_handle:
            model = solve_handle.model()
            unsat_constraint_atoms = []
            while model is not None:
                unsat_constraint_atoms = [
                    a for a in model.symbols(atoms=True) if a.match(UNSAT_CONSTRAINT_SIGNATURE, 1, True)
                ]
                solve_handle.resume()
                model = solve_handle.model()
            unsat_constraints: Dict[int, str] = {}
            for a in unsat_constraint_atoms:
                constraint_id = a.arguments[0].number
                constraint = str(constraint_lookup.get(constraint_id))
                unsat_constraints[constraint_id] = constraint

            return unsat_constraints
