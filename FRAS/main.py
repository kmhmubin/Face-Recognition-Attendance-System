import os  # accessing the os functions
import check_camera
import Capture_Image
import Train_Image
import Recognize
import time


# creating the title bar function

def title_bar():
    os.system('cls')  # for windows

    # title of the program

    print("\t**********************************************")
    print("\t***** Face Recognition Attendance System *****")
    print("\t**********************************************")


# creating the user main menu function

def mainMenu():
    title_bar()
    print()
    print(10 * "*", "WELCOME MENU", 10 * "*")
    print("[1] Check Camera")
    print("[2] Capture Faces")
    print("[3] Train Images")
    print("[4] Recognize & Attendance")
    print("[5] Auto Mail")
    print("[6] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))
        except ValueError:
            print("Invalid Choice. Enter 1-6\n Try Again")
        except Exception as e:
            print(str(e))
        else:
            try:
                if choice == 1:
                    checkCamera()
                elif choice == 2:
                    CaptureFaces()
                elif choice == 3:
                    Trainimages()
                elif choice == 4:
                    RecognizeFaces()
                elif choice == 5:
                    os.system("py automail.py")
                    mainMenu()
                elif choice == 6:
                    print("Thank You")
                    break
                else:
                    print("Invalid Choice. Enter 1-6")
                    time.sleep(1)
                    mainMenu()
            except Exception as e:
                print("Some Error occurred! - ", str(e))


# ---------------------------------------------------------
# calling the camera test function from check camera.py file

def checkCamera():
    check_camera.camer()
    input("Enter any key to return main menu")
    mainMenu()


# --------------------------------------------------------------
# calling the take image function form capture image.py file

def CaptureFaces():
    Capture_Image.takeImages()
    input("Enter any key to return main menu")
    mainMenu()


# -----------------------------------------------------------------
# calling the train images from train_images.py file

def Trainimages():
    Train_Image.TrainImages()
    input("Enter any key to return main menu")
    mainMenu()


# --------------------------------------------------------------------
# calling the recognize_attendance from recognize.py file

def RecognizeFaces():
    Recognize.recognize_attendence()
    input("Enter any key to return main menu")
    mainMenu()


# ---------------main driver ------------------
mainMenu()
