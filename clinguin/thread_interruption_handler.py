import signal
import os

class ThreadInterruptionHandler:

    def signal_handler(signal_, frame):
        print("You pressed Ctrl+C! - Exiting now!")
        os.kill(os.getpid(), signal.SIGTERM)

    @classmethod
    def register_signal_handler(cls):
        signal.signal(signal.SIGINT, cls.signal_handler)
