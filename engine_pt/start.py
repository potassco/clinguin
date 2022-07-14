from subprocess import Popen

import threading
import sys


from server_helper import start
from client_helper import start as cart

print(sys.argv)

server = threading.Thread(target=start)
client = threading.Thread(target=cart)

server.start()
client.start()

