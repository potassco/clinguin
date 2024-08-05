"""
Annotations used to express overwrites and extensions of methods.
They enhance documentation and help to understand the code.
"""


def extends(super_cls):
    """
    Decorator to indicate that a method extends a method of a super class.
    Args:
        super_cls (_type_): The super class.
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = (
            (func.__doc__ or "")
            + f"""
        Important:
            Extends :meth:`{super_cls.__name__}.{func.__name__}`
        """
        )
        return wrapper

    return decorator


def overwrites(super_cls):
    """
    Decorates a method to indicate that it overwrites a method of a super class.
    Args:
        super_cls (_type_): The super class.
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = (
            (func.__doc__ or "")
            + f"""
        Important:
            Overwrites :meth:`{super_cls.__name__}.{func.__name__}`
        """
        )
        return wrapper

    return decorator
