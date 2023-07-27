import copy

def get_scene_script(script, timeline):
    ret = []
    curr_script_id = 0
    for idx, t in enumerate(timeline):

      start = t['start']
      end = t['end']
      txt = ""      

      for s in script[curr_script_id:]:
         if end < s['start']:
            break 
         txt += s['text']
         curr_script_id += 1
         if  s['end'] > end:
            break
    
      ret.append({'tid': idx, 'start':start, 'end': end, 'text': txt})
      
    return ret




from kiwipiepy import Kiwi

import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-summarization')
model = model.to(device)

kiwi = Kiwi()


def make_summary(scene_script):
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


def get_scene_summary(script, timeline):
    return make_summary(get_scene_script(script, timeline))