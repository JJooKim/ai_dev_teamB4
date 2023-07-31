import os
from datetime import datetime

def vid_sum(sum_code, base_path):
    for i in range(len(sum_code['output'])):
        temp='ffmpeg -y -ss ' + str(datetime.strptime(sum_code['output'][i]['timestamps'][0], '%H:%M:%S.%f'))[11:] + ' -i ' + base_path + '/youtube_original.mp4 -to ' + str(datetime.strptime(sum_code['output'][i]['timestamps'][1], '%H:%M:%S.%f')-datetime.strptime(sum_code['output'][i]['timestamps'][0], '%H:%M:%S.%f')) + ' -vcodec copy -acodec copy ' + base_path + '/cut_youtube_' + str(i) + '.mp4'
        os.system(temp)
    for i in range(len(sum_code['output'])):
        temp = 'ffmpeg -y -i ' + base_path + '/cut_youtube_' + str(i) + '.mp4 -r 15 ' + base_path + '/sum_gif' + str(i) + '.gif'
        os.system(temp)
    return True

def vid_sum_from_scene(sum_code, base_path):
    for i in range(len(sum_code)):
        temp='ffmpeg -y -ss ' + str(sum_code[i]['start']) + ' -i ' + base_path + '/youtube_original.mp4 -to ' + str(sum_code[i]['end'] - sum_code[i]['start']) + ' -vcodec copy -acodec copy ' + base_path + '/scene_youtube_' + str(i) + '.mp4'
        os.system(temp)
    for i in range(len(sum_code)):
        temp = 'ffmpeg -y -i ' + base_path + '/scene_youtube_' + str(i) + '.mp4 -r 15 ' + base_path + '/scene_gif' + str(i) + '.gif'
        os.system(temp)
    return True

def vid_sum_from_voice(sum_code, base_path):
    for i in range(len(sum_code[0]['Voice Activity Detection based Timeline'])):
        temp='ffmpeg -y -ss ' + str(sum_code[0]['Voice Activity Detection based Timeline'][i]['start']) + ' -i ' + base_path + '/youtube_original.mp4 -to ' + str(sum_code[0]['Voice Activity Detection based Timeline'][i]['end'] - sum_code[0]['Voice Activity Detection based Timeline'][i]['start']) + ' -vcodec copy -acodec copy ' + base_path + '/voice_youtube_' + str(i) + '.mp4'
        os.system(temp)
    for i in range(len(sum_code[0]['Voice Activity Detection based Timeline'])):
        temp = 'ffmpeg -y -i ' + base_path + '/voice_youtube_' + str(i) + '.mp4 -r 15 ' + base_path + '/voice_gif' + str(i) + '.gif'
        os.system(temp)
    return True

def voice_image(sum_code, base_path):
    for i in range(len(sum_code[0]['Voice Activity Detection based Timeline'])):
        temp = 'ffmpeg -y -ss ' + str(sum_code[0]['Voice Activity Detection based Timeline'][i]['start']) + ' -i ' + base_path + '/youtube_original.mp4 ' + base_path + '/voice_image_' + str(i) + '.jpg'
        os.system(temp)