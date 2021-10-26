from server import Server
from settings import Settings

from multiprocessing import Process

from flask import Flask as f

def run_server():
    """
        Method to run server from server.py
    """
    settings = Settings()
    server =  Server(settings)
    server.run()

if __name__ == "__main__":
    run_server()

    proc = Process(target=start_process, args=(x,))
    proc.start()