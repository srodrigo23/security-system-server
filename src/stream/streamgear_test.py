from vidgear.gears import StreamGear # import required libraries

# Single Source Mode
# activate Single-Source Mode with valid video input
stream_params = {"-video_source": "../mediachibolos.mp4"} 
# stream_params = {"-video_source": 0, "-livestream": True} #doesn't work
# describe a suitable manifest-file location/name and assign params
streamer = StreamGear(output="dash_out.mpd", **stream_params)
# transcode source
streamer.transcode_source()
# terminate
streamer.terminate()