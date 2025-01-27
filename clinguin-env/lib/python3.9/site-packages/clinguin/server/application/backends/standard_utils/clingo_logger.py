"""
Clingo logger.
TODO
"""

from clingo import MessageCode


class ClingoLogger:
    """
    ClingoLogger Class.
    TODO
    """

    errors: list[str] = []

    @classmethod
    def logger(cls, msgC: MessageCode, errStr: str) -> None:
        """
        Adds a log.
        """
        print(msgC, " : ", errStr)
        cls.errors.append(errStr)

    @classmethod
    def errorString(cls):
        """
        Adds an error string.
        """
        return "\n".join(cls.errors)
