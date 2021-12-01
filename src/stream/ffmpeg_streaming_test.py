# https://abhitronix.github.io/vidgear/v0.2.1-stable/gears/streamgear/ffmpeg_install/
# https://pypi.org/project/python-ffmpeg-video-streaming/#requirements
# https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming#requirements

import ffmpeg_streaming
from ffmpeg_streaming import Formats

video = ffmpeg_streaming.input('../media/tiktok.mp4')
dash = video.dash(Formats.h264())
# dash.auto_generate_representations([1080, 720, 480])
dash.auto_generate_representations([480])
dash.generate_hls_playlist()
dash.output('./dash.mpd')