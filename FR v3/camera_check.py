# checking the webcam/camera module
import cv2

#calling the videocapture module

cap = cv2.videocapture(0)

while(True):
    #capture frame-by-frame
    ret, frame = cap.read()

    #display the result
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#when everyting is done , exicute
cap.release()
cv2.destroyAllWindows()
