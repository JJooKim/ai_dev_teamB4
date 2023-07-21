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


# mainpage
def index_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        youtube_form = YoutubeForm(request.POST)
        if youtube_form.is_valid():
            return redirect('test_page1', url=url)
        else:
            return render(request, 'index.html', {'youtube_form': youtube_form})
    else:
        youtube_form = YoutubeForm()
    return render(request, 'index.html', {'youtube_form': youtube_form})


<<<<<<< HEAD
# test_page
def test_page1_view(request, url):
    audio_path = pre_processing.saveVideo(url)
    time.sleep(3)
    original_audio_path = os.path.join(audio_path, "youtube_original.mp4")
=======


# page1
def page1_view(request, url):
    v_path, a_path = pre_processing.saveVideo(url)
>>>>>>> 76dd01a4010d2f0d3d179113736a188b8bc90952

    print(v_path)
    print(a_path)

<<<<<<< HEAD
    # script = get_script(audio_path)

    # fps 줄이기
    lower_frame(original_audio_path, 5)

    # 비디오 요약
    video = pgl_sum(audio_path)
    vid_sum(video)

    # 원본 비디오 삭제 -> 작업 종료 이후에도 ffmpeg가 좀 더 사용해 삭제에러가 발생해 코드 삭제
=======
    video = pgl_sum(v_path)

    script = get_script(a_path)

    pre_processing.removeVideo(a_path)
    pre_processing.removeVideo(v_path)

  
    return render(request, 'page1.html', {'url': url, "script": script, "video": video})

>>>>>>> 76dd01a4010d2f0d3d179113736a188b8bc90952

    return render(request, 'page1.html', {'url': url, "video": video})