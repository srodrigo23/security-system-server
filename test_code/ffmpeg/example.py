import time
import multiprocessing as mp
import numpy as np
import random
import subprocess as sp
import cv2
import os

# HLS DAHS Streaming
# https://www.fatalerrors.org/a/live-streaming-with-python.html

# Define the templates required for opencv
# template_path = "./high_img_template.jpg"

# Define the variables to be displayed by the rectangle
# category = "Category:      board"

# var_confidence = (np.random.randint(86, 98)) / 100
# Confidence = "Confidence:     " + str(var_confidence)

# var_precision = round(random.uniform(98, 99), 2)
# Precision = "Precision:    " + str(var_precision) + "%"

# product_yield = "Product Yield:  100%"

# result = "Result: perfect"


# Read the template and get the height and width of the template
# template = cv2.imread(template_path, 0)
# h, w = template.shape[:2]
# Define template matching function
def template_match(img_rgb):
    # Gray scale conversion
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # template matching
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # Set threshold
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]):
        # This is a direct fixed area
        cv2.rectangle(img_rgb, (155, 515), (1810, 820), (0, 0, 255), 3)
        cv2.putText(img_rgb, category, (240, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img_rgb, Confidence, (240, 640), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img_rgb, Precision, (240, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img_rgb, product_yield, (240, 720), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img_rgb, result, (240, 780), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
    return img_rgb


# Video properties
size = (1920, 1080)
sizeStr = str(size[0]) + 'x' + str(size[1])
# fps = cap.get(cv2.CAP_PROP_FPS)  # 30p/self
# fps = int(fps)
fps = 11
hz = int(1000.0 / fps)
print ('size:'+ sizeStr + ' fps:' + str(fps) + ' hz:' + str(hz))

rtmpUrl = 'rtmp://localhost/hls/test'
# Live pipeline output
# ffmpeg push rtmp key: sharing data through pipeline
command = ['ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', sizeStr,
    '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    rtmpUrl]
#Pipeline property configuration
# pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
pipe = sp.Popen(command, stdin=sp.PIPE) #,shell=False
# pipe.stdin.write(frame.tostring())

# Save pictures as local video
save_path = "./res_imgs"
if os.path.exists(save_path):
    os.makedir(save_path)

def image_get(q):
    while True:
        # start = time.time()
        #flag += 1
        time.sleep(0.5)
        frame = q.get()
        # frame = template_match(frame) #original
        # end = time.time()
        # print("the time is", end-start)
        cv2.imshow("frame", frame)
        cv2.waitKey(0)
        # pipe.stdin.write(frame.tostring())
        #cv2.imwrite(save_path + "%d.jpg"%flag,frame)
        
def image_put(q):
    # Take local video verification
    # cap = cv2.VideoCapture("./new.mp4")
    # Take the form of video streaming
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

    if cap.isOpened():
        print('success-------')
    else:
        print('faild')
    while True:
        q.put(cap.read()[1])
        time.sleep(0.5)
        q.get() if q.qsize() > 1 else time.sleep(0.01)

# Multithreading a camera
def run_single_camera():
    # initialization
    # multiprocesing
    mp.set_start_method(method='spawn')  # init
    # queue
    queue = mp.Queue(maxsize=2)
    processes = [mp.Process(target=image_put, args=(queue, )),
                 mp.Process(target=image_get, args=(queue, ))]

    [process.start() for process in processes]
    [process.join() for process in processes]

def run():
    run_single_camera()  # quick, with 2 threads

if __name__ == '__main__':
    run()