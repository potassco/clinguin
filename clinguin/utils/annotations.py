# import clinguin.server.application.backends
# from clinguin.server.application.backends import *

import sys


def extends(super_cls):
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


# def overwrites(func):

#     def wrapper(self, *args, **kwargs):
#         return func(self, *args, **kwargs)

#     cls_name = func.__qualname__.split(".")[0]
#     module_name = func.__module__
#     module = sys.modules[module_name]
#     cls = getattr(module, cls_name, None)

#     if cls is None:
#         raise KeyError(f"Class {cls_name} not found in module {module_name}")

#     super_cls = cls.__bases__[0].__name__
#     overwrite_str = f"""
#     Warning:
#         Overwrites :meth:`{super_cls}.{func.__name__}`
#     """
#     wrapper.__name__ = func.__name__
#     wrapper.__doc__ = (func.__doc__ or "") + overwrite_str

#     return wrapper


# import inspect


# def overwrites(func):
#     def wrapper(self, *args, **kwargs):
#         return func(self, *args, **kwargs)

#     cls = None
#     for cls_candidate in inspect.getmro(type(func.__globals__)):
#         if func.__name__ in cls_candidate.__dict__:
#             cls = cls_candidate
#             break

#     if cls is None:
#         raise KeyError(f"Class for method {func.__name__} not found")

#     super_cls = cls.__bases__[0].__name__
#     overwrite_str = f"""
#     Warning:
#         Overwrites :meth:`{super_cls}.{func.__name__}`
#     """
#     wrapper.__name__ = func.__name__
#     wrapper.__doc__ = (func.__doc__ or "") + overwrite_str

#     return wrapper


# # def overwrites(func):
# #     def wrapper(self, *args, **kwargs):
# #         return func(self, *args, **kwargs)

# #     cls = func.__qualname__.split(".")[0]
# #     super_cls = func.__globals__[cls].__bases__[0].__name__
# #     overwrite_str = f"""
# #     Warning:
# #         Overwrites :meth:`{super_cls}.{func.__name__}`
# #     """
# #     wrapper.__name__ = func.__name__
# #     wrapper.__doc__ = (func.__doc__ or "") + overwrite_str

# #     return wrapper


# # # def overwrites(func):
# # #     cls = None
# # #     cls = None

# # #     def wrapper(self, *args, **kwargs):
# # #         cls = type(self)
# # #         return func(self, *args, **kwargs)

# # #     overwrite_str = f"""
# # #         Warning:
# # #             {cls}
# # #             {cls.__bases__}
# # #             Overwrites :meth:`{func.__class__.__bases__[-1].__name__}.{func.__name__}`
# # #     """
# # #     wrapper.__name__ = func.__name__
# # #     wrapper.__doc__ = func.__doc__ + overwrite_str

# # #     return wrapper

# # #     # def overwrites(func):

# # #     #     def inner():
# # #     #         func()

# # #     #     help(func)
# # #     overwrite_str = f"""
# # #         Warning:
# # #             {func.__class__}
# # #             {func.__class__.__bases__}
# # #             Overwrites :meth:`{func.__class__.__bases__[-1].__name__}.{func.__name__}`
# # #     """


# # # #     inner.__name__ = func.__name__
# # # #     inner.__doc__ = func.__doc__ + overwrite_str
# # # #     return inner
