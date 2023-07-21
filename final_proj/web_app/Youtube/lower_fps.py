from moviepy.editor import *


import os

base_path = os.getcwd()
base_path = os.path.join(base_path, "web_app")
base_path = os.path.join(base_path, "Youtube")


def lower_frame(video_path, fps):
    if fps==0:
        return 1
    clip = VideoFileClip(video_path)
    clip.write_videofile(video_path[:-13]+".mp4", fps=fps)
    clip.close()

    new_video_path = os.path.join(base_path,'youtube.mp4')
    return new_video_path