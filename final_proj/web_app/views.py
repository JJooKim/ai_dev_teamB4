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


from .scene_script import get_scene_script, get_scene_summary

import send_data

import pickle

# mainpage
def index_view(request):
    if request.method == 'POST':
        youtube_form = YoutubeForm(request.POST)

        if youtube_form.is_valid():
            youtube = youtube_form.save()
            url = youtube.url
            base_path = os.getcwd()
            data_path = os.path.join(base_path, "web_app", "Data")
            base_path = os.path.join(base_path, "web_app", "Youtube", request.session.session_key)


            # .mp4, .wav 생성, title 
            v_path, a_path, title = pre_processing.saveVideo(url, base_path)

            # fps 줄인 .mp4 생성
            low_v_path = lower_frame(v_path, 5)
            
            ## cv
            video = pgl_sum(low_v_path)   # pgl_sum 결과(json) 반환
            vid_sum(video, base_path)  # pgl_sum 결과에 해당하는 영상 추출, 저장
            
            ## nlp
            script = get_script(a_path)  # whisper 결과(json) 반환

            ## Time line 받아오기

            # Scene Detect 타임 라인
            scene_time = get_scene_time(v_path) 
            # Voice Detect 타임 라인 
            voice_time = get_voice_time(a_path) 

            # Scene, Voice, 타임라인 별 script & summary 반환
            
            scene_summary = get_scene_summary(script, scene_time)

            voice_summary = get_scene_summary(script, voice_time[0]['Voice Activity Detection based Timeline'])

            

            # download 받은 영상 제거
            pre_processing.removeVideo(a_path)
            pre_processing.removeVideo(v_path)
            pre_processing.removeVideo(low_v_path)

            # Save information as 
            save_data = {'title': title, 'url': url, 'whisper': script, 'scene_summary': scene_summary, 'voice_summary': voice_summary}

            file_path = os.path.join(base_path, 'data.pkl')
            data_path = os.path.join(data_path, "{}.pkl".format(title))

            with open(file_path, 'wb') as fp:
                pickle.dump(save_data, fp)
                print('dictionary saved successfully to file')

            with open(data_path, 'wb') as fp:
                pickle.dump(save_data, fp)
                print('accumulate script data')

            return redirect('page1')
    else:
        youtube_form = YoutubeForm()
    request.session.save()
    return render(request, 'index.html', {'youtube_form': youtube_form, 'key':request.session.session_key})



# page1
def page1_view(request):

    base_path = os.getcwd()
    base_path = os.path.join(base_path, "web_app", "Youtube", request.session.session_key)
    file_path = os.path.join(base_path, 'data.pkl')
    with open(file_path, 'rb') as fp:
        data = pickle.load(fp)

    page1_data = send_data.page1_data(data)

    """
    page1_data['full summary'] = ['---']
    page1_data['text'] = ['dlfkjsldkf','dfklsd', ...]
    page1_data['img'] = ['img1', 'img2', ...]
    page1_data['timeline'] = ['00:00:00-00:01:32', ...]
    """

      
    return render(request, 'page1.html', page1_data)


# page1
def page2_view(request):

    base_path = os.getcwd()
    base_path = os.path.join(base_path, "web_app", "Youtube", request.session.session_key)
    file_path = os.path.join(base_path, 'data.pkl')
    with open(file_path, 'rb') as fp:
        data = pickle.load(fp)

    """
    전체 스크립트
    timeline, script
    """
    page2_data = send_data.page2_data(data)

    return render(request, 'page2.html', page2_data)


# page1
def page3_view(request):

    base_path = os.getcwd()
    base_path = os.path.join(base_path, "web_app", "Youtube", request.session.session_key)
    file_path = os.path.join(base_path, 'data.pkl')
    with open(file_path, 'rb') as fp:
        data = pickle.load(fp)

    """
    img, 
    """
    page3_data = send_data.page3_data(data)
      
    return render(request, 'page3.html', page3_data)