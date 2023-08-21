import logging

from clingo import MessageCode

class ClingoLogger:

    errors: list[str] = []

    @classmethod
    def logger(cls,msgC:MessageCode, errStr:str) -> None:
        print(msgC, " : ", errStr)
        cls.errors.append(errStr)

    @classmethod
    def errorString(cls):
        return "\n".join(cls.errors)