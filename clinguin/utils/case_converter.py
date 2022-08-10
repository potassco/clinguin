
class CaseConverter:

    @classmethod
    def snakeCaseToCamelCase(cls, snake_case):
        components = snake_case.split('_')

        return components[0] + ''.join(x.title() for x in components[1:]) 


