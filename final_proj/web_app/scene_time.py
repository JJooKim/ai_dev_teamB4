import scenedetect 
import time
from datetime import datetime
from scenedetect import VideoManager, SceneManager, StatsManager
from scenedetect.detectors import ContentDetector

def get_scene_time(v_path):
    video_path = v_path
    #stats_path = './result/csv/SceneDetect.csv'

    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)

    # threshold : 0~100 사이의 값으로, 0으로 갈수록 민감하게
    scene_manager.add_detector(ContentDetector(threshold=30))

    # 처리속도 향상을 위해 이미지 크기를 낮춤
    video_manager.set_downscale_factor()

    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    scene_list = scene_manager.get_scene_list()
    #print(f'{len(scene_list)} scenes detected!')

    t_list = []
    for i, scene in enumerate(scene_list):
        time_set = datetime.strptime('00:00:00.000','%H:%M:%S.%f')
        start, end = datetime.strptime(str(scene[0])[:12],'%H:%M:%S.%f') - time_set, datetime.strptime(str(scene[1])[:12],'%H:%M:%S.%f') - time_set
        start_timestamp = start.total_seconds()
        end_timestamp = end.total_seconds()
        dic = {}
        dic['tid'] = i
        dic['start'] = start_timestamp
        dic['end'] = end_timestamp
        t_list.append(dic)
    
    return t_list