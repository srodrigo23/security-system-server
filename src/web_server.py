from flask import Flask, send_from_directory

# Flask Constructor
app = Flask(__name__)

cams = {}

cams['cam1'] = []
cams['cam2'] = []


__server__ = Flask(__name__)

   def run_forever(self):
        self.__server__.run(
            host=self.__host__,
            port=self.__port__
        )

    @__server__.route("/")
    def main_route(self):
        return 'This is a test'


if __name__ == "__main__":
    http_server = HTTPServer()
    http_server.run_forever()

# https: // www.geeksforgeeks.org/how-to-build-a-simple-android-app-with-flask-backend/
# decorator to associate a function with the url
# @app.route("/")
# def showHomePage():
# 	return "This is home page"

# @app.route('/video/<path:numstream>/hls_out.m3u8')
# def return_file(numstream):
# 	return send_from_directory(f'../live{numstream}', 'hls_out.m3u8')

# @app.route("/numcams")
# def return_num_cams():
#     return str(len(cams))

@app.route('/stream/<path:numstream>/<path:filename>')
def assets(numstream, filename):
	return send_from_directory(f'../live{numstream}', filename)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
