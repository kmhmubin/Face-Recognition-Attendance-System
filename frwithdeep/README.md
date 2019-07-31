# Face Recognition with deep learning and opencv

In this project we use the deep machine learning for best result. To get higher accuracy rate in face recognition we use more than 850 picture. Although it not that much big dataset compate to other. But we get what we wanted. our project have now around 90% accuracy rate.

## File Index

In this photo we can see the dirctory list of our project.

[file direcotory list](Document Metarial/Doc Images/frwithdeep dirctorylist.png)

---------------------------------------------------------

## File Directory list details

* **dataset:**  In dataset folder we collect many picture of popular                   actors. We organize the photos by their name.
* **dlib:** dlib is a c++ library file which help to analysi the face in our project.

* **venv :** virtual enviroment for python. Best to use it.
* **camera_check.py :** To check the camera working or not.
* **encode_face.py :** To train the faces and create a pickle object which store all the data about faces.
* **encodings.pickle :** In this object all the data about faces are store.
* **recognize_face_video.py :** real time streaming , detection and recognize the faces.
* **google_image_downloader.py :** to automatice download images from google image search.
* **search_bing_api :** to download images form bing image search engine automaically.

------------------------------------------------------------

# Install Process
 
we need to install so many packages and library for sucessfully run the file. All the steps are below.

## What is Dlib Library?

Dlib is a modern C++ toolkit containing machine learning algorithms and tools for creating complex software in C++ to solve real world problems. It is used in both industry and academia in a wide range of domains including robotics, embedded devices, mobile phones, and large high performance computing environments.This library also work with python.

[Dlib Library Full Documentaion](http://dlib.net/)

## Face Recognition Library Module

To recognisze and manipulate faces we need to algorithm.We are going to use face recognition library which is built using dlib's state-of-the-art face recognition built with deep learning. The model has an **accuracy** of **99.38%** on the Labeled Faces in the Wild benchmark.It also provide simple command tool to do work.

## Install Dlib on Ubuntu

The step by step instructions to install Dlib on Ubuntu.Install all the libraries as Admin which  will help to errorless install.

**step 1: Install OS libraries**

```
sudo apt-get install build-essential cmake pkg-config

sudo apt-get install libx11-dev libatlas-base-dev

sudo apt-get install libgtk-3-dev libboost-python-dev

```
**step 2:Install Python libraries**

Try to use Virtual Environment to install Python libraries.

```
sudo apt-get install python-dev python-pip python3-dev python3-pip

sudo -H pip3 install -U pip numpy scipy matplotlib scikit-image scikit-learn ipython opencv-contrib-python



```
**step 3: Compile DLib**

Clone the code from github:
```
git clone https://github.com/davisking/dlib.git
```
Build the main dlib library
```
cd dlib
mkdir build; cd build; cmake ..; cmake --build .
```
Build and install the Python extensions:
``` 
cd ..
python3 setup.py install
```
*If there any problem to install the python extension use **sudo -H** before install.*

## Install Face Recogniton Module on Ubuntu

First, make sure you have dlib already installed with Python bindings.Then, install this module from pypi using pip3

```
sudo -H pip3 install face_recognition
```
---------------------------------

## Virtual Enviroment

First we need to install the virtual evn in our os. 


**step 1: Install venv in os**
```
sudo pip install virtualenv
```

Then go to your work folder run the terminal

**step 2:Creating venv in workpath**

```
mkdir nameofenv
eg. mkdir venv

cd venv
virtualenv env1

```

**step 3:Activate Virtual env**

```
source virtualenv/env1/bin/activate
```

--------------------------------------

## Downloading Images Dataset automatically

We are going to download our images for our training dataset. To do that,we need to download so many images and it's not easy to download manually and also time consuming. We have a proper solution for this problem. How about we are going to build a script which are going to download images automatically in order and save in a directory with sub-folder. Isn't it a best solution for our problem.So lets make a script.

Before we start building our script there are 2 options. Those are

* [Google API image downloader](https://google-images-download.readthedocs.io/en/latest/arguments.html)
* [Bing API images downloader](https://www.pyimagesearch.com/2018/04/09/how-to-quickly-build-a-deep-learning-image-dataset/)

Follow Those link to build your own image downloader.

## Terminal code to run the python files

* **encode_face.py**

```
python encode_faces.py --dataset dataset --encodings encodings.pickle
```
It will run the encode_face python file and create a data object encodings pickle file.

* **recognize_face_video.py**
```
python recognize_faces_video.py --encodings encodings.pickle \

## after show this " > " symbole use this code 

  --output output/webcam_face_recognition_output.avi --display 1
```
It will run the recognize_faces_video python file along with encodings pickle and start webcam and recognize the person in the database.