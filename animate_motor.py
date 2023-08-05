from motor import Motor
import time
import os
# Class berikut berfungsi untuk menggerakan motor
class Animate():
    def __init__(self):
        self.is_raspberry = os.environ.get('IS_RASPBERRY')
        self.is_raspberry = int(self.is_raspberry)
        self.animate = False
        if self.is_raspberry:
            self.motor = Motor()
            self.motor.control()
        else:
            self.motor = None
    
    def start(self):
        self.animate = True
    
    def run(self):
        if self.is_raspberry:
            while self.animate:
                if not self.animate:
                    break 
                self.motor.control("right")
                if not self.animate:
                    break 
                time.sleep(1)
                self.motor.control("left")
                if not self.animate:
                    break 
                time.sleep(1)
                if not self.animate:
                    break 
            self.motor.control()
    
    def stop(self):
        self.animate = False