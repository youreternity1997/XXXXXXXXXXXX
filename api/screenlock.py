# GPIO（General Purpose I/O Ports）意思是通用輸入/輸出埠，也就是一些針腳可以通過它們輸出高電位或者低電位，可以供使用者由程式控制自由使用，與裝置進行通訊，達到控制裝置的目的。
import Adafruit_BBIO.GPIO as GPIO
import os
import time, threading

class ScreenLock:
    def __init__(self, gpio_pin = 'P9_17'):
        self.gpio = gpio_pin
        self.status = 0
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 設定這個針腳是作為輸入。
        # for button LED
        GPIO.setup("P9_12", GPIO.OUT) # 設定這個針腳是作為輸出。
        GPIO.output("P9_12", GPIO.HIGH) # 設定針對輸出的狀態是高電位。
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
            new_switch_state = GPIO.input(self.gpio) # 取得該針腳的當下狀態為何，這樣就可以進一步有邏輯去判斷了。
            if new_switch_state == 0 and old_switch_state == 1 : # new_switch_state == 0 代表不是處於鎖定螢幕狀態。
                if self.status == 0:
                    os.system('gnome-screensaver-command -l') # 鎖定螢幕
                    #os.system('echo "standby" > /sys/power/state')
                    #print("123") 
                    self.status = 1 # 鎖螢幕狀態
                elif self.status == 1:
                    #print("456") 
                    os.system('gnome-screensaver-command -d') # 結束鎖定螢幕
                    self.status = 0 # 無鎖螢幕狀態
                time.sleep(0.1)
            old_switch_state = new_switch_state
#ScreenLock()            
