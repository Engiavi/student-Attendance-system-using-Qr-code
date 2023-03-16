import cv2
import numpy as np
import pandas as pd
import json
import datetime
import os
from pyzbar.pyzbar import decode

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    qrcode = decode(gray_img)
    data = []
    processed_data = set()
    for obj in qrcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        qrcodeData = obj.data.decode("utf-8")
        qrcodeType = obj.type
        string = "Data " + str(qrcodeData) + " | Type " + str(qrcodeType)
        data_dict = json.loads(qrcodeData)
        # print(type(data_dict))
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        print("qrcode: "+ qrcodeData +" | Type: "+qrcodeType)
        firstname = data_dict.get('firstname')
        lastname = data_dict.get('lastname')
        emailid = data_dict.get('emailid')
        
        # Check if the data is already present in the set
        if qrcodeData not in processed_data:
            # Add the data to the set
            processed_data.add(qrcodeData)
            # Get the current time
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.append({"firstname": firstname, "lastname": lastname,"emailid":emailid, "time": time})
    return data

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,1920)
cap.set(4,1080)

data = []
while True:
    ret,frame = cap.read()
    data = data + decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(3)
    if code == ord('q'):
        break

# Remove duplicate rows from the dataframe

df = pd.DataFrame.from_records(data, columns=["firstname", "lastname", "emailid", "time"])
df = df.drop_duplicates(subset=["firstname", "lastname", "emailid"])

# Get the number of existing qrcode files
qrcode_files = len([f for f in os.listdir('excel') if f.startswith('qrcode') and f.endswith('.xlsx')])

# Create a unique file
filename = "excel/qrcode" + str(qrcode_files + 1) + ".xlsx"
df.to_excel(filename, index=False)

print("Data saved to " + filename + ".")