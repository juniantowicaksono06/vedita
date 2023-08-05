import os
if int(os.environ.get("IS_RASPBERRY")) == 1:
    import RPi.GPIO as GPIO



class Motor():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.ENA = int(os.environ.get("ENA"))
        self.IN1 = int(os.environ.get("IN1"))
        self.IN2 = int(os.environ.get("IN2"))
        self.IN3 = int(os.environ.get("IN3"))
        self.IN4 = int(os.environ.get("IN4"))
        self.ENB = int(os.environ.get("ENB"))
    
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

        self.pwm1 = GPIO.PWM(self.ENA, 100)  # Frequency = 100Hz
        self.pwm2 = GPIO.PWM(self.ENB, 100)  # Frequency = 100Hz

        self.pwm1.start(0)
        self.pwm2.start(0)
        self.speed = 100
        self.pwm1.ChangeDutyCycle(self.speed)
        self.pwm2.ChangeDutyCycle(self.speed)
        self.control()
    
    def control(self, direction = None):
         # Set motor direction
        if direction == 'backward':
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
        elif direction == 'forward':
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
        elif direction == 'stop':
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)
        elif direction == 'right':
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
        elif direction == 'left':
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
        elif direction is None or direction == "stop":
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)