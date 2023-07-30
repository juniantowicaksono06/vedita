from media import AudioPlayer
from record import Record
import requests
import globalvar
import constant
import base64
import json

def action_konfirmasi_bahasa_id(data, filename_audio):
    audio = AudioPlayer()
    record = Record()
    record.record_audiov2(filename_audio)
    with open(filename_audio, 'rb') as file:
        file_audio = file.read()
    req = requests.post(f"{globalvar.base_url}/vedita-action", data={"data": {
            "tag": data['tag'],
            "status": globalvar.current_status,
        }, 
        "language": globalvar.current_language
    }, files={'file': ('audio.wav', file_audio)}, verify=False)
    if req.status_code == 200:
        result = req.json()
        data = result['data']
        b64_wav = data['b64_wav']
        b64_wav = base64.b64decode(b64_wav.encode('utf-8'))
        with open(globalvar.output_filename, 'wb') as wav_file:
            wav_file.write(b64_wav)
        
        audio.load_audio(globalvar.output_filename)
        audio.play_audio()
        audio.exit()
        globalvar.change_language(constant.LANGUAGE_ID)
        return True
    return False


def action_konfirmasi_bahasa_eng(data, filename_audio):
    audio = AudioPlayer()
    record = Record()
    record.record_audiov2(filename_audio)
    with open(filename_audio, 'rb') as file:
        file_audio = file.read()
    
    payload = {
        "data": json.dumps({
            "tag": data['tag'],
            "status": globalvar.current_status
        }),
        "language": globalvar.current_language
    }

    req = requests.post(f"{globalvar.base_url}/vedita-action", data=payload, files={'file': ('audio.wav', file_audio)}, verify=False)
    print(req.content)
    if req.status_code == 200:
        result = req.json()
        data = result['data']
        b64_wav = data['b64_wav']
        b64_wav = base64.b64decode(b64_wav.encode('utf-8'))
        with open(globalvar.output_filename, 'wb') as wav_file:
            wav_file.write(b64_wav)
        
        audio.load_audio(globalvar.output_filename)
        audio.play_audio()
        audio.exit()
        globalvar.change_language(constant.LANGUAGE_EN)
        return True
    return False

def action_ubah_bahasa_eng(data, filename_audio):
    globalvar.change_language(constant.LANGUAGE_EN)

def action_ubah_bahasa_indo(data, filename_audio):
    globalvar.change_language(constant.LANGUAGE_ID)