import os
from django.shortcuts import HttpResponse, render, redirect

from .models import Youtube
from .forms import YoutubeForm

from .get_script import get_script
from .get_sum_v import pgl_sum

from .Youtube import pre_processing

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
    audio_path = pre_processing.saveVideo(url)

    audio_path = os.path.join(audio_path, "youtube.mp4")


    video = pgl_sum(audio_path)

    script = get_script(audio_path)

    pre_processing.removeVideo(audio_path)
  
    return render(request, 'page1.html', {'url': url, "script": script, "video": video})


