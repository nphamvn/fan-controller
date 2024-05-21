# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
from flask import Flask
import threading

app = Flask(__name__)
lock = threading.Lock()

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"
    
PIN = 11
OFFSET_DUTY = 0.5
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY
SERVO_DELAY_SEC = 0.001

@app.route('/switch', methods=['POST'])
def switch():
    with lock:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.output(PIN, GPIO.LOW)
        p = GPIO.PWM(PIN, 50)

        p.start(0)

        def servoWrite(angle):
            if(angle < 0):
                angle = 0
            elif(angle > 180):
                angle = 180
            dc = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * angle / 180.0
            p.ChangeDutyCycle(dc)

        for angle in range(90, -1, -1):
            servoWrite(angle)
            sleep(SERVO_DELAY_SEC)
        sleep(0.5)

        for angle in range(0, 91, 1):
            servoWrite(angle)
            sleep(SERVO_DELAY_SEC)
        sleep(0.5)

        p.stop()
        GPIO.cleanup()
        
        return "done"

if __name__ == '__main__':
    app.run(host='0.0.0.0')