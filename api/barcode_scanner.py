# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:04:09 2020

@author: hutton
"""

import queue
from evdev import InputDevice, ecodes, list_devices, categorize
from select import select
import signal, sys
from datetime import datetime
import calendar
import threading
from time import sleep

from .Interruptable import Interruptable

class BarcodeScanner(Interruptable):
    """TODO"""

    def __init__(self, device_name='Bar Code'):
        self.modifiers = {
            # 0: None, 29: u'LCTRL', 42: u'LSHFT', 54: u'RSHFT', 56: u'LALT', 97:u'RCTRL', 100: u'RALT'
            0: 0, 29: 1, 42: 2, 54: 3, 56: 4, 97: 5, 100: 6
        }
        self.layouts  = {
	11:	u'0', 2:	u'1', 3:	u'2', 4:	u'3',
	5:	u'4', 6:	u'5', 7:	u'6', 8:	u'7',
	9:	u'8', 10:	u'9', 16:       u'Q', 17:       u'W',
        18:     u'E', 19:       u'R', 20:       u'T', 21:       u'Y',
        22:     u'U', 23:       u'I', 24:       u'O', 25:       u'P',
        30:     u'A', 31:       u'S', 32:       u'D', 33:       u'F',
        34:     u'G', 35:       u'H', 36:       u'J', 37:       u'K',
        38:     u'L', 44:       u'Z', 45:       u'X', 46:       u'C',
        47:     u'V', 48:       u'B', 49:       u'N', 50:       u'M',
        42:     u''
}

        self.device = None
        devices = map(InputDevice, list_devices())
        for device in devices:
            if device_name in device.name:
                self.device = InputDevice(device.fn)
                print('Lecteur de codes-barres : ' + device.name)
                break

        self._listeners = []
        self.que = queue.Queue()
        Interruptable.__init__(self)
        self.device.grab()
    def saveBarcode(self, bc):
        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())

        entry = bc
        with open('barcodes.txt', 'w') as bc_file:
                bc_file.write(entry)
        return entry
    def start_capture(self):
        """TODO"""

        def run(que):
            barcode = ''
            id_card = ''
            modifier = 0
            keycode = 0
            NOT_RECOGNIZED_KEY = u'X'
            while not self.interrupted():
                select([self.device], [], [], 0.25)
                try:
                    for event in self.device.read():
                            if event.type == ecodes.EV_KEY:
                                data = categorize(event)
                                if data.keystate == 1:
                                    scancode = data.scancode
                                    if scancode == 28: # Enter
                                        id_card = self.saveBarcode(barcode)
                                        barcode = ''
                                        print(id_card)
                                        self.interrupt()
                                    else:
                                        key = self.layouts.get(scancode, NOT_RECOGNIZED_KEY)
                                        barcode = barcode + key
                                        if key == NOT_RECOGNIZED_KEY:
                                            print('unknown key, scancode=' + str(scancode))
                except BlockingIOError:
                    pass
            self.device.ungrab()
            que.put(id_card)


        thread = threading.Thread(target=run, name='barcode_scanner', args=(self.que,))
        thread.start()
        return self.que.get()

    def register_listener(self, callback):
        self._listeners.append(callback)
