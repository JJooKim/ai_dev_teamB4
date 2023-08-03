import scenedetect 
import time
from datetime import datetime
from scenedetect import VideoManager, SceneManager, StatsManager
from scenedetect.detectors import ContentDetector

def get_scene_time(v_path, video_length):
    video_path = v_path
    thresh_hold=70
    min_hold, max_hold= 30, 95
    for _ in range(5):
        video_manager = VideoManager([video_path])
        stats_manager = StatsManager()
        scene_manager = SceneManager(stats_manager)

        # threshold : 0~100 사이의 값으로, 0으로 갈수록 민감하게
        scene_manager.add_detector(ContentDetector(thresh_hold))

        # 처리속도 향상을 위해 이미지 크기를 낮춤
        video_manager.set_downscale_factor()
        #화면 전환 부분 탐색 시작
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)

        scene_list = scene_manager.get_scene_list()
        #화면 전환 된 파트를 리스트에 저장(timestamp 단위)
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
        #JSON(tid, start, end)가 담긴 리스트 반환
        if len(t_list)==video_length/10+1:
            return t_list
        elif len(t_list) > video_length/10+1:
            min_hold=thresh_hold
            thresh_hold=(thresh_hold+max_hold)/2
        else:
            max_hold=thresh_hold
            thresh_hold=(thresh_hold+min_hold)/2
    return t_list
