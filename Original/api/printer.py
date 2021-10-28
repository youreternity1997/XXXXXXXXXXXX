import serial
import Adafruit_BBIO.UART as UART

class Printer:
    def __init__(self, device_name='/dev/usb/lp0'):
        UART.setup("UART4")
        self.device = None
        try:
            self.device = open(device_name, 'wb') # 試圖打開影印機('wb':用於讀寫二進制文件，)
            #self.device = serial.Serial(device_name, 9600)
        except:
            print("Device not found or cable not plugged in.")

    def prints(self, content = ""):
        if self.device is None:
            try:
                self.device = open(device_name, 'wb') # 試圖打開影印機('wb':用於讀寫二進制文件，)
                #self.device = serial.Serial(device_name, 9600)
            except:
                print("Device not found or cable not plugged in.")
                return
            print("USB error")
        self.device.write(content) # 執行列印紙條

    def close(self):
        if self.device is None:
            print("USB error")
            return
        self.device.close() # 關閉影印機
