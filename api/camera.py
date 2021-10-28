import cv2, queue, threading, time # #Queue 模塊 是提供佇列操作的模塊。佇列 (First In First Out) 是線程間最常用的交換數據的形式。
from api.LED import LED
import glob, os

# bufferless VideoCapture
class VideoCapture:
    def __init__(self, name, height=720, width=1280):
        self.cap = None 
        self.LED0 = LED()
        self.q = queue.Queue() #佇列 (First In First Out) 是線程間最常用的交換數據的形式。
        try:
            self.cap = cv2.VideoCapture(name)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G')) # 4個字符表示的視頻的編碼器格式
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75) # 0.75 表示“自動曝光，自動光圈”（Auto to Manual）
            self.setWidth(width)
            self.setHeight(height)
            #self.cap.release()
            #self.cap = None
        except:
            print("camera connect error")

    def setWidth(self, width):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def setHeight(self, height):
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    def isOpened(self):
        return self.cap.isOpened()
        
    def open(self, name=0, height=720, width=1280):
        if self.cap == None:
            # 自動尋找相機索引(ID)並設定相機參數
            Camera_path = glob.glob('/dev/vi*') # ('dev/video1')
            Camera_name = os.path.split(Camera_path[0])[1] # video1
            Camera_id = int(Camera_name[-1]) # 1 or 0 or else
            self.cap = cv2.VideoCapture(Camera_id)
            self.cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
            self.setWidth(width)
            self.setHeight(height)
            
        time.sleep(3) # 執行調自動接著調手動  他就會發生錯誤  但加個時間delay就不會了
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) # 0.25表示“手動曝光，手動光圈”（Auto to Manual），然後cv2.CAP_PROP_EXPOSURE才能正常使用
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 0.008) # 設置曝光絕對值
        self.t2 = threading.Thread(target = self.LED0.LED_blink)
        self.t2.start()
        self.t1 = threading.Thread(target = self._reader)
        self.t1.daemon = True # daemon的值默認為False；daemon屬性為True，主線程運行結束時不對這個子線程進行檢查而直接退出，同時所有daemon為True的子線程將隨主線程一起結束，而是否運行完成。
        self.t1.start()

    def _reader(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True): # 當線程t是可運行的
            # cap.read()是按幀讀取，其會返回兩個值：ret,frame（ret是布爾值，如果讀取幀是正確的則返回True，如果文件到讀取結束，它的返回值為False；那個Frame為圖像的三維矩陣BGR形式。）
            ret, frame = self.cap.read()
            if not ret: # 沒有讀取到影像
                break
            if not self.q.empty(): # 如果q不是空的
                try:
                    self.q.get_nowait() # discard previous (unprocessed) frame 。也等於 q.get(False) 
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        success = True
        if not self.q.empty(): # 如果q不是空的
            result = self.q.get()
        else:
            success = False
            result = False
    
        return success, result
    
    def release(self):
        self.t1.do_run = False
        self.t1.join()
        self.t2.do_run = False
        self.t2.join()
        self.LED0.LED_close()
        #self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
        self.cap.release()
        self.cap = None

