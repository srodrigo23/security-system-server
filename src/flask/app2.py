from flask import Flask, send_from_directory

# Flask Constructor
app = Flask(__name__)

#  
# https: // www.geeksforgeeks.org/how-to-build-a-simple-android-app-with-flask-backend/
# 
# decorator to associate
# a function with the url
@app.route("/")
def showHomePage():
	# response from the server
	return "This is home page"

@app.route('/video/dash.mpd')
def return_file():
	return send_from_directory('../ffmpeg/', 'dash.mpd')


@app.route('/video/<path:filename>')
def assets(filename):
	# Add custom handling here.
	# Send a file download response.
	return send_from_directory('../ffmpeg', filename)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
