from tkinter import *
import cv2
from PIL import Image,ImageTk
from api.camera import VideoCapture

def take_snapshot():
    img = cv2.flip(root.cv2image, 0)
    cv2.imwrite('../Jimmytest/copy.jpg',img)
    print("capture")

def video_loop():
    success, img = camera.read()  # 從攝像頭讀取照片
    if success:
            cv2.waitKey(0) #等按鈕
            root.cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA) # 轉換顏色從BGR到RGBA
            current_image = Image.fromarray(root.cv2image) # 將影象轉換成Image物件  #這兩行是從cv轉到 PIL image
            imgtk = ImageTk.PhotoImage(image=current_image)
            panel.imgtk = imgtk
            panel.config(image=imgtk)
            root.after(100, video_loop) # 1毫秒之後重跑此function

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

camera = VideoCapture(0, height= 720, width=1280)  #攝像頭 接上板子應該是 0
camera.open()

root = Tk()
root.title("opencv + tkinter")
#root.protocol('WM_DELETE_WINDOW', detector)
panel = Label(root)  # initialize image panel
panel.pack(padx=10, pady=10)
root.config(cursor="arrow")


# 修改不同參數請調整此值
'''
0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
5. CV_CAP_PROP_FPS Frame rate.
6. CV_CAP_PROP_FOURCC 4-character code of codec.
7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
'''
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
