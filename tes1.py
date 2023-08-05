from motor import Motor
from dotenv import load_dotenv
load_dotenv()
import time

motor = Motor()
motor.control("forward")
time.sleep(3)
motor.control("stop")