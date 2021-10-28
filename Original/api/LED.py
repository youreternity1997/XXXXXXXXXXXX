#import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO #GPIO（General Purpose I/O Ports）意思是通用輸入/輸出埠，也就是一些針腳可以通過它們輸出高電位或者低電位，可以供使用者由程式控制自由使用，與裝置進行通訊，達到控制裝置的目的。

import time, threading

class LED:
    def __init__(self, gpio_pin = "P9_16"):
        self.gpio = gpio_pin    
        GPIO.setup(self.gpio, GPIO.OUT) #設定掃描機輸出
    def LED_blink(self):
        GPIO.output(self.gpio, GPIO.HIGH) #掃描機高電位打開
    def LED_close(self):
        GPIO.output(self.gpio, GPIO.LOW) #掃描機低電位關閉
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

