
def get_scene_script(script, timeline):
    ret = []
    id = 0
    for t in timeline:

      start = t['start']
      end = t['end']
      s = ''      


      max_time_s = int(script[-1]['start'])
      max_time_e = int(script[-1]['end'])


      if not start :
        start_k = 0
      else :
        k = 0
        while start > int(script[k]['start']) and int(script[k]['start']) != max_time_s :
          k += 1
        start_k = k

      if not end :
        end_k = len(script) -1
      else :
        k = 0
        while end > int(script[k]['end']) and int(script[k]['end']) != max_time_e :
          k += 1
        end_k = k


      for i in range(start_k, end_k + 1) :
        s += script[i]['text']
 
      ret.append({'tid': id, 'start':start, 'end': end, 'text': s})
      id += 1


    return ret

from kiwipiepy import Kiwi

import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-summarization')
model = model.to(device)

kiwi = Kiwi()


import copy



def get_scene_summary(scene_script):
    """
    text : 요약을 원하는 text
    k : 하나로 뭉칠 segment 갯수
    output : (요약문 -> list)
    """
      
    res = copy.deepcopy(scene_script)

    
    
    for idx, seg in enumerate(scene_script):
      text = seg['text']
      summ = ""
      for i, sent in enumerate(kiwi.split_into_sents(text)):
      # print(sent)

        sent = sent.text
        summ += sent
      raw_input_ids = tokenizer.encode(summ)
      input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

      inputs = torch.tensor([input_ids])
      inputs = inputs.to(device)

      # summary_ids = model.generate(inputs,  max_new_tokens=100)

      summary_ids = model.generate(inputs,  max_new_tokens=100)
      output = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)



      res[idx]['summ_text'] = output
    

    return res