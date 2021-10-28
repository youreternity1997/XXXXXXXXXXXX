import Adafruit_BBIO.GPIO as GPIO
import os
import time, threading

class ScreenLock:
    def __init__(self, gpio_pin = 'P9_17'):
        self.gpio = gpio_pin
        self.status = 0
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        # for button LED
        GPIO.setup("P9_12", GPIO.OUT)
        GPIO.output("P9_12", GPIO.HIGH)
        #GPIO.add_event_detect(gpio_pin, GPIO.BOTH, callback=lambda: self.test)
        #GPIO.wait_for_edge(gpio_pin, GPIO.RISING)
        t = threading.Thread(target = self._click)
        t.start()

    def test(self):
        while True:
            print(123)

    def _click(self):
        old_switch_state = 1
        while True:
            new_switch_state = GPIO.input(self.gpio)
            if new_switch_state == 0 and old_switch_state == 1 :
                if self.status == 0:
                    os.system('gnome-screensaver-command -l') 
                    #os.system('echo "standby" > /sys/power/state')
                    #print("123") 
                    self.status = 1
                elif self.status == 1:
                    #print("456") 
                    os.system('gnome-screensaver-command -d')
                    self.status = 0
                time.sleep(0.1)
            old_switch_state = new_switch_state
#ScreenLock()        
