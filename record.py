import pyaudio
import wave
import numpy as np
import requests
import os
import platform
from utils import get_base_path
import pygame
import speech_recognition as sr

class Record():
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.record = sr.Recognizer()
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.THRESHOLD = 30
        self.BELOW_THRESHOLD = 0
        self.recorded_audio = []
        self.recording_finished = False
        base_path = get_base_path()
        self.recorded_directory = os.path.join(base_path, 'recorded')
        if not os.path.exists(self.recorded_directory):
            os.makedirs(self.recorded_directory)
        
    

    def calculate_decibel(self, audio_chunk):
        rms = np.sqrt(np.mean(np.square(audio_chunk)))
        decibel = 20 * np.log10(rms)
        # print("Decibel:", decibel)
        return decibel
    

    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        decibel = self.calculate_decibel(audio_data)
        print("Decibel:", decibel)
        if decibel <= self.THRESHOLD:
            self.BELOW_THRESHOLD += 1
            self.recorded_audio.append(in_data)
            if self.BELOW_THRESHOLD >= 100:
                self.recording_finished = True
                return (in_data, pyaudio.paComplete)
            return (in_data, pyaudio.paContinue)
        else:
            self.BELOW_THRESHOLD = 0
            self.recorded_audio.append(in_data)
            return (in_data, pyaudio.paContinue)
    
    def record_audiov2(self, output_filename=None, keep_listening=False, timeout = None):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Say something...")
                    audio = self.record.listen(source, timeout=timeout)
                    print("Finish recording")
                if output_filename is not None:
                    with open(output_filename, 'wb') as file:
                        file.write(audio.get_wav_data())
                    return True
                if not keep_listening:
                    break
            except sr.WaitTimeoutError as e:
                print("Finished recording")
                if not keep_listening:
                    print("Recording stop")
                    break
        return False

    def record_audio(self, output_filename=None):
        self.recorded_audio = []
        self.recording_finished = False
        p = pyaudio.PyAudio()
        audio_stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )
        print("Merekam suara...")
        audio_stream.start_stream()
        while not self.recording_finished:
            pass
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        print("Berhenti merekam suara")

        if output_filename:
            output_filename = os.path.join(self.recorded_directory, output_filename)
            recorded_data = b''.join(self.recorded_audio)        
            wf = wave.open(output_filename, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(recorded_data)
            wf.close()
        
    def play_audio(self, audio_name):
        if platform.system().lower() == 'windows':
            os.system(f"start {audio_name}")
        else:
            os.system(f"ffplay -v 0 -nodisp -autoexit {audio_name}")

    
    def trigger_dita(self):
        output_filename = "output_trigger_dita.wav"
        input_filename = "input_trigger.wav"
        self.record_audio(input_filename)