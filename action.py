from media import AudioPlayer
from record import Record
import requests
import globalvar
import constant
import base64
import json
from PIL import Image
from utils import convert_b64_to_file, make_request, show_image_full_screen
import threading

def action_ditaaja_reset_password(data, filename_audio):
    return default_confirm(data, filename_audio)

def action_ditaaja_unlock_domain(data, filename_audio):
    return default_confirm(data, filename_audio)

def action_konfirmasi_bahasa_id(data, filename_audio):
    return default_confirm(data, filename_audio)

def action_konfirmasi_bahasa_eng(data, filename_audio):
    return default_confirm(data, filename_audio)

def action_ubah_bahasa_eng(data, filename_audio):
    globalvar.change_language(constant.LANGUAGE_EN)

def action_ubah_bahasa_indo(data, filename_audio):
    globalvar.change_language(constant.LANGUAGE_ID)

def action_cuaca_konfirmasi_kota(data, filename_audio):
    return default_confirm(data, filename_audio)

def action_suhu_konfirmasi_kota(data, filename_audio):
    return default_confirm(data, filename_audio)

# def action_konfirmasi_faq_reset_password_desmita(data, filename_audio):
#     return action_konfirmasi_faq_desmita(data, filename_audio)

# def action_konfirmasi_faq_reset_password_desmita(data, filename_audio):
#     return action_konfirmasi_faq_desmita(data, filename_audio)

def action_konfirmasi_faq_desmita(data, filename_audio):
    b64_faq_img = False
    if "b64_faq_img" in data:
        if data['b64_faq_img'] is not None:
            b64_faq_img = data['b64_faq_img']
    if not b64_faq_img:
        return default_confirm(data, filename_audio)
    else:
        print("B64 FAQ Img:",b64_faq_img)
        convert_b64_to_file(globalvar.output_faq_filename, b64_faq_img)
        threading.Thread(target=show_image_full_screen, args=(globalvar.output_faq_filename, )).start()
        
        audio = AudioPlayer()
        record = Record()
        record.record_audiov2(filename_audio)
        audio.load_audio(globalvar.output_filename)
        audio.play_audio()
        audio.exit()
        return True
    return False
  
def default_confirm(data, filename_audio):
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
    req = make_request(f"{globalvar.base_url}/vedita-action", method="POST", payload=payload, files={'file': ('audio.wav', file_audio)}, verify=False)
    if req.status_code == 200:
        result = req.json()
        data = result['data']
        b64_wav = data['b64_wav']
        b64_wav = base64.b64decode(b64_wav.encode('utf-8'))
        with open(globalvar.output_filename, 'wb') as wav_file:
            wav_file.write(b64_wav)
        print(data.keys())
        if "b64_faq_img" in data:
            convert_b64_to_file(globalvar.output_faq_filename, data['b64_faq_img'])
            threading.Thread(target=show_image_full_screen, args=(globalvar.output_faq_filename, )).start()

        audio.load_audio(globalvar.output_filename)
        audio.play_audio()
        audio.exit()
        return True
    return False