from django.shortcuts import HttpResponse, render, redirect

from .models import Youtube
from .forms import YoutubeForm

from .get_script import get_script

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
    #audio_path = get_audio_path() ->오디오 파일 만들고 파일 경로 반환
    audio_path = 'web_app/audios/video1.wav'
    script = get_script(audio_path) # -> 오디오 파일 바탕으로 script json 데이터 제공

    return render(request, 'page1.html', {'url': url, "script": script})


