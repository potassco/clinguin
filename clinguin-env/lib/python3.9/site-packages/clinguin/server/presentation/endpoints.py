"""
Module for the Endpoints class.
"""

import logging
import traceback
from importlib.metadata import metadata

import clingo
from fastapi import APIRouter

from clinguin.utils import Logger

from ...utils import get_server_error_alert
from ...utils.logger import colored_text
from .backend_operation_dto import BackendOperationDto

# Self Defined
from .endpoints_helper import EndpointsHelper


class Endpoints:
    """
    The endpoints class define the available endpoints the backend
    (this time backend refers to the general concept of backend, like a server backend) has.
    These are defined in the ''__init__'', and correspond to the three methods:

    Methods:
        health -> Json : Returns name, version and description of clinguin.
        standard_executor -> Json : Returns the default GUI representation as Json that the Backend provides.
        operation_executor -> Json : Executes a operation defined by the Json passed with the Post request.
    """

    last_response = None

    def __init__(self, args) -> None:
        Logger.setup_logger(args.log_args, process="server")
        self._logger = logging.getLogger(args.log_args["name"])

        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.standard_executor, methods=["GET"])
        self.router.add_api_route("/backend", self.operation_executor, methods=["POST"])

        self._backend = args.backend(args)

    async def health(self):
        """
        Health endpoint (/health) of the server-backend,
        returns name, version and summary of clinguin.
        """
        self._logger.info("--> Health")
        cuin = metadata("clinguin")
        return {
            "name": cuin["name"],
            "version": cuin["version"],
            "description": cuin["summary"],
        }

    async def standard_executor(self):
        """
        Get endpoint (/) of the server-backend,
        calls the get() method of the respective backend (clinguin/clingo/clingraph/etc.).
        The get() method is implemented by every backend.
        """
        self._logger.info(colored_text("=>=>=>=>=>=>=>=>=> GET", "GREEN"))
        self._logger.info("%s get()", colored_text("-->", "GREEN"))
        try:
            json = self._backend.get()
            self.last_response = json
            self._logger.info(colored_text("--------------------", "GREEN"))
            return json
        except Exception as e:
            self._logger.error("Handling global exception in endpoint")
            self._logger.error(e)
            self._logger.error(traceback.format_exc())
            return get_server_error_alert(str(e), self.last_response)

    async def operation_executor(self, backend_call_string: BackendOperationDto):
        """
        Post endpoint (/backend) of the server-backend,
        which can be used to call specific methods/functions of the backend.
        It takes a backend_call_string, which is essentially a json defining a function to be called,
        including arguments.
        For example: {'function':'add_assumption(p(1),true)'}
        """

        self._logger.info(colored_text("=>=>=>=>=>=>=>=>=> POST", "GREEN"))

        try:
            try:
                symbol = clingo.parse_term(backend_call_string.function)
            except Exception as exc:
                msg = f"Could not parse {backend_call_string.function} into an atom."
                self._logger.error(msg)
                raise Exception(msg) from exc

            if symbol.type != clingo.SymbolType.Function:
                raise Exception(f"Operation {symbol} is not a function")

            # pylint: disable=protected-access
            if hasattr(backend_call_string, "context"):
                self._backend._set_context(backend_call_string.context)
            else:
                self._backend._set_context([])

            function_name = symbol.name
            operations = []
            if function_name == "":
                operations = symbol.arguments
            else:
                operations = [symbol]

            for p in operations:
                function_name = p.name

                function_arguments = list(map(str, p.arguments))

                call_args = ",".join(function_arguments)
                self._logger.info(
                    "%s %s(%s)", colored_text("-->", "GREEN"), function_name, call_args
                )

                EndpointsHelper.call_function(
                    self._backend, function_name, function_arguments, {}
                )

            self._logger.info(" get(%s)", colored_text("-->", "GREEN"))

            self.last_response = self._backend.get()
            self._logger.info(colored_text("--------------------", "GREEN"))
            return self.last_response

        except Exception as e:
            self._logger.error("Handling global exception in endpoint")
            self._logger.error(e)
            self._logger.error(traceback.format_exc())
            return get_server_error_alert(str(e), self.last_response)
