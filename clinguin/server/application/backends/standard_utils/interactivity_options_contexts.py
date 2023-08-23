# pylint: disable=R1705,W0622
"""
Module that supports the interactive clingraph.
"""
from typing import Any, Union

from clorm import (
    ConstantField,
    FactBase,
    IntegerField,
    Predicate,
    combine_fields,
    refine_field,
)


class Option_Context(Predicate):
    """
    A sort of DAO.
    """

    node = refine_field(ConstantField, ["node", "edge"])
    id = combine_fields([ConstantField, IntegerField])
    type = refine_field(ConstantField, ["checkbox", "text", "select"])
    name = ConstantField
    value = combine_fields([ConstantField, IntegerField])


class User_Input(Predicate):
    """
    A sort of DAO.
    """

    node = refine_field(ConstantField, ["node", "edge"])
    id = combine_fields([ConstantField, IntegerField])
    type = refine_field(ConstantField, ["checkbox", "text", "select"])
    name = ConstantField
    value = combine_fields([ConstantField, IntegerField])


class Select_Option(Predicate):
    """
    A sort of DAO.
    """

    name = ConstantField
    value = combine_fields([ConstantField, IntegerField])


class SelectOptionClass:
    """
    SelectOptionClass Class.
    """

    def __init__(self, name: str, state: Any, options: [str]):
        self.name = name
        self.type = "select"
        self.state = state
        self.options = options

    def __eq__(self, other):
        if isinstance(other, SelectOptionClass):
            return other.name == self.name
        else:
            return False

    def to_dict(self):
        """
        to_dict.
        """
        return {
            "name": self.name,
            "type": self.type,
            "state": self.state,
            "options": self.options,
        }


class InputOption:
    """
    InputOption Class.
    """

    def __init__(self, type: str, name: str, state: Any):
        self.type = type
        self.name = name
        self.state = state

    def __eq__(self, other):
        if isinstance(other, InputOption):
            return other.name == self.name and other.type == self.type
        else:
            return False

    def to_dict(self):
        """
        to_dict.
        """
        return {"name": self.name, "type": self.type, "state": self.state}


class NodeOptions:
    """
    NodeOptions Class.
    """

    def __init__(
        self,
        id: str,
        compType: str,
        options: list[Union[InputOption, SelectOptionClass]],
    ):
        self.id = id
        self.options = options
        self.compType = compType

    def addOption(self, option: Union[InputOption, SelectOptionClass]) -> None:
        """
        Adds an option.
        """
        for self_option in self.options:
            if self_option == option:
                return

        self.options.append(option)

    def to_dict(self):
        """
        to_dict.
        """
        options_list = [option.to_dict() for option in self.options]
        return {"id": self.id, "compType": self.compType, "options": options_list}


class OptionsList:
    """
    OptionsList Class.
    """

    def __init__(self, options: list[NodeOptions]):
        self.options = options

    def add(
        self, id: str, compType: str, option: Union[InputOption, SelectOptionClass]
    ):
        """
        Adds an option.
        """
        for opt in self.options:
            if opt.id == id:
                opt.addOption(option)
                return

        self.options.append(NodeOptions(str(id), compType, [option]))

    def to_json(self):
        """
        to_json.
        """
        jsonList = []
        for item in self.options:
            jsonItem = item.to_dict()
            jsonList.append(jsonItem)

        return jsonList


def createOptionsList(atoms: FactBase) -> OptionsList:
    """
    createOptionsList Function.
    """
    options_list = OptionsList([])
    solution = (
        atoms.query(Option_Context)
        .select(
            Option_Context.id,
            Option_Context.name,
            Option_Context.type,
            Option_Context.value,
            Option_Context.node,
        )
        .all()
    )
    for s in solution:
        if s[2] == "select":
            sel_opt_solutions = (
                atoms.query(Select_Option)
                .select(Select_Option.name, Select_Option.value)
                .all()
            )
            selOpts = []
            for o in sel_opt_solutions:
                if o[0] == s[1]:
                    selOpts.append(o[1])
            options_list.add(str(s[0]), s[4], SelectOptionClass(s[1], s[3], selOpts))
        else:
            options_list.add(str(s[0]), s[4], InputOption(s[2], s[1], s[3]))

    return options_list
