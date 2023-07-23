# from scenedetect import VideoManager, SceneManager, StatsManager
# from scenedetect.detectors import ContentDetector
# from scenedetect.scene_manager import save_images, write_scene_list_html


import PySceneDetect.scenedetect as sd




video_path = 'final_proj/web_app/Youtube/dvideo/sum_gif0.gif'
#stats_path = './result/csv/SceneDetect.csv'

model = sd.detect(video_path)

video_manager = VideoManager([video_path])
stats_manager = StatsManager()
scene_manager = SceneManager(stats_manager)
# threshold : 0~100 사이의 값으로, 0으로 갈수록 민감하게
scene_manager.add_detector(ContentDetector(threshold=30))
# 처리속도 향상을 위해 이미지 크기를 낮춤
video_manager.set_downscale_factor()
video_manager.start()
scene_manager.detect_scenes(frame_source=video_manager)
# # 결과
# with open(stats_path, 'w') as f:
#     stats_manager.save_to_csv(f, video_manager.get_base_timecode())
scene_list = scene_manager.get_scene_list()
print(f'{len(scene_list)} scenes detected!')
# save_images(
#     scene_list,
#     video_manager,
#     num_images=1,
#     image_name_template='$SCENE_NUMBER',
#     output_dir='./result/scenes'
# )
for scene in scene_list:
    start, end = scene
    print(f'{start.get_seconds()} ~ {end.get_seconds()}')