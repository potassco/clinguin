
def callFunction(engines, name, args, kwargs):
    found = False
    function = None
    for engine in engines:
        if hasattr(engine, name):
            function = getattr(engine, name)
            found = True
            break

    if found:
        result = function(*args, **kwargs)
        return result
    else:
        print('[CRITICAL] - Could not find function ' + name + ' in backend')
