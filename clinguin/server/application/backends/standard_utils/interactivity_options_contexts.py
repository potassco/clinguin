import json

from clorm import Predicate, ConstantField, IntegerField, refine_field, combine_fields, StringField, FactBase
from typing import Any, Union

class Option_Context(Predicate):
    node = refine_field(ConstantField, ["node","edge"])
    id = combine_fields([ConstantField,IntegerField])
    type = refine_field(ConstantField, ["checkbox","text","select"]) # TODO: Add the other HTML input types.
    name = ConstantField
    value = combine_fields([ConstantField,IntegerField])

class User_Input(Predicate):
    node = refine_field(ConstantField, ["node","edge"])
    id = combine_fields([ConstantField,IntegerField])
    type = refine_field(ConstantField, ["checkbox", "text", "select"])  # TODO: Add the other HTML input types.
    name = ConstantField
    value = combine_fields([ConstantField,IntegerField])

class Select_Option(Predicate):
    name = ConstantField
    value = combine_fields([ConstantField,IntegerField])

class Select_Option_Class:
    def __init__(self, name:str, state:Any, options:[str]):
        self.name = name
        self.type = "select"
        self.state = state
        self.options = options


    def __eq__(self, other):
        if isinstance(other, Select_Option_Class):
            return other.name == self.name
        else:
            return False

    def toDict(self):
        return {"name":self.name, "type":self.type, "state":self.state, "options":self.options}

class Input_Option:
    def __init__(self, type:str, name:str, state:Any):
        self.type = type
        self.name = name
        self.state = state


    def __eq__(self, other):
        if isinstance(other, Input_Option):
            return other.name == self.name and other.type == self.type
        else:
            return False

    def toDict(self):
        return {"name":self.name, "type":self.type, "state":self.state}
class NodeOptions:
    def __init__(self, id: str, compType: str, options: list[Union[Input_Option,Select_Option_Class]]):
        self.id = id
        self.options = options
        self.compType = compType

    def addOption(self, option:Union[Input_Option,Select_Option_Class]) -> None:
        for selfOption in self.options:
            if selfOption == option:
                return

        self.options.append(option)

    def toDict(self):
        options_list = [option.toDict() for option in self.options]
        return {"id": self.id, "compType": self.compType, "options": options_list}


class OptionsList:
    def __init__(self, options: list[NodeOptions]):
        self.options = options

    def add(self, id:str, compType:str, option:Union[Input_Option,Select_Option_Class]):
        for opt in self.options:
            if opt.id == id:
                opt.addOption(option)
                return

        self.options.append(NodeOptions(str(id),compType, [option]))

    def toJson(self):
        jsonList = []
        for item in self.options:
            jsonItem = item.toDict()
            jsonList.append(jsonItem)

        return jsonList

def createOptionsList(atoms: FactBase) -> OptionsList:
    oL = OptionsList([])
    solution = atoms.query(Option_Context).select(Option_Context.id, Option_Context.name, Option_Context.type, Option_Context.value, Option_Context.node ).all()
    for s in solution:
        if s[2] == "select":
            selOpt_solutions = atoms.query(Select_Option).select(Select_Option.name, Select_Option.value).all()
            selOpts = []
            for o in selOpt_solutions:
                if o[0] == s[1]:
                    selOpts.append(o[1])
            oL.add(str(s[0]), s[4], Select_Option_Class(s[1], s[3], selOpts))
        else:
            oL.add(str(s[0]), s[4], Input_Option(s[2],s[1], s[3]))


    return oL

