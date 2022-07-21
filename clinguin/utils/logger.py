import logging

log_levels = {
    "NOTSET" : logging.NOTSET,
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARNING,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL
}

class Logger:
    
    @classmethod
    def _getLogFilePath(ctl, logger_config):
        log_file_path = "./logs/" + logger_config['timestamp'] + "-" + logger_config['name'] + ".log"
        return log_file_path

    @classmethod
    def _addShellHandlerToLogger(ctl, logger, logger_config):
        shell_formatter = logging.Formatter(logger_config['format_shell'])

        logger.setLevel(log_levels[logger_config['log_level']])

        handler_sh = logging.StreamHandler()
        handler_sh.setFormatter(shell_formatter)

        logger.addHandler(handler_sh)

    @classmethod
    def _addFileHandlerToLogger(ctl, logger, logger_config, log_file_path):
        file_formatter = logging.Formatter(logger_config['format_file'])

        with open(log_file_path, "a+") as file_object:
            file_object.write("<<<<<NEW-LOG-INSTANCE-" + logger_config['name'] + ">>>>>\n\n")

        handler_f = logging.FileHandler(log_file_path)
        handler_f.setFormatter(file_formatter)
        logger.addHandler(handler_f)




    @classmethod
    def setupLogger(ctl, logger_config):
        log_file_path = ctl._getLogFilePath(logger_config)

        logger = logging.getLogger(logger_config['name'])
        ctl._addShellHandlerToLogger(logger, logger_config)
        ctl._addFileHandlerToLogger(logger, logger_config, log_file_path)

    @classmethod
    def setupUvicornLoggerOnStartup(ctl, logger_config):
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
        log_file_path = ctl._getLogFilePath(logger_config)

        logger = logging.getLogger("uvicorn")
        ctl._addShellHandlerToLogger(logger, logger_config)
        ctl._addFileHandlerToLogger(logger, logger_config, log_file_path)


        

