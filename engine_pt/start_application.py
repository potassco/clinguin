import uvicorn


from parse_input import ArgumentParser
from start_server import startServer

if __name__ == '__main__':
    parser = ArgumentParser()
    (logic_programs, engines) = parser.parse()

    startServer(logic_programs, engines)
else:
    print(app.test)
    

