
def call_function(engines, name, args, kwargs):
    found = False
    function = None
    for engine in engines:
        if hasattr(engine, name):
            function = getattr(engine, name)
            found = True
            break
            
    if found == True:
        result = function(*args, **kwargs)
        return result
    else:
        print('[CRITICAL] - Could not find function ' + name + ' in solver')

