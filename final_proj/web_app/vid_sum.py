import os
from datetime import datetime

def vid_sum(sum_code):
    base_path = os.getcwd()

    for i in range(len(sum_code['output'])):
        temp='ffmpeg -y -ss ' + str(datetime.strptime(sum_code['output'][i]['timestamps'][0], '%H:%M:%S.%f'))[11:] + ' -i ' + base_path + '\web_app\Youtube\Video\youtube.mp4 -to ' + str(datetime.strptime(sum_code['output'][i]['timestamps'][1], '%H:%M:%S.%f')-datetime.strptime(sum_code['output'][i]['timestamps'][0], '%H:%M:%S.%f')) + ' -vcodec copy -acodec copy ' + base_path + '\web_app\Youtube\Video\cut_youtube_' + str(i) + '.mp4'
        os.system(temp)
