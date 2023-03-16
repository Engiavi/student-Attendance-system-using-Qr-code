import cv2
import numpy as np
# import time
from pyzbar.pyzbar import decode

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    qrcode = decode(gray_img)

    for obj in qrcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        
        pts = pts.reshape((-1,1,2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        qrcodeData = obj.data.decode("utf-8")
        qrcodeType = obj.type
        string = "Data " + str(qrcodeData) + " | Type " + str(qrcodeType)
        
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        print("qrcode: "+qrcodeData +" | Type: "+qrcodeType)

cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    m=decoder(frame)
    # time.sleep(1)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(3)
    if code == ord('q'):
        break
