# Human-Face-Recognition-Attendance-System
A system which can recognize face and match with its own database and take the attendance automatic.

**Abstract:**

Authentication is one of the significant issues in the era of information system. Among other things, human face recognition (HFR) is one of known techniques which can be used for user authentication. However, it is difficult to estimate the attendance precisely using each result of face recognition independently because the face detection rate is not sufficiently high.

Continuous observation improves the performance for the estimation of the attendance we constructed the lecture attendance system based on face recognition, and applied the system to classroom. This paper first review the related works in the field of attendance management and face recognition. Then, it introduces our system structure and plan.

Finally, experiments are implemented to provide as evidence to support our plan. The result shows that continuous observation improved the performance for the estimation of the attendance.

**Keywords:** _Human Face Recognition, Attendance system, Raspberry Pi_

**Introduction and Background:**

As we are making a system which can recognize face and match with its own database. It will make the attendance system more authentic. Our primary goal is to help the lecturers, improve and organize the process of track and manage student attendance and absenteeism.

Additionally, we seek to provide a valuable attendance service for both teachers and students. Reduce manual process errors by provide automated and a reliable attendance system uses face recognition technology.

Increase privacy and security which student cannot presenting himself or his friend while they are not. Flexibility, Lectures capability of editing attendance records.

**Objectives:**

Our aim is to build up a face recognition system where a human will stand in front of the system and a camera will match the face along with its database.

There will no extra RFID card people need to carry any more and this system will be the most authentic system of taking attendance. We will try to build this system as efficient as possible.

**Scope:**

We have divided our work into two parts.

   1. Sensing Face and Capture.

   2. Match with database.

**Methodology and Approach:**

Face detection involves separating image windows into two classes; one containing faces (turning the background (clutter).

The first step is a classification task that takes some arbitrary image as input and outputs a binary value of yes or no, indicating whether there are any faces present in the image. The second step is the face localization task that aims to take an image as input and output the location of any face or faces within that image as some bounding box with (x, y, width, height).

After taking the picture the system will compare the equality of the pictures in its database and give the most related result.

There is still no work combining image processing by raspbian operating system with open CV platform. So, we want to introduce this model.



**Software Used:**

Python, Open CV , Raspbian OS

**Components:**

The total estimated components to complete the project is provided in Table 2.

| Name of Item |
| --- |
| HD Webcam ( Camera Module) |
| Raspberry Pi |
| SD card |
| Battery |
| Wires and Other |

Table 2: Component for the project



**Time-plan:**

List the deliverables with specific dates so that you can make concerted effort to achieve them.

| Serial | Description |
| --- | --- |
| Task 1 | Buying product |
| Task 2 | Learning image processing and applying it |
| Task 3 | Write the system code |
| Task 4 | Use camera for image processing |
| Task 5 | Assembling everything |

Table 1: List of all tasks



**Expected Outcomes:**

The system stores the faces that are detected and automatically marks attendance.

Ease of use is manipulate and recognize the faces in real time using. Multiple face detection. Multipurpose software Can be used in different places.

Ease of use is manipulate and recognize the faces in real time using. Multiple face detection. Multipurpose software Can be used in different places.



**References:**

[1]The best work is &quot;AUTOMATED ATTENDANCE MACHINE USING FACE DETECTION AND RECOGNITION.&quot; Of UNIVERSITY OF NAIROBI. Another work is &quot;Automatic Attendance System Using Face Recognition.&quot; Of IJMTER University.
