import requests
import platform
import time
from media import AudioPlayer
from record import Record
from dotenv import load_dotenv
from utils import get_base_path
import os
load_dotenv()
import status_constant as STATUS
import base64

base_url = os.environ.get('API_BASE_URL')
output_filename = os.path.join(get_base_path(), 'output.mp3')
current_status = STATUS.IDLE_STATUS

def listen_trigger_vedita():
    global current_status
    audio = AudioPlayer()
    filename_audio = os.path.join(get_base_path(), "input.wav")
    record = Record()
    record.record_audiov2(filename_audio, keep_listening=True)
    with open(filename_audio, 'rb') as file:
        file_audio = file.read()
    req = requests.post(f"{base_url}/vedita_voice_commands", files={'file': ('audio.wav', file_audio)}, verify=False)
    # print(req.content)
    if req.status_code == 200:
        response = req.content
        with open(output_filename, 'wb') as file:
            file.write(response)
        audio.load_audio(output_filename)
        audio.play_audio()
        audio.exit()
        current_status = STATUS.TRIGGER_STATUS
        return True
    return False

def listen_command():
    global current_status
    filename_audio = os.path.join(get_base_path(), 'input.wav')
    audio = AudioPlayer()
    record = Record()
    record.record_audiov2(filename_audio)
    with open(filename_audio, 'rb') as file:
        file_audio = file.read()
    req = requests.post(f"{base_url}/vedita_voice_commands", files={'file': ('audio.wav', file_audio)}, verify=False, data={'triggered': '1'})
    if req.status_code == 200:
        response = req.json()
        data = response['data']
        b64_wav = data['b64_wav']
        b64_wav = base64.b64decode(b64_wav.encode('utf-8'))
        with open(output_filename, 'wb') as wav_file:
            wav_file.write(b64_wav)
        audio.load_audio(output_filename)
        audio.play_audio()
        audio.exit()
        return True
    return False

while True:
    try:
        if current_status == STATUS.IDLE_STATUS:
            triggered = listen_trigger_vedita()
        elif current_status != STATUS.IDLE_STATUS:
            listen_command()
    except KeyboardInterrupt:
        break

print("Finish")