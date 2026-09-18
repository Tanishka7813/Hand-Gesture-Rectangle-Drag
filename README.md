\# Hand Gesture Rectangle Drag



A real-time computer vision project that allows users to drag rectangles on the screen using hand gestures, without touching the screen.



\## Features



\- Real-time hand tracking using a webcam

\- Touchless rectangle dragging

\- Pinch gesture for selecting and dragging

\- Multiple draggable rectangles

\- Smooth rectangle movement

\- Visual hand landmarks and connections

\- Simple keyboard control to quit the application



\## Technologies Used



\- Python

\- OpenCV

\- CVZone

\- MediaPipe

\- NumPy



\## How It Works



The webcam captures the user's hand movements in real time.



The program detects the hand and tracks the index and middle fingertips. When the fingers come close together, the program recognizes it as a pinch gesture.



If the pinch gesture is performed over a rectangle, that rectangle becomes active and follows the user's finger movement.



\## Installation



1\. Clone this repository:



```bash

git clone https://github.com/Tanishka7813/Hand-Gesture-Rectangle-Drag.git



2.Open the project folder:

cd Hand-Gesture-Rectangle-Drag



3.Install the required dependencies:

pip install -r requirements.txt



Run the Project

Run: python drag.py



Make sure your webcam is connected and accessible.



Controls:

1.Pinch index and middle fingers → Select and drag a rectangle

2\.Q → Quit the application



Project Structure:

Hand-Gesture-Rectangle-Drag/

│

├── drag.py

├── hand\_landmarker.task

├── requirements.txt

└── README.md



Applications:

This project demonstrates touchless human-computer interaction using computer vision and hand gestures.



Author:

Tanishka Jaiswal



