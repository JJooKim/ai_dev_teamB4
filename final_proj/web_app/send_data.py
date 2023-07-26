
# data = {'title': title, 'url': url, 'whisper': script, 'scene_summary': scene_summary, 'voice_summary': voice_summary}
# whisper = scene_summary = [{'start':start, 'end': end, 'text': txt, ...}, {'start':start, 'end': end, 'text': txt, ...}, ... ]
# scene_summary = [{'tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text': sum_text}, {tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text'}]
# voice summary = [{'tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text': sum_text}, {tid': idx, 'start':start, 'end': end, 'text': txt, 'summ_text'}]


def make_fullSum(voice_sum):
    full_summary = ''

    for voice_data in voice_sum:
        full_summary = full_summary + " " + voice_data['summ_text']

    return full_summary


def page1_data(data):
    voice_summary = data['voice_summary']
    full_summary = make_fullSum(voice_summary)

    new_data = {'summary': full_summary, 'text': [], 'time': [], 'img': []}

    for voice_data in voice_summary:
        new_data['text'].append(voice_data['summ_text'])

        start_t = sec2strtime(voice_data['start'])
        end_t = sec2strtime(voice_data['end'])
        time = start_t + '-' + end_t

        new_data['time'].append(time)

    return new_data



def page2_data(data):
    new_data = {'text': [], 'time': []}
    voice_sum = data['voice_summary']

    for voice_data in voice_sum:
        new_data['text'].append(voice_data['text'])
        new_data['time'].append(voice_data['start'])

    return new_data


# 00:00:00-00:01:32
def page3_data(data):
    new_data = {'text': [], 'time': [], 'img': []}
    scene_sum = data['scene_summary']

    for scene_data in scene_sum:
        new_data['text'].append(scene_data['summ_text'])
        
        start_t = sec2strtime(scene_data['start'])
        end_t = sec2strtime(scene_data['end'])
        time = start_t + '-' + end_t

        new_data['time'].append(time)


    return new_data

# second to time(string type)
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