
class StandardTextProcessing:

    @classmethod
    def parseStringWithQuotes(ctl, text):
        if len(text) > 0:
            if text[0] == "\"":
                text = text[1:]
        if len(text) > 0:
            if text[len(text)-1] == "\"":
                text = text[:-1]

        return text
 
