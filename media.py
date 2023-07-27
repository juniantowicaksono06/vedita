import pygame

class AudioPlayer:
    def __init__(self, audio_name = None):
        pygame.init()
        pygame.mixer.init()
        self.audio_file_path = audio_name  # Replace with the path to your audio file

    def load_audio(self, audio_name = None):
        try:
            if audio_name is not None:
                self.audio_file_path = audio_name
            pygame.mixer.music.load(self.audio_file_path)
        except pygame.error as e:
            print("Error loading audio.")
            print("Error:", str(e))

    def play_audio(self):
        try:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
        except pygame.error as e:
            print("Error playing audio.")
            print("Error:", str(e))

    def pause_audio(self):
        try:
            pygame.mixer.music.pause()
        except pygame.error:
            print("Error pausing audio.")

    def unpause_audio(self):
        try:
            pygame.mixer.music.unpause()
        except pygame.error:
            print("Error unpausing audio.")

    def stop_audio(self):
        try:
            pygame.mixer.music.stop()
        except pygame.error as e:
            print("Error stopping audio.")
            print("Error:", str(e))
    
    def exit(self):
        try:
            pygame.mixer.quit()
        except pygame.error:
            print("Error exiting")