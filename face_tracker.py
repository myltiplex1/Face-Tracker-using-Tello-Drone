import cv2
import time
import numpy as np
from djitellopy import Tello
from meshDetector import FaceMeshDetector

def initialize_drone():
    """Initializes and prepares the Tello drone for flight."""
    drone = Tello()
    drone.connect()
    print(f"Battery Level: {drone.get_battery()}%")
    
    # Ensure the battery is sufficiently charged
    if drone.get_battery() < 20:
        print("Warning: Battery is too low to take off. Please charge the drone.")
        return None

    # Calibrate drone gyroscope (optional but recommended)
    print("Calibrating drone...")
    drone.send_command_with_return("rc 0 0 0 0")
    time.sleep(2)

    # Start video streaming
    drone.streamoff()
    drone.streamon()

    # Take off and adjust initial height
    drone.takeoff()
    print("Drone taking off...")
    time.sleep(4)  # Allow the drone to stabilize

    # Send hover command to stop any drift
    drone.send_rc_control(0, 0, 0, 0)
    print("Hovering to stabilize...")

    # Move up slightly to avoid ground effects
    drone.move_up(95)
    print("Drone moved to initial height.")

    return drone

def tello_get_frame(drone, width=640, height=480):
    """Captures and resizes the frame from the drone's camera."""
    frame_read = drone.get_frame_read()
    frame = frame_read.frame
    frame = cv2.resize(frame, (width, height))
    return frame

def track_face(drone, face_center_x, face_width, frame_width, pid, prev_error):
    """Adjusts the drone's movement based on face position and size."""
    error = face_center_x - frame_width // 2  # Horizontal error
    yaw_speed = pid[0] * error + pid[1] * (error - prev_error)
    yaw_speed = int(np.clip(yaw_speed, -30, 30))  # Limit yaw speed to avoid abrupt turns

    # Forward/backward control based on face size
    ideal_face_width = 150  # Ideal width when face is at the correct distance
    fb_speed = 0
    if face_width < ideal_face_width - 20:  # Too far, move forward
        fb_speed = 20
    elif face_width > ideal_face_width + 20:  # Too close, move backward
        fb_speed = -20

    # Send movement commands to the drone
    drone.send_rc_control(0, fb_speed, 0, yaw_speed)
    print(f"Yaw Speed: {yaw_speed}, Forward/Backward Speed: {fb_speed}")
    return error

def detect_and_track_face(drone, detector):
    """Detects and tracks a face, adjusting drone position as needed."""
    w, h = 640, 480  # Frame dimensions
    pid = [0.5, 0.5, 0]  # PID coefficients for smoother control
    prev_error = 0  # Previous error for PID control
    no_face_timeout = 30  # Time (seconds) before landing if no face is detected
    last_face_time = time.time()  # Timestamp for last detected face

    while True:
        frame = tello_get_frame(drone, w, h)
        detector.detect_faces(frame)

        if detector.results and detector.results.multi_face_landmarks:
            last_face_time = time.time()  # Reset no-face timer
            landmarks = detector.results.multi_face_landmarks[0]

            # Calculate bounding box around the detected face
            ih, iw, _ = frame.shape
            x_min, x_max, y_min, y_max = iw, 0, ih, 0
            for lm in landmarks.landmark:
                x, y = int(lm.x * iw), int(lm.y * ih)
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y)
                y_max = max(y_max, y)

            # Calculate face center and width
            face_center_x = (x_min + x_max) // 2
            face_width = x_max - x_min

            # Track the face using PID control
            prev_error = track_face(drone, face_center_x, face_width, w, pid, prev_error)
            print(f"Face Center X: {face_center_x}, Face Width: {face_width}")
        else:
            print("No face detected.")
            # Check if timeout has occurred
            if time.time() - last_face_time > no_face_timeout:
                print("No face detected for too long. Landing...")
                break

        # Display the frame for debugging
        cv2.imshow("Tello Face Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key press
            print("Exiting...")
            break

    cv2.destroyAllWindows()

def main():
    """Main function to execute face tracking with the Tello drone."""
    try:
        # Initialize face detector and drone
        detector = FaceMeshDetector(effects=None)
        drone = initialize_drone()

        if drone is None:  # Ensure drone initialization was successful
            print("Drone initialization failed.")
            return

        # Begin face tracking
        detect_and_track_face(drone, detector)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure safe landing and stream shutdown
        if 'drone' in locals() and drone is not None:
            try:
                print("Landing drone...")
                drone.land()
            except Exception as e:
                print(f"Error during landing: {e}")
            drone.streamoff()
            print("Stream turned off. Exiting program.")

if __name__ == "__main__":
    main()
