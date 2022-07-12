import uvicorn


from parse_input import init
from start_server import startServer

if __name__ == '__main__':
    (logic_programs, engines) = init()

    startServer(logic_programs, engines)
else:
    print(app.test)
    

