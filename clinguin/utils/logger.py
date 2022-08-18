import logging
import os
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

log_levels = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            color =  COLOR_SEQ % (30 + COLORS[levelname])
            levelname_color = color + levelname[0:4] + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

class Logger:

    @classmethod
    def _getLogFilePath(ctl, log_arg_dict):
        log_file_path = os.path.join("logs",
            (log_arg_dict['timestamp'] + "-" + log_arg_dict['name'] + ".log"))
        return log_file_path

    @classmethod
    def _addShellHandlerToLogger(ctl, logger, log_arg_dict):
        shell_formatter = ColoredFormatter(log_arg_dict['format_shell'])

        logger.setLevel(log_levels[log_arg_dict['level']])

        handler_sh = logging.StreamHandler()
        handler_sh.setFormatter(shell_formatter)

        logger.addHandler(handler_sh)

    @classmethod
    def _addFileHandlerToLogger(ctl, logger, log_arg_dict, log_file_path):
        file_formatter = ColoredFormatter(log_arg_dict['format_file'])

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


