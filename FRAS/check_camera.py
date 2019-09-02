import cv2


def camer():
    cap = cv2.VideoCapture(0)

    while(True):
        #capture frame-by-frame
        ret, frame  = cap.read()
        #operations on the frame come here
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #display the resulting frame
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # when everything is done
    cap.release()
    cv2.destroyAllWindows()

