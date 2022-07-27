from clorm import Predicate, ConstantField, RawField, Raw, StringField


class ElementDao(Predicate):
    id = RawField
    type = RawField
    parent = RawField

    class Meta:
        name = "element"
