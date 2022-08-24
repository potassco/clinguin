import logging

from clinguin.utils import CaseConverter, Logger

class EndpointsHelper:

    @classmethod
    def callFunction(cls, backend, name, args, kwargs):
        logger = logging.getLogger(Logger.server_logger_name)

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
            error_string = "Could not find function: " + name + " :in backend"
            logger.error(error_string)
            raise Exception(error_string)

