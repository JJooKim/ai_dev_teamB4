import os
from datetime import datetime
from facenet_pytorch import MTCNN
import torch
import numpy as np
import mmcv, cv2
from PIL import Image, ImageStat

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

def brightness(frame):
   im = frame.convert('L')
   stat = ImageStat.Stat(im)
   return stat.rms[0]

def voice_image(sum_code, base_path):
    mtcnn = MTCNN(keep_all=True)
    for i in range(len(sum_code[0]['Voice Activity Detection based Timeline'])):
        video = mmcv.VideoReader(base_path+'/voice_youtube_'+str(i)+'.mp4')
        frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]
        best_image=[0, 0, frames[0]]

        for frame in frames[::10]:
            boxes, _ = mtcnn.detect(frame)

            try:
                boxes=len(boxes)
            except:
                boxes=0
            
            if boxes >= best_image[0]:
                if brightness(frame) > best_image[1] and brightness(frame) < 100:
                    best_image=[boxes, brightness(frame), frame]
        
        best_image[2].save(base_path+'/voice_image_'+str(i)+'.jpg')
