
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks



def pgl_sum(audio_path):
    #yt = YouTube(url)
 
    summarization_pipeline = pipeline(Tasks.video_summarization, model='damo/cv_googlenet_pgl-video-summarization')

    video = summarization_pipeline(audio_path)
    return video