from djitellopy import Tello
import time

# Initialize the Tello drone
drone = Tello()

# Connect to the drone
drone.connect()

try:
    print("Measuring height. Use Ctrl+C to stop.")
    while True:
        # Get and print the drone's height
        height = drone.get_height()
        print(f"Current height: {height} cm")
        
        # Wait for a short interval before the next measurement
        time.sleep(0.5)  # Measure every 0.5 seconds

except KeyboardInterrupt:
    print("Stopped height measurement.")

finally:
    # Disconnect from the drone
    drone.end()