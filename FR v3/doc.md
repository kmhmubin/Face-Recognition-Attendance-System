<!-- workthrough documentation -->
<!-- This documentation only for fr v3 -->
# Intrducton

In this version we are going to work with dlib lib and face_recognition packages. TO use those packages we need to setup the necessery packages.

## What is Dlib Library?

Dlib is a modern C++ toolkit containing machine learning algorithms and tools for creating complex software in C++ to solve real world problems. It is used in both industry and academia in a wide range of domains including robotics, embedded devices, mobile phones, and large high performance computing environments.This library also work with python.

[Dlib Library Full Documentaion](http://dlib.net/)

## Face Recognition Library Module

To recognisze and manipulate faces we need to algorithm.We are going to use face recognition library which is built using dlib's state-of-the-art face recognition built with deep learning. The model has an **accuracy** of **99.38%** on the Labeled Faces in the Wild benchmark.It also provide simple command tool to do work.

## Install Dlib on Ubuntu

The step by step instructions to install Dlib on Ubuntu.Install all the libraries as Admin which  will help to errorless install.

#### System Information

* Ubuntu 18.04 LTS
* Anaconda 2019.07
* Python 3.6



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

sudo -H pip3 install -U pip numpy scipy matplotlib scikit-image scikit-learn ipython

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







