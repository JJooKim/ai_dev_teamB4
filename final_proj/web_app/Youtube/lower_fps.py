from moviepy.editor import *

def lower_frame(video_path, fps):
    if fps==0:
        return 1
    clip = VideoFileClip(video_path)
    clip.write_videofile(video_path[:-13]+".mp4", fps=fps)