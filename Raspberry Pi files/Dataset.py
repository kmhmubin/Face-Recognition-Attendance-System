import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
import numpy
import io

#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()



cam = cv2.VideoCapture(0) 
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)



Id=raw_input('enter your id')
sampleNum=0
while(True):
    ret, img = cam.read()    #cam output
    cv2.imshow('frame',img)   #screen output
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   #convert black and white
    faces = detector.detectMultiScale(gray, 1.3, 5)  #detect face
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)  #framing
        cv2.imwrite("Dataset/"+Id +'_'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w]) #saving data in id
        #incrementing sample number 
        sampleNum=sampleNum+1 
        #saving the captured face in the dataset folder
        

        cv2.imshow('frame',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>30:
        break
cam.release()
cv2.destroyAllWindows()
