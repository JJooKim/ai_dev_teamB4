import os
from django.shortcuts import HttpResponse, render, redirect

from .models import Youtube
from .forms import YoutubeForm

from .get_script import get_script 
from .get_sum_v import pgl_sum 
from .vid_sum import vid_sum 

from .Youtube import pre_processing 
from .Youtube.lower_fps import lower_frame 

from .scene_time import get_scene_time 
from .voice_time import get_voice_time 

# mainpage
def index_view(request):
    if request.method == 'POST':
        youtube_form = YoutubeForm(request.POST)

        if youtube_form.is_valid():
            youtube = youtube_form.save()
            return redirect('page1', url=youtube.url)
    else:
        youtube_form = YoutubeForm()

    return render(request, 'index.html', {'youtube_form': youtube_form})




# page1
def page1_view(request, url):
    # .mp4, .wav 생성
    v_path, a_path = pre_processing.saveVideo(url)

    # fps 줄인 .mp4 생성
    low_v_path = lower_frame(v_path, 5)
    
    ## cv
    video = pgl_sum(low_v_path)   # pgl_sum 결과(json) 반환
    vid_sum(video)  # pgl_sum 결과에 해당하는 영상 추출, 저장
    
    ## nlp
    script = get_script(a_path)  # whisper 결과(json) 반환


    ## Time line 받아오기
    # Scence Detect 타임 라인
    scene_time = get_scene_time(v_path) 
    # voice Detect 타임 라인 
    voice_time = get_voice_time(a_path) 

    ## summary..
    # kobart_result = get_kobart_result()
    

    # download 받은 영상 제거
    pre_processing.removeVideo(a_path)
    pre_processing.removeVideo(v_path)
    pre_processing.removeVideo(low_v_path)
  
    return render(request, 'page1.html', {'url': url, "script": script, "video": video, "scene_time": scene_time, "voice_time": voice_time})


