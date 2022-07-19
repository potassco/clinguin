from clorm import Predicate, ConstantField, RawField, Raw

class AttributeDao(Predicate):
    id = RawField
    key = RawField
    value = RawField

    class Meta:
        name = "attribute"
 
