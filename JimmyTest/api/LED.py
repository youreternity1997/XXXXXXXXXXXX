#import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time, threading

class LED:
    def __init__(self, gpio_pin = "P9_16"):
        self.gpio = gpio_pin    
        GPIO.setup(self.gpio, GPIO.OUT)
    def LED_blink(self):
        GPIO.output(self.gpio, GPIO.HIGH)
    def LED_close(self):
        GPIO.output(self.gpio, GPIO.LOW)
    '''
    def __init__(self, pwm_pin = "P9_16"):
        self.pwm = pwm_pin    

    def LED_blink(self):
        PWM.start(self.pwm, 100, 10000)
        #PWM.set_duty_cycle(self.pwm, 100)

    def LED_close(self):
        PWM.stop(self.pwm)
        PWM.cleanup()
    '''
test = LED()
test.LED_blink()
'''
test = LED()
t = threading.Thread(target = test.LED_blink)
t.start()
time.sleep(3)
print("after 3 sec")
t.do_run = False
t.join()
test.LED_close()
'''
