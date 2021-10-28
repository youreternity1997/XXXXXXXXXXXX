
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:04:09 2020

@author: hutton
"""
import queue
import serial
from select import select
import signal, sys
import threading
from time import sleep,time
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.GPIO as GPIO
from .Interruptable import Interruptable
UART.setup("UART2")
GPIO.setup("P9_15", GPIO.OUT)
GPIO.output("P9_15", GPIO.HIGH)
#HOSTMODE=b'\x07\xc6\x04\x08\x00\x8a\x08\xfe\x95'
#SCAN=b"\x04\xe4\x04\x00\xff\x14"
SCAN=b"\x5e\x5f\x5e\x53\x43\x41\x4e\x2e"
class BarcodeScanner(Interruptable):
    def __init__(self, device_name='/dev/serial/by-id/usb-Linux_3.10.14_with_dwc2-gadget_GadGet_Serial_v2.4_Linux_3.10.14_with_dwc2-gadget-if00', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):

        self.device = None
        ser = serial.Serial()
        ser.port = device_name
        ser.baudrate = baudrate
        ser.parity = parity #set parity check: no parity
        ser.stopbits = stopbits #number of stop bits
        #ser.timeout = None          #block read
        ser.timeout = timeout            #non-block read
        ser.setRTS(False)
        try:
            ser.open()
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
        entry = entry.replace('\r','')
        return entry
    def start_capture(self):
        """TODO"""
        def run(que, X):
            time_started = time()
            barcode = ''
            id_card = ''
            while not self.interrupted():
                select([self.device], [], [], 0.25)
                while self.device.inWaiting() > 0:
                    rr = self.device.read(1)
                    if rr != b'\x04' and rr !=b'\x06': 
                        barcode += rr.decode('unicode_escape')
                        if self.device.inWaiting()==0:
                            id_card = self.saveBarcode(barcode)
                            barcode = ''
                            print(id_card)
                            self.interrupt()
                    else:
                        self.device.flushInput()
                if  time() > time_started + X:
                    self.interrupt()
            que.put(id_card)

        self.clear()
        #self.device.write(HOSTMODE)
        self.device.flushInput()
        self.device.flushOutput()
        self.device.write(SCAN)
        
        #thread = threading.Thread(target=run, name='barcode_scanner', args=(self.que,8,))
        #thread.start()
        run(self.que, 6)

        return self.que.get()

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

