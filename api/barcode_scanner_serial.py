

# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:04:09 2020

@author: hutton
"""
import queue # Queue 模塊 是提供佇列操作的模塊。佇列 (First In First Out) 是線程間最常用的交換數據的形式。
import serial # pyserial模組封裝了對串列埠的訪問。
from select import select
import signal, sys
import threading
from time import sleep,time
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.GPIO as GPIO
from .Interruptable import Interruptable
UART.setup("UART2") # 通用非同步收發器(Universal Asynchronous Receiver/Teainsmitter)，稱作UART，是以串列傳輸的方式建立兩個裝置之間的連線。
GPIO.setup("P9_15", GPIO.OUT) # 設定掃描機輸出
GPIO.output("P9_15", GPIO.HIGH) # 掃描機高電位打開
#HOSTMODE=b'\x07\xc6\x04\x08\x00\x8a\x08\xfe\x95'
#SCAN=b"\x04\xe4\x04\x00\xff\x14"
SCAN=b"\x5e\x5f\x5e\x53\x43\x41\x4e\x2e"

class BarcodeScanner(Interruptable):
    def __init__(self, device_name='/dev/serial/by-id/usb-Linux_3.10.14_with_dwc2-gadget_GadGet_Serial_v2.4_Linux_3.10.14_with_dwc2-gadget-if00', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):

        self.device = None
        ser = serial.Serial() #pyserial模組封裝了對串列埠的訪問。
        ser.port = device_name #裝置的埠 ex:COM5、COM3
        ser.baudrate = baudrate #波特率 ex:9600 (bit per second)
        ser.parity = parity #用來檢測傳送的位元組是否有傳輸錯誤: PARITY_NONE(無校驗). Other:PARITY_EVEN(偶校驗), PARITY_ODD(奇校驗), PARITY_MARK, PARITY_SPACE
        ser.stopbits = stopbits #number of stop bits(停止位)
        #ser.timeout = None #block read
        ser.timeout = timeout #non-block read  #讀超時設定
        ser.setRTS(False) #you can't control the RTS
        try:
            ser.open() #打开串口
            self.device = ser 
            #self.device = open(device_name, 'wb')
        except serial.SerialException:
            print("error open serial port: " + device_name)

        self._listeners = []
        self.que = queue.Queue()
        Interruptable.__init__(self)
        
    def saveBarcode(self, bc):
        entry = bc
        with open('barcodes.txt', 'w') as bc_file:
                bc_file.write(entry)
        entry = entry.replace('\r','') #\r表示將游標的位置回退到本行的開頭位置
        return entry
    
    def start_capture(self):
        """TODO"""
        def run(que, X):
            time_started = time()
            barcode = ''
            id_card = ''
            while not self.interrupted(): #Thread.interrupt()
                select([self.device], [], [], 0.25) #####################################################################
                while self.device.inWaiting() > 0: #inWaiting()：返回接收快取中的位元組數
                    rr = self.device.read(1) #從埠讀1個位元組
                    if rr != b'\x04' and rr !=b'\x06': ##################################################################
                        barcode += rr.decode('unicode_escape') # 解碼rr並加起來
                        if self.device.inWaiting()==0: #如果返回接收快取中的位元組數==0
                            id_card = self.saveBarcode(barcode) 
                            barcode = ''
                            print(id_card)
                            self.interrupt() #中斷
                    else:
                        self.device.flushInput() #丟棄接收緩存中的所有數據
                if  time() > time_started + X:
                    self.interrupt() # 超過6秒即中斷
            que.put(id_card) #將id_card加進que

        self.clear() #清空
        #self.device.write(HOSTMODE)
        self.device.flushInput() #丟棄接收緩存中的所有數據
        self.device.flushOutput() #終止當前寫操作，並丟棄發送緩存中的數據。
        self.device.write(SCAN) #向埠寫Scan data
        
        #thread = threading.Thread(target=run, name='barcode_scanner', args=(self.que,8,))
        #thread.start()
        run(self.que, 6)
        return self.que.get() #返回que的值

    def register_listener(self, callback):
        self._listeners.append(callback)

    def clear(self):
        self.reset()
        while not self.que.empty():
            self.que.get()
    def close(self):
        if self.device is None:
            print("serial error")
            return
        self.device.close()
