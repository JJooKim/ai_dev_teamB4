import torch
from pyannote.audio import Pipeline
from pydub import AudioSegment

access_token = "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"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def milliSec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
    return s

def compareSec(time1, time2, millisec):
    if (milliSec(time2) - milliSec(time1)) >= millisec:
        return True
    else:
        return False
    
def milli2strtime(milli_sec):
    if milli_sec < 0:
        return False

    str_time = ''

    remain_t = milli_sec
    ms = remain_t%1000

    remain_t = remain_t//1000
    s = remain_t%60

    remain_t = remain_t//60
    m = remain_t%60

    remain_t = remain_t//60
    h = remain_t%60

    str_time = str(int(h)).zfill(2) + ':' + str(int(m)).zfill(2) + ':' + str(int(s)).zfill(2) + '.' + str(int(ms))

    return str_time

def time2sec(timeStr):
    spl = timeStr.split(":")
    s = (int)(int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )
    return s


def get_segment_based_vad(output, sec):
  # sec는 초단위 ex. 5(5초), 10(10초)
    timelines = []
    tid = 0

    for i, speech in enumerate(output.get_timeline()):
        str_speech = str(speech)
        start_time = str_speech[2:15]
        end_time = str_speech[20:-1]

        if i == 0:
            timelines.append({'tid': tid, 'start': time2sec(start_time), 'end': time2sec(end_time)})
            tid += 1
            continue

        prev_start_time = timelines[-1]['start']
        prev_end_time = timelines[-1]['end']

        milli_sec = sec*1000

        if compareSec(prev_end_time, start_time, milli_sec):
            timelines.append({'tid': tid, 'start': time2sec(start_time), 'end': time2sec(end_time)})
            tid += 1
        else:
            timelines[-1]['end'] = end_time

    return timelines

def get_segment_based_sdz(output, speaker_sec, empty_sec):
  # sec는 초단위 ex. 5(5초), 10(10초)
  timelines = []
  tid = 0
  milli_sec = empty_sec*1000

  # 같은 speaker 끼리 모아서 timeline 만들기
  for i, speech in enumerate(output.get_timeline()):
    str_speech = str(speech)
    start_time = str_speech[2:15]
    end_time = str_speech[20:-1]
    speaker = output.get_labels(speech)
    speaker = list(speaker)[0]

    if i == 0:
      timelines.append({'tid': tid, 'start': time2sec(start_time), 'end': time2sec(end_time), 'speaker': speaker})
      tid += 1
      continue

    prev_start_time = timelines[-1]['start']
    prev_end_time = timelines[-1]['end']
    prev_speaker = timelines[-1]['speaker']

    # 이전 발화시간과 empty_sec 이상의 차이가 있다면
    # (이전 발화 후 현 발화 간의 시간이 empty_sec보다 길다면) 
    # 같은 speaker라도 발화 split
    if compareSec(prev_end_time, start_time, milli_sec):
      timelines.append({'tid': tid, 'start': time2sec(start_time), 'end': time2sec(end_time), 'speaker': speaker})
      continue


    if prev_speaker == speaker:
      timelines[-1]['end'] = end_time
    else:
      timelines.append({'tid': tid, 'start': time2sec(start_time), 'end': time2sec(end_time), 'speaker': speaker})
      tid += 1

  # 한 사람의 발화가 sec초 이상인 timeline 추출
  long_timelines = []
  milli_sec = speaker_sec*1000
  tid = 0
    
  for i, timeline in enumerate(timelines):
    if compareSec(timeline['start'], timeline['end'], milli_sec):
      timeline['tid'] = tid
      tid += 1
      long_timelines.append(timeline)

  return timelines, long_timelines

def get_segment_based_osd(output, sec, audio_end_time):
    # overlapped timeline 앞 뒤 sec 길이의 구간
    # ex.
    # [input]  overlapped timeline: 00:01:32   sec: 60(1분)
    # [output] 00:00:32 - 00:02:32의 timeline
    # sec는 초단위 ex. 5(5초), 10(10초)
    timelines = []
    tid = 0

    for i, speech in enumerate(output.get_overlap()):
        str_speech = str(speech)
        overlap_start_time = str_speech[2:15]
        overlap_end_time = str_speech[20:-1]

        milli_sec = sec*1000

        start_time = milliSec(overlap_start_time) - milli_sec
        start_time = milli2strtime(start_time)

        end_time = milliSec(overlap_end_time) + milli_sec
        end_time = milli2strtime(end_time)

        # start_time이 영상 시작 시간보다 작은 경우
        if start_time == False:
            start_time = '00:00:00'

        # end_time이 영상 종료 시간보다 큰 경우
        if milliSec(end_time) > milliSec(audio_end_time):
            end_time = audio_end_time

        timelines.append({'tid': tid, 'start': time2sec(start_time), 'end': time2sec(end_time)})
        tid += 1

    return timelines

def get_voice_time(audio_path, method='vad'):
    if method == 'vad':
        VAD = Pipeline.from_pretrained("pyannote/voice-activity-detection", use_auth_token= (access_token))
        VAD.to(device)

        vad_output = VAD(audio_path)
        tl = get_segment_based_vad(vad_output, 5)

        return[{'Voice Activity Detection based Timeline': tl}]


    else:
        SDZ = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token= (access_token))
        SDZ.to(device)

        sdz_output = SDZ(audio_path)

        if method == 'sdz':
            tl, long_tl = get_segment_based_sdz(sdz_output, 30, 5)

            return[{'Speaker Diarization based Timeline': tl, 'Long Segment': long_tl}]

        elif method == 'osd':
            # audio의 end time 구하기
            audio = AudioSegment.from_file(audio_path, format='wav')
            millisec_time = audio.duration_seconds * 1000
            audio_end = milli2strtime(millisec_time)

            tl = get_segment_based_osd(sdz_output, 60, audio_end)
            
            return[{'timeline': tl}]