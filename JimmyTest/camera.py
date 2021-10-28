from tkinter import *
import cv2
from PIL import Image,ImageTk
from api.camera import VideoCapture
import time

def take_snapshot(t):
    img = cv2.flip(root.cv2image, 0)
    #cv2.imwrite('..\Jimmytest\copy.jpg',img)
    cv2.imwrite(("20211020/" + t + ".jpg"), img)
    print("capture")

def video_loop():
    success, img = camera.read()  # 從攝像頭讀取照片
    if success:
            print('img.shape=', img.shape)
            cv2.waitKey(10) #等按鈕
            root.cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA) # 轉換顏色從BGR到RGBA
            current_image = Image.fromarray(root.cv2image) # 將影象轉換成Image物件  #這兩行是從cv轉到 PIL image
            imgtk = ImageTk.PhotoImage(image=current_image)
            panel.imgtk = imgtk
            panel.config(image=imgtk)
            t = time.localtime()
            print('t=', t)
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('t=', t)
            take_snapshot(t)
            root.after(1000, video_loop) # 1毫秒之後重跑此function

def plus(val):
    camera.set(val, camera.get(val)+1)
    print(val, camera.get(val))

def minus(val):
    camera.set(val, camera.get(val)-1)
    print(val, camera.get(val))

def printdetail(val):
    # print(val, camera.get(val))
    # print('0', camera.get(cv2.CAP_PROP_POS_MSEC))
    # print('1', camera.get(cv2.CAP_PROP_POS_FRAMES))
    # print('2', camera.get(cv2.CAP_PROP_POS_AVI_RATIO))
    # print('3', camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    # print('4', camera.get(cv2.CAP_PROP_FRAME_HEIGHT ))
    # print('5', camera.get(cv2.CAP_PROP_FPS ))
    # print('6', camera.get(cv2.CAP_PROP_FOURCC ))
    # print('7', camera.get(cv2.CAP_PROP_FRAME_COUNT ))
    # print('8', camera.get(cv2.CAP_PROP_FORMAT ))
    # print('9', camera.get(cv2.CAP_PROP_MODE ))
    print('BRIGHTNESS', camera.get(cv2.CAP_PROP_BRIGHTNESS ))
    print('CONTRAST', camera.get(cv2.CAP_PROP_CONTRAST ))
    print('SATURATION', camera.get(cv2.CAP_PROP_SATURATION))
    print('HUE', camera.get(cv2.CAP_PROP_HUE))
    print('GAIN', camera.get(cv2.CAP_PROP_GAIN ))
    print('EXPOSURE', camera.get(cv2.CAP_PROP_EXPOSURE ))
    # print('16', camera.get(cv2.CAP_PROP_CONVERT_RGB ))
    # # print(camera.get(cv2.CAP_PROP_WHITE_BALANCE  ))
    # print('18', camera.get(cv2.CAP_PROP_RECTIFICATION  ))

#camera = cv2.VideoCapture(0)  #攝像頭 接上板子應該是 0
camera = VideoCapture(0, height= 720, width=1280)
camera.open()

root = Tk()
root.title("opencv + tkinter")
#root.protocol('WM_DELETE_WINDOW', detector)
panel = Label(root)  # initialize image panel
panel.pack(padx=10, pady=10)
root.config(cursor="arrow")
val = 15
btn = Button(root, text="capture", command=take_snapshot)
btn.pack(fill="both", expand=True, padx=10, pady=10)
btn = Button(root, text="+++++", command=lambda: plus(val))
btn.pack(fill="both", expand=True, padx=10, pady=10)
btn = Button(root, text="-----", command=lambda: minus(val))
btn.pack(fill="both", expand=True, padx=10, pady=10)
btn = Button(root, text="print", command=lambda: printdetail(val))
btn.pack(fill="both", expand=True, padx=10, pady=10)

video_loop()

root.mainloop()
# 當一切都完成後，關閉攝像頭並釋放所佔資源
camera.release()
cv2.destroyAllWindows()
