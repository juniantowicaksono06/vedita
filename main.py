from dotenv import load_dotenv
load_dotenv()
import requests
import platform
import time
from media import AudioPlayer
from record import Record
from utils import get_base_path
import os
import constant
import base64
import globalvar
from action import *

# Fungsi dibawah untuk trigger Vedita agar bisa mengeksekusi command
def listen_trigger_vedita():
    audio = AudioPlayer()
    filename_audio = os.path.join(get_base_path(), "input.wav")
    record = Record()
    record.record_audiov2(filename_audio, keep_listening=True)
    with open(filename_audio, 'rb') as file:
        file_audio = file.read()
    req = requests.post(f"{globalvar.base_url}/vedita_voice_commands", files={'file': ('audio.wav', file_audio)}, data={'status': globalvar.current_status}, verify=False)
    if req.status_code == 200:
        response = req.content
        with open(globalvar.output_filename, 'wb') as file:
            file.write(response)
        audio.load_audio(globalvar.output_filename)
        audio.play_audio()
        audio.exit()
        globalvar.current_status = constant.TRIGGER_STATUS
        return True
    return False

# Fungsi dibawah untuk mendengarkan sekaligus untuk mengekseksi command
def listen_command():
    filename_audio = os.path.join(get_base_path(), 'input.wav')
    audio = AudioPlayer()
    record = Record()
    record.record_audiov2(filename_audio, timeout=10)
    with open(filename_audio, 'rb') as file:
        file_audio = file.read()
    req = requests.post(f"{globalvar.base_url}/vedita_voice_commands", files={'file': ('audio.wav', file_audio)}, verify=False, data={'status': globalvar.current_status, 'language': globalvar.current_language})
    if req.status_code == 200:
        response = req.json()
        data = response['data']
        b64_wav = data['b64_wav']
        b64_wav = base64.b64decode(b64_wav.encode('utf-8'))
        with open(globalvar.output_filename, 'wb') as wav_file:
            wav_file.write(b64_wav)
        audio.load_audio(globalvar.output_filename)
        audio.play_audio()
        audio.exit()
        tag = data['tag']
        function_name = f"action_{tag}"
        print("Function Name: ", function_name)

        if function_name in globals() and callable(globals()[function_name]):
            func = globals()[function_name]
            response = func(data, filename_audio)
            return response
    return False

while True:
    try:
        if globalvar.current_status == constant.IDLE_STATUS:
            triggered = listen_trigger_vedita()
        elif globalvar.current_status != constant.IDLE_STATUS:
            listen_command()
    except KeyboardInterrupt:
        break

print("Finish")