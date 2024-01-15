from ultralytics import YOLO
import cv2
import tkinter as tk
# import easyocr
import matplotlib.pyplot as plt
from tkinter import messagebox
from util import *
import cv2
from paddleocr import PaddleOCR

auth = [["34EYN860"],["34GJG620"],["34BZ5195"],["54AHS236"],["34FM6073"],["06EBA052"],["38J1277"],["34NJ7554"],["34FCB257"],["34EKV745"],["34RE4322"],["06GKN62"],["34KC0038"],["06LAZ97"],["34ALP090"],["34NH0632"],["34V0769"], ["06ARS06"],["34FUM086"],["34FSU605"],["34JS8849"],["34EE3170"],["34RH4466"],["34EOY935"],["34TEE19"],["34ADG69"],["34HV9205"],["30JS9946"]]

characters = set()
for sublist in auth:
    for item in sublist:
        characters.update(item)
allowList = ''.join(characters) 

# messagebox için
# root = tk.Tk()
# root.withdraw()
# results = []

ocr_model = PaddleOCR(lang='en',use_gpu=True)
licensePlateDetector = YOLO('./models/best.pt')

# cap = cv2.VideoCapture('./videos/q.mp4')
cap = cv2.VideoCapture('rtsp://admin:admin123@192.168.0.22:554')

ret = True
while ret:
    ret, frame = cap.read()
    if ret:
        # görüntü tersse       
        # frame = cv2.flip(frame, 0)
        # görüntü aynalanmışsa       
        # frame = cv2.flip(frame, 1)
        cv2.imshow("ss",frame)

        licensePlates = licensePlateDetector(frame)

        for li in licensePlates:
            for licensePlate in li.boxes.data.tolist():
                x1, y1, x2, y2, score, classId = licensePlate
                licensePlateCrop = frame[int(y1):int(y2), int(x1): int(x2), :]
            
                H,W = licensePlateCrop.shape[:2]
                H,W=H*2,W*2
                resizedImg = cv2.resize(licensePlateCrop,(W,H))
                
                licensePlateCropGray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
                thresholdImg = cv2.threshold(licensePlateCropGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                plt.axis("off") 
                plt.imshow(thresholdImg, cmap='gray')
                cv2.imshow("ss2",thresholdImg)
                # plt.show()
                result = ocr_model.ocr(thresholdImg)
            
                try:
                    sa = result[0][0][1][0]
                except:
                    sa = 'sa'
                cv2.imshow("ss",frame)
                result = ControlTheLicensePlate(sa,auth,thresholdImg)

                if result is not None:
                    print(result)
                    # messagebox.showinfo("plaka", result)
