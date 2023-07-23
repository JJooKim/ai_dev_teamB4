#from PySceneDetect.scenedetect import detect

def get_scene_time(video_path):
    ret = []
    
    # scene_list = detect(video_path, ContentDetector(threshold=30))
    # for i, scene in enumerate(scene_list):
    #     ret.append({"start": scene[0].get_timecode(), "end": scene[1].get_timecode(), "start_frames": scene[0].get_frames(), "end_frames": scene[1].get_frames()})

    return ret