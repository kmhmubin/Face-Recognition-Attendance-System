import csv
import re
import cv2
import os


# counting the numbers


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def check_name(name):
    matches = re.findall(r"^[ A-Za-z]+$", name)
    if len(matches) > 0:
        return True
    return False


def check_student_csv_file():
    try:
        file = open("StudentDetails"+os.sep+"StudentDetails.csv", 'r+')
    except FileNotFoundError:
        with open("StudentDetails"+os.sep+"StudentDetails.csv", 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Id", "Name"])
    except Exception as e:
        print(str(e))
    else:
        read_csv = csv.reader(file)
        if not list(read_csv)[0] == ["Id", "Name"]:
            write_csv = csv.writer(file)
            write_csv.writerow(["Id", "Name"])


# Take image function

def takeImages():

    Id = input("Enter Your Id: ")
    name = input("Enter Your Name: ")

    if(is_number(Id) and check_name(name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for(x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum+1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage" + os.sep + name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                # display the frame
                cv2.imshow('frame', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()

        # Below function checks if StudentDetails.csv
        # file exists or Not
        # if it exists then it will check if
        # it contains Id, name header or not
        # if any of the conditions is not met,
        # it will do the needful
        check_student_csv_file()

        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open("StudentDetails"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
    else:
        if(is_number(Id)):
            print("Enter Alphabetical Name")
        elif(not check_name(name)):
            print("Name can only contain Alphabets and Spaces")

        if(name.isalpha()):
            print("Enter Numeric ID")
