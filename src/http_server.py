from flask import Flask

__server__ = Flask(__name__)

        
    def run_forever(self):
        self.__server__.run(
            host = self.__host__, 
            port = self.__port__
        )
    @__server__.route("/")
    def main_route(self):
        return 'This is a test'


if __name__ == "__main__":
    http_server = HTTPServer()
    http_server.run_forever()
