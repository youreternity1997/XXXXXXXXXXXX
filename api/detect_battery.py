import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
from datetime import datetime
import os
ADC.setup()
test = "P9_25"
GPIO.setup(test, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(test, GPIO.FALLING)
logfile = os.open('bat_log.log', os.O_RDWR)
class Detect_Battery:
    def __init__(self, adc_pin = "P9_37"):
        self.adc_pin = adc_pin
    def detect(self):
        connect = GPIO.input(test)
        now = datetime.now()
        #GPIO.wait_for_edge(test, GPIO.BOTH)
        potVal=ADC.read(self.adc_pin)
        potVolt=potVal*1.8
        os.write(logfile, bytes('%s,%f\n' % (now, potVolt), 'UTF-8'))
        return connect,potVolt
