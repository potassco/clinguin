import logging


class Logger:

    instance = None 


    def __init__(self, name, reroute_default = False):
        log_file_path = "./logs/" + name + ".log"

        formatter = logging.Formatter('%(levelname)s<%(asctime)s>: %(message)s')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        with open(log_file_path, "a+") as file_object:
            file_object.write("<<<<<NEW-LOG-INSTANCE-" + name + ">>>>>\n\n")

        handler_f = logging.FileHandler(log_file_path)
        handler_f.setFormatter(formatter)

        handler_sh = logging.StreamHandler()
        handler_sh.setFormatter(formatter)

        self.logger.addHandler(handler_f)
        self.logger.addHandler(handler_sh)

        """
        if reroute_default:
            loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
            print(loggers)

            uvicorn_error = logging.getLogger("uvicorn.error")

            print(uvicorn_error.hasHandlers())
            
            uvicorn_error.addHandler(handler_sh)
            uvicorn_error.addHandler(handler_f)
            #uvicorn_error.disabled = True
            uvicorn_access = logging.getLogger("uvicorn.access")
            uvicorn_access.disabled = True

            uvicorn = logging.getLogger("uvicorn")
            print(uvicorn.hasHandlers())
            uvicorn = logging.getLogger("fastapi")
            print(uvicorn.hasHandlers())
            uvicorn = logging.getLogger()
            print(uvicorn.hasHandlers())
        """
 
             
            #default.addHandler(handler_f)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    
