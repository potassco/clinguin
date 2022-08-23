from clinguin.utils import CaseConverter

class EndpointsHelper:

    @classmethod
    def callFunction(cls, backend, name, args, kwargs):
        found = False
        function = None

        snake_case_name = name
        camel_case_name = CaseConverter.snakeCaseToCamelCase(snake_case_name)


        if hasattr(backend, snake_case_name):
            function = getattr(backend, snake_case_name)
            found = True
        elif hasattr(backend, camel_case_name):
            function = getattr(backend, camel_case_name)
            found = True

        if found:
            result = function(*args, **kwargs)
            return result
        else:
            print('[CRITICAL] - Could not find function ' + name + ' in backend')

