import torch
import os
from django.shortcuts import HttpResponse, render, redirect
from .models import Youtube
from .forms import YoutubeForm
import time
from .get_script import get_script
from .get_sum_v import pgl_sum
from .vid_sum import vid_sum
from .Youtube import pre_processing
from .Youtube.lower_fps import lower_frame

import logging

# mainpage
def index_view(request):
    if request.method == 'POST':
        youtube_form = YoutubeForm(request.POST)
        if youtube_form.is_valid():
            youtube = youtube_form.save()
            return redirect('loading_page', url=youtube.url)
    else:
        youtube_form = YoutubeForm()

    return render(request, 'index.html', {'youtube_form': youtube_form})

# page1
def page1_view(request, url):
    audio_path = pre_processing.saveVideo(url)

    audio_path = os.path.join(audio_path, "youtube.mp4")

    script = get_script(audio_path)

    

    video = pgl_sum(audio_path)


    pre_processing.removeVideo(audio_path)
  
    return render(request, 'page1.html', {'url': url, "script": script, "video": video})


#test_page
def test_page1_view(request, url):
    audio_path = pre_processing.saveVideo(url)
    time.sleep(1)
    vid_Complete = False
    original_audio_path = os.path.join(audio_path, "youtube_original.mp4")
    
    audio_path = os.path.join(audio_path, "youtube.mp4")

    #script = get_script(audio_path)

    #fps 줄이기
    lower_frame(original_audio_path, 5)
    
    #비디오 요약
    video = pgl_sum(audio_path)
    vid_Complete = vid_sum(video)
    
    #원본 비디오 삭제
    #time.sleep(3)
    #pre_processing.removeVideo(original_audio_path)
  
    return render(request, 'page1.html', {'url': url, "video":video})

def loading_page_view(request, url):
    audio_path = pre_processing.saveVideo(url)
    time.sleep(1)
    vid_Complete = False
    original_audio_path = os.path.join(audio_path, "youtube_original.mp4")

    audio_path = os.path.join(audio_path, "youtube.mp4")

    # script = get_script(audio_path)

    # fps 줄이기
    lower_frame(original_audio_path, 5)

    # 비디오 요약
    video = pgl_sum(audio_path)
    vid_Complete = vid_sum(video)

    # 원본 비디오 삭제
    # time.sleep(3)
    # pre_processing.removeVideo(original_audio_path)
    if vid_Complete:
        return render(request, 'page1.html', {'url': url, "video":video})

    return False