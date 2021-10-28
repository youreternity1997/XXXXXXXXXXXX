import Adafruit_BBIO.ADC as ADC #ADC enables reading analog input values from the analog to digital converter (ADC) 
import Adafruit_BBIO.GPIO as GPIO #GPIO（General Purpose I/O Ports）意思是通用輸入/輸出埠，也就是一些針腳可以通過它們輸出高電位或者低電位，可以供使用者由程式控制自由使用，與裝置進行通訊，達到控制裝置的目的。
from datetime import datetime
import os
ADC.setup()

test = "P9_25" #腳位
GPIO.setup(test, GPIO.IN, pull_up_down = GPIO.PUD_UP) #想要獲取針腳的狀態就先將針腳設定為輸入，GPIO.PUD_UP:開啟內建上拉電阻的選項
############################測試開始(可忽略)
GPIO.add_event_detect(test, GPIO.FALLING) #GPIO.add_event_detect(test, GPIO.FALLING, callback=buttonPressed) 是事件方式，當輸入腳位由高電位變成低電位 (GPIO.FALLING) 時，會直接跳到已登記的程式buttonPressed
############################測試結束

logfile = os.open('bat_log.log', os.O_RDWR)

class Detect_Battery:
    def __init__(self, adc_pin = "P9_37"):
        self.adc_pin = adc_pin
    def detect(self):
        connect = GPIO.input(test) #以取得該針腳的當下狀態為何。
        now = datetime.now()
        #GPIO.wait_for_edge(test, GPIO.BOTH) #GPIO.wait_for_edge() 是等候按鍵時會一直停著，直到狀態成立才能繼續。
        potVal = ADC.read(self.adc_pin)
        potVolt = potVal*1.8
        os.write(logfile, bytes('%s,%f\n' % (now, potVolt), 'UTF-8'))
        return connect, potVolt
