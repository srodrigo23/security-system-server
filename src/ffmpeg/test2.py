import cv2
import subprocess as sp
import numpy
import time

FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
    '-i', 'tiktok.mp4',
    '-an', '-sn',
    '-pix_fmt', 'bgr24',
    '-vcodec', 'rawvideo',
    '-vf', 'showinfo',
    '-f', 'image2pipe', 'pipe:1']

pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=1920 * 1080 * 3+3357)


while pipe.poll() is None:

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

    raw_image = pipe.stdout.read(1920 * 1080 * 3)
    info = pipe.stderr.read(3357)

    image1 = numpy.frombuffer(raw_image, dtype='uint8')
    image2 = image1.reshape((1080, 1920, 3))

    cv2.imshow('Video', image2)
    print(info)

    pipe.stdout.flush()
    pipe.stderr.flush()

pipe.terminate()

cv2.destroyAllWindows()