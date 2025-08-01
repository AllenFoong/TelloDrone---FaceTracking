"""
controllers/console.py

Manual control of DJI Tello using an 8BitDo Ultimate Bluetooth Controller via Pygame.
- Left stick: strafe (LR) & forward/back (FB)
- Right stick: yaw & up/down (UD)
- Button A: Takeoff
- Button B: Land (only if flying)
- Button X: Flip left (only if flying)
- Button Y: Flip forward (only if flying)
- Back/Select: Exit and land
"""
import sys
try:
    import pygame
except ImportError:
    print("Error: pygame module not found. Please install with `pip install pygame`.")
    sys.exit(1)
import time
from djitellopy import tello
import os

# ---------------- CONFIGURATION ----------------
AXIS_LR = 0        # Left stick horizontal
AXIS_FB = 1        # Left stick vertical
AXIS_YAW = 2       # Right stick horizontal
AXIS_UD = 3        # Right stick vertical (pushed up negative)

BUTTON_TAKEOFF      = 0  # B button (8bitdo controller dif with normal controller)
BUTTON_LAND         = 1  # A button
BUTTON_FLIP_LEFT    = 2  # Y button
BUTTON_FLIP_FORWARD = 3  # X button
BUTTON_EXIT         = 6  # Back/Select button

JOY_DEADZONE = 0.1
# -----------------------------------------------

# Initialize Pygame and joystick
def init_joystick():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick detected. Connect your 8BitDo Ultimate Controller and retry.")
        sys.exit(1)
    js = pygame.joystick.Joystick(0)
    js.init()
    print(f"Joystick initialized: {js.get_name()}")
    return js

# Scale and apply deadzone
def process_axis(val):
    return 0 if abs(val) < JOY_DEADZONE else val

# Main logic moved to run_console()

def run_console():
    joystick = init_joystick()

    # Initialize drone
    drone = tello.Tello()
    print("Connecting to Tello...")
    drone.connect()
    print(f"Battery: {drone.get_battery()}%")
    drone.streamoff()

    flying = False
    print("Controls: A=Takeoff, B=Land, X=Flip Left, Y=Flip Forward, Back=Exit.")

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    btn = event.button
                    if btn == BUTTON_TAKEOFF and not flying:
                        print("Taking off...")
                        drone.takeoff()
                        flying = True
                    elif btn == BUTTON_LAND and flying:
                        print("Landing...")
                        drone.land()
                        flying = False
                    elif btn == BUTTON_FLIP_LEFT and flying:
                        print("Flip left...")
                        drone.flip_left()
                    elif btn == BUTTON_FLIP_FORWARD and flying:
                        print("Flip forward...")
                        drone.flip_forward()
                    elif btn == BUTTON_EXIT:
                        print("Exit button pressed.")
                        running = False

            # Read axes
            lr_raw  = joystick.get_axis(AXIS_LR)
            fb_raw  = joystick.get_axis(AXIS_FB)
            yaw_raw = joystick.get_axis(AXIS_YAW)
            ud_raw  = -joystick.get_axis(AXIS_UD)  # invert

            lr  = process_axis(lr_raw)
            fb  = process_axis(fb_raw)
            yaw = process_axis(yaw_raw)
            ud  = process_axis(ud_raw)

            # Send RC control (0-100 scale)
            drone.send_rc_control(
                int(lr * 100),
                int(fb * 100),
                int(ud * 100),
                int(yaw * 100)
            )
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error:", e)

    print("Shutting down: landing and cleanup.")
    if flying:
        drone.land()
    drone.end()
    pygame.quit()
    sys.exit()

# Automatically run when imported
run_console()
