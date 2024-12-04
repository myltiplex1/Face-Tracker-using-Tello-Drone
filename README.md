# Tello Drone Face Tracking Project
## Overview
This project demonstrates how to control a Tello drone to track and follow a face using computer vision and PID control. The drone detects the face using a real-time face detection model and adjusts its position accordingly.

## The main functionality includes:

1. Face detection using medeiapipe.
2. Drone control based on the detected face's position and size.
3. Safety feature to automatically land the drone if no face is detected for a predefined period.

## Requirements
To run this project, you'll need the following:
- Python 3.x
- Tello drone and djitellopy library
- OpenCV for image processing
- NumPy for numerical operations
- mediapipe for face detection

You can install the required Python libraries with:

## Project Setup
1. Initialize the Drone:
The initialize_drone() function sets up the drone for flight, checks the battery level, calibrates the gyroscope, and starts the video stream.
2. Face Detection and Tracking:
The detect_and_track_face() function captures frames from the drone’s camera, uses the meshDetector.py to detect faces, and sends movement commands to the drone based on the face’s location and size.
3. PID Control for Stability:
PID control is used to adjust the drone’s yaw (rotation) and forward/backward speed based on the face’s position in the frame.
4. Safety Measures:
If no face is detected for a specified amount of time, the drone will automatically land.

## Usage
Run the Project
After setting up the required libraries and connecting the Tello drone, you can run the project using the following command:

python3 face_tracker.py

This will start the drone, initiate the face detection, and begin tracking.

## Important Notes
- Ensure that your drone has sufficient battery charge.
- The drone will land automatically if no face is detected within a set time.
- The height.py can be used to know the drone's height.
