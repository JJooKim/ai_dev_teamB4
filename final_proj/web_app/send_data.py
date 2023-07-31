
# data = {'title': title, 'url': url, 'whisper': script, 'scene_summary': scene_summary, 'voice_summary': voice_summary}
# whisper = [{'start':start, 'end': end, 'text': txt, ...}, {'start':start, 'end': end, 'text': txt, ...}, ... ]
# scene_summary = [{'tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text': sum_text}, {tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text'}]
# voice summary = [{'tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text': sum_text}, {tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text'}]
# 'cut_youtube'
'scene_gif'
'scene_youtube'
'sum_gif'
'voice_gif'
'voice_youtube'

def make_fullSum(voice_sum):
    full_summary = ''

    for voice_data in voice_sum:
        full_summary = full_summary + " " + voice_data['summ_text']

    return full_summary


def page1_data(data):
    voice_summary = data['voice_summary']
    full_summary = make_fullSum(voice_summary)

    new_data = {'title': data['title'], 'url': data['url'], 'summary': full_summary, 'text': [], 'time': [], 
                'cut_youtube': data['cut_youtube'], 'scene_gif': data['scene_gif'], 'scene_youtube': data['scene_youtube'],
                  'sum_gif': data['sum_gif'], 'voice_image': data['voice_image'], 'voice_youtube': data['voice_youtube'],
                  'key': data['key']}

    for voice_data in voice_summary:
        new_data['text'].append(voice_data['summ_text'])

        start_t = sec2strtime(voice_data['start'])
        end_t = sec2strtime(voice_data['end'])
        time = start_t + '-' + end_t

        new_data['time'].append(time)

    return new_data


# scene 기준
def page2_data(data):

    new_data = {'title': data['title'], 'url': data['url'], 'summ_text': [], 'time': [], 
                'cut_youtube': data['cut_youtube'], 'scene_gif': data['scene_gif'], 'scene_youtube': data['scene_youtube'],
                  'sum_gif': data['sum_gif'], 'voice_image': data['voice_image'], 'voice_youtube': data['voice_youtube'],
                  'key': data['key']}
    scene_sum = data['scene_summary']

    for scene_data in scene_sum:
        new_data['summ_text'].append(scene_data['summ_text'])
        
        start_t = sec2strtime(scene_data['start'])
        end_t = sec2strtime(scene_data['end'])
        time = start_t + '-' + end_t

        new_data['time'].append(time)
    
    # zip 으로 묶기
    new_data['zip_scene_gif_summ_text'] = zip(new_data['scene_gif'],new_data['summ_text'])
        
    return new_data



def page3_data(data):
    new_data = {'title': data['title'], 'url': data['url'], 'summ_text': [], 'text': [], 'start_time': [], 
                'cut_youtube': data['cut_youtube'], 'scene_gif': data['scene_gif'], 'scene_youtube': data['scene_youtube'],
                  'sum_gif': data['sum_gif'], 'voice_image': data['voice_image'], 'voice_youtube': data['voice_youtube'], 
                  'key': data['key']}
    # new_data = {'summ_text': ['dfsdfsdf'], 'text': [['dfs', 'df', 'sdf']], 'start_time': [[0, 1, 2]]}
    voice_sum = data['voice_summary']
    whisper_data = data['whisper']

    for voice_data in voice_sum:
        # voice_data = {'tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text': sum_text}
        new_data['summ_text'].append(voice_data['summ_text'])

        start_time = voice_data['start']
        end_time = voice_data['end']

        timeline_script = []
        timeline_start = []

        is_start = False
        is_end = False

        for ind, w_data in enumerate(whisper_data):
            if start_time <= w_data['start'] and is_start == False:
                is_start = True

            if end_time <= w_data['end'] and is_end == False:
                is_end = True
            
            if is_start and not is_end :
                timeline_start.append(sec2strtime(w_data['start']))
                timeline_script.append(w_data['text'])

            if is_start and is_end:
                new_data['text'].append(timeline_script)
                new_data['start_time'].append(timeline_start)
                break

    return new_data




# second to time(string type)
# 00:00:00-00:01:32
def sec2strtime(sec): # 92.321
    # sec: float
    if sec < 0:
        return False

    str_time = ''

    remain_t = int(sec) # remain_t = 92
    s = remain_t%60 # s = 32

    remain_t = remain_t//60 # remain_t = 1
    m = remain_t%60 # m = 1

    remain_t = remain_t//60 # remain_t = 0
    h = remain_t%60 # h = 0

    str_time = str(int(h)).zfill(2) + ':' + str(int(m)).zfill(2) + ':' + str(int(s)).zfill(2)

    return str_time