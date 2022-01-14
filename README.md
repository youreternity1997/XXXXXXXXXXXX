# Drug_Detector
## database
![](https://i.imgur.com/hYHAqYF.png)
![](https://i.imgur.com/hvS2vLm.png)
已修改->把cape_position table 去掉->發現這樣好像比較好用(在position確定不變的情況下）



=======================================================================================
1.~~ : 聖鋒工程師所撰寫部分。

2.1.0_20210630 : 
    1. 註解api/camera.py
    1. api/camera.py中新增自動抓取相機ID(camera_id)(line:113~118)
    
2.1.1_20210725~20210726 : 
    1. 註解api中LED.py、barcode_scanner_serial.py、VKeyboard.py、screenlock.py、printer.py、camera.py
    
2.1.2_20210727 : 
    1. 註解api/detect_battery.py

2.2.0_20211029 : 
    1. 在DD.py中新增自動抓取相機ID(camera_id)(line:113~118)
    2. 固定式改成自動式抓取試紙與線段(creat_cor、MED)(line:619~623、1696) : 修改cor.main()和MED()，用scipy抓取區域    最小值、區域最大值當作線段邊界，改成全自動分類線段
    2. 對旋轉校正的QRcode影像除雜訊(line:1263~1331) : 降躁讓影像旋轉校正更正確
    3. 解決身分證資料夾重複(line:1680~1681)
    4. api/camera.py修改: .set(cv2.CAP_PROP_FPS, 5)，FPS降低成5fps(原本為30fps)
    5. api/camera.py修改: .set(cv2.CAP_PROP_EXPOSURE, 0.0035)，0.05變成0.0035
    6. JimmyTest/camera.py修改: .set(cv2.CAP_PROP_FPS, 5)，FPS降低成5fps(原本為30fps)
    7. 在DD.py中新增自動抓取相機ID(camera_id)(line:113~118)




對旋轉校正的QRcode影像除雜訊(line:1263~1331) : 降躁讓影像旋轉校正更正確。