from server import Server
from settings import Settings

def run_server():
    """
    Method to run server from server.py
    """
    settings = Settings()
    server =  Server(settings)
    server.run()

if __name__ == "__main__":
    run_server()
