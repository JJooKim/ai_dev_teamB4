import whisper

def get_script(audio_path):
    model = whisper.load_model('large')
    result = model.transcribe(audio_path)
    script = result['segments']
    
    return script