import logging
import os

log_levels = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


class Logger:

    @classmethod
    def _getLogFilePath(ctl, log_arg_dict):
        log_file_path = os.path.join("logs",
            (log_arg_dict['timestamp'] + "-" + log_arg_dict['name'] + ".log"))
        return log_file_path

    @classmethod
    def _addShellHandlerToLogger(ctl, logger, log_arg_dict):
        shell_formatter = logging.Formatter(log_arg_dict['format_shell'])

        logger.setLevel(log_levels[log_arg_dict['level']])

        handler_sh = logging.StreamHandler()
        handler_sh.setFormatter(shell_formatter)

        logger.addHandler(handler_sh)

    @classmethod
    def _addFileHandlerToLogger(ctl, logger, log_arg_dict, log_file_path):
        file_formatter = logging.Formatter(log_arg_dict['format_file'])

        with open(log_file_path, "a+") as file_object:
            file_object.write(
                "<<<<<NEW-LOG-INSTANCE-" +
                log_arg_dict['name'] +
                ">>>>>\n\n")

        handler_f = logging.FileHandler(log_file_path)
        handler_f.setFormatter(file_formatter)
        logger.addHandler(handler_f)

    @classmethod
    def setupLogger(ctl, log_arg_dict):

        log_file_path = ctl._getLogFilePath(log_arg_dict)

        logger = logging.getLogger(log_arg_dict['name'])
        if not log_arg_dict['shell_disabled']:
            ctl._addShellHandlerToLogger(logger, log_arg_dict)
        if not log_arg_dict['file_disabled']:
            ctl._addFileHandlerToLogger(logger, log_arg_dict, log_file_path)

    @classmethod
    def setupUvicornLoggerOnStartup(ctl, log_arg_dict):
        # ----------------------------------------------------------
        # Remove handlers from uvicorn loggers

        logger = logging.getLogger("uvicorn.access")
        for handler in logger.handlers:
            logger.removeHandler(handler)

        logger = logging.getLogger("uvicorn.error")
        for handler in logger.handlers:
            logger.removeHandler(handler)

        logger = logging.getLogger("uvicorn")
        for handler in logger.handlers:
            logger.removeHandler(handler)

        # Add new handlers to top-level-uvicorn logger
        log_file_path = ctl._getLogFilePath(log_arg_dict)

        logger = logging.getLogger("uvicorn")
        if not log_arg_dict['shell_disabled']:
            ctl._addShellHandlerToLogger(logger, log_arg_dict)
        if not log_arg_dict['file_disabled']:
            ctl._addFileHandlerToLogger(logger, log_arg_dict, log_file_path)


