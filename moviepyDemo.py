# Video clip transformations using moviepy python3
# noqa: E402

import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import VideoFileClip
import cv2
import utils
import time
import datetime


def flip(image):
    """Flips an image vertically """
    return image[::-1]  # remember that image is a numpy array


clip = VideoFileClip("test_video.mp4")

# timer = Timer()
# timer.tic()
start = time.time()
# Transform video and perform image flip
new_clip = clip.fl_image(flip)
end = time.time()
total_time = (end - start)

# timer.toc()
# print( datetime.timedelta(seconds=clip.duration))

clip_len = time.strftime("%H:%M:%S", time.gmtime(clip.duration))
print((('Image flips took {:.3f}s for '
        '{} long video').format(total_time, clip_len)))


# Saves the frame at 1.2 sec
# clip1.save_frame("D:\\Computer-Vision\\Python-Practice\\
#                    video-frames\\frames1_2.jpeg", t=1.2) # Windows file path


# Write a video to a file
new_clip.write_videofile("test_output.mp4", audio=False)
