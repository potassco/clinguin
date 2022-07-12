import argparse
import importlib
import sys

def init():
    engines = []
    default_engine = 'server.application.standard_solver'


    parser = argparse.ArgumentParser(description = 'Clinguin is a GUI language extension for a logic program that uses Clingo.')

    parser.add_argument('--engine', type = str, nargs = '*', help = 'Optionally specify which engine(s) to use (seperate engines by \',\'')
    parser.add_argument('source_files', nargs = '+', help = 'Specify at least one source file')

    args = parser.parse_args()

    print(args.engine)
    print(args.source_files)

    import_error = False
    if args.engine == None or len(args.engine) == 0:
        # Load default engine (default_engine)
        module = None
        module_spec = importlib.util.find_spec(default_engine)
        if module_spec is not None:
            module = importlib.import_module(default_engine)
            engines.append(module)
        else:
            import_error = True
    else:
        # Go through all provided engines and load them
        for engine in args.engine:
            module = None
            module_spec = importlib.util.find_spec(engine)
            if module_spec is not None:
                module = importlib.import_module(engine)
                engines.append(module)
            else:
                import_error = True

    if import_error == True:
        print("Module import error")
        sys.exit(1)

    # TODO:
    # Load logic program
    
    return (None, engines)

