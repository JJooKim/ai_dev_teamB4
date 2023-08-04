import os
from django.shortcuts import HttpResponse, render, redirect

from .models import Youtube
from .forms import YoutubeForm

from .get_script import get_script 
from .get_sum_v import pgl_sum 
from .vid_sum import vid_sum, vid_sum_from_scene, vid_sum_from_voice, voice_image

from .Youtube import pre_processing 
from .Youtube.lower_fps import lower_frame 

from .scene_time import get_scene_time 
from .voice_time import get_voice_time 


from .scene_script import get_scene_script, get_scene_summary

from .send_data import page1_data, page2_data, page3_data

import pickle, shutil
# mainpage
def index_view(request):
    #세션 생성 및 저장
    try:
        request.session.save()
    except:
        request.session['']=''
        request.session.save()

    #index 진입 시 사용자 디렉토리 삭제(초기화)
    base_path=os.getcwd()
    base_path=os.path.join(base_path, 'web_app', 'static', request.session.session_key)
    
    try:
        shutil.rmtree(base_path)
    except:
        pass
    

    if request.method == 'POST':
        youtube_form = YoutubeForm(request.POST)

        if youtube_form.is_valid():
            youtube = youtube_form.save()
            url = youtube.url
            base_path = os.getcwd()
            base_path = os.path.join(base_path, "web_app", "static", request.session.session_key)

            # .mp4, .wav 생성, title 
            v_path, a_path, title, length = pre_processing.saveVideo(url, base_path)

            # fps 줄인 .mp4 생성
            low_v_path = lower_frame(v_path, 5)
            
            ## cv
            video = pgl_sum(low_v_path)   # pgl_sum 결과(json) 반환
            vid_sum(video, base_path)  # pgl_sum 결과에 해당하는 영상 추출, 저장
            
            ## nlp
            script = get_script(a_path)  # whisper 결과(json) 반환

            ## Time line 받아오기

            # Scene Detect 타임 라인
            scene_time = get_scene_time(v_path, length) 
            vid_sum_from_scene(scene_time,base_path)
            # Voice Detect 타임 라인 
            voice_time = get_voice_time(a_path)
            

            # Scene, Voice, 타임라인 별 script & summary 반환
            
            scene_summary = get_scene_summary(script, scene_time)

            voice_summary = get_scene_summary(script, voice_time[0]['Voice Activity Detection based Timeline'])
            vid_sum_from_voice(voice_time, base_path)
            voice_image(voice_time,base_path)
    #        [{'Voice Activity Detection based Timeline': [{'start': 0, 'end': 13}, {'start': 33, 'end': 63}]}]

            # Save information as 
            save_data = {'title': title, 'url': url, 'whisper': script, 'scene_summary': scene_summary, 'voice_summary': voice_summary}
            #save_data{'cut_youtube', 'scene_gif', 'scene_youtube', 'sum_gif', 'voice_gif', 'voice_youtube'}
            #생성한 파일 리스트 딕셔너리에 추가
            save_data.update(pre_processing.return_file_name_dict(request.session.session_key))
            save_data['key']=request.session.session_key
            file_path = os.path.join(base_path, 'data.pkl')
            with open(file_path, 'wb') as fp:
                pickle.dump(save_data, fp)

            title=title.replace('/','').replace('\\','').replace('|','')

            pkl_path = os.getcwd()
            pkl_path=os.path.join(pkl_path, "web_app", "Data", title)
            pkl_path=pkl_path+'.pkl'
            with open(pkl_path, 'wb') as fp:
                pickle.dump(save_data, fp)

            '''
            # download 받은 영상 제거
            pre_processing.removeVideo(a_path)
            pre_processing.removeVideo(v_path)
            pre_processing.removeVideo(low_v_path)
            '''

            return redirect('page1')
    else:
        youtube_form = YoutubeForm()
    request.session.save()
    return render(request, 'index.html', {'youtube_form': youtube_form, 'key':request.session.session_key})


# page1
def page1_view(request):

    base_path = os.getcwd()
    base_path = os.path.join(base_path, "web_app", "static", request.session.session_key)
    file_path = os.path.join(base_path, 'data.pkl')
    with open(file_path, 'rb') as fp:
        data = pickle.load(fp)

    # p1_data: {'title': title, 'url': url, 'summary': full_summary, 'text': [...], 'time': [...], 'pgl_img': []}
    p1_data = page1_data(data)
    
      
    return render(request, 'page1.html', p1_data)


# page1
def page2_view(request):

    base_path = os.getcwd()
    base_path = os.path.join(base_path, "web_app", "static", request.session.session_key)
    file_path = os.path.join(base_path, 'data.pkl')
    with open(file_path, 'rb') as fp:
        data = pickle.load(fp)
    
    # p2_data = {'title': ..., 'url': ..., 'summ_text': [...], 'time': [...], 'img': [...]}
    p2_data = page2_data(data)
      


    return render(request, 'page2.html', p2_data)


# page1
def page3_view(request):

    base_path = os.getcwd()
    base_path = os.path.join(base_path, "web_app", "static", request.session.session_key)
    file_path = os.path.join(base_path, 'data.pkl')
    with open(file_path, 'rb') as fp:
        data = pickle.load(fp)

    # p3_data = {'title': ..., 'url': ..., 'summ_text': [...], 'text': [[...],[...],[...],...], 'start_time': [[...],[...],[...],...], 'img': []}
    p3_data = page3_data(data)

      
    return render(request, 'page3.html', p3_data)