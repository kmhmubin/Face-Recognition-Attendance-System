import cv2
import numpy as np 
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import logging as log
import datetime as dt
from time import sleep



cx = 160
cy = 120

# names related to ids: example
names = ['None', 'tasnim','Amir'] 


#iniciate id counter
id = 0





xdeg = 150
ydeg = 150


  # calling the harr cascade file
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer=cv2.face.LBPHFaceRecognizer_create()
log.basicConfig(filename='database.log',level=log.INFO)
# opening the database file using append mode
file = open("/home/pi/Testnew/data_log.csv", "a")




	


images=[]
labels=[]
for filename in os.listdir('Dataset'):
	im=cv2.imread('Dataset/'+filename,0)
	images.append(im)
	labels.append(int(filename.split('.')[0][0]))
	



recognizer.train(images,np.array(labels))
print 'Training Done . . . '

font = cv2.FONT_HERSHEY_SIMPLEX
cap=cv2.VideoCapture(0)
lastRes=''
count=0

print ' Done 2 . . . '
log.info("Date Time , Student Name \n")
file.write("-------------------------------------------------  \n")
file.write("        Date:"+str(dt.datetime.now().strftime("%d-%m-%Y"))+"        \n")
file.write("-------------------------------------------------  \n")
file.write("Time , Student Name \n")
while(1):
	ret, frame=cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	faces = faceCascade.detectMultiScale(gray)
	count+=1

	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                  
                
                id,confidence=recognizer.predict(gray[y:y+h, x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 40):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    log.info(str(dt.datetime.now()) + ","+ str(id)+"\n")
                    file.write(str(dt.datetime.now().strftime("%H:%M:%S")) + ","+ str(id)+"\n")

                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
        
                cv2.putText(frame, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(frame, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

                
                #cv2.putText( frame, str(lastRes), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
                


		

	
	
	cv2.imshow('frame',frame)
	k = 0xFF & cv2.waitKey(10)
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()

