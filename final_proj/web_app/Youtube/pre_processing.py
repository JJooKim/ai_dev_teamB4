import os

base_path = os.getcwd()
base_path = os.path.join(base_path, "web_app")
base_path = os.path.join(base_path, "Youtube")


import yt_dlp

def saveVideo(url):
    video_url = url
    video_dir = os.path.join(base_path, "Video")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': video_dir+'/youtube',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)

    ydl.download([video_url])
    

    return video_dir 

def removeVideo(file_path):
    os.remove(file_path)
