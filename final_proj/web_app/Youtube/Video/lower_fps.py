from moviepy.editor import *
base_path = os.getcwd()
base_path = os.path.join(base_path, "web_app", "Youtube", "Video")
clip = VideoFileClip(base_path+"/youtube.mp4")
clip.write_videofile(base_path+'/youtube_changed.mp4', fps=5)