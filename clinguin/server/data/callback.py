from clorm import Predicate, ConstantField, RawField, Raw


class CallbackDao(Predicate):
    id = RawField
    action = RawField
    policy = RawField

    class Meta:
        name = "callback"
