import sys
import os
import re
import datetime

# --- Ensure 'result' directory exists ---
base_dir = os.path.join(os.path.dirname(__file__), 'result')
os.makedirs(base_dir, exist_ok=True)

# --- Auto‑incrementing base filename for both log and video ---
existing = os.listdir(base_dir)
nums = []
for fname in existing:
    m = re.match(r'flight_(\d+)_\d{8}_\d{6}\.txt$', fname)
    if m:
        nums.append(int(m.group(1)))
next_num = max(nums) + 1 if nums else 1

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
base_name = f"flight_{next_num}_{timestamp}"

# --- Paths for log and video ---
log_path   = os.path.join(base_dir, f"{base_name}.txt")
video_path = os.path.join(base_dir, f"{base_name}.avi")

# --- Setup logging to file and console ---
log_file = open(log_path, 'a')
class Tee:
    def __init__(self, *streams):
        self.streams = streams
    def write(self, data):
        for s in self.streams:
            s.write(data)
    def flush(self):
        for s in self.streams:
            s.flush()

sys.stdout = Tee(sys.stdout, log_file)
sys.stderr = Tee(sys.stderr, log_file)

import cv2
import numpy as np
from djitellopy import tello
import time

width, height = 640, 480
fb_range = [10000, 20000]

#pid = [0.4, 0.3, 0.05]
#pid = [0.5, 0.1, 0.05]
# pid = [0.5, 0.1, 0.1]

pid = [0.4, 0.3, 0.05]
p_error = 0

# --- Brightness/contrast adjustment helper ---
def adjust_brightness_contrast(img, alpha=1.3, beta=20):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

# --- Setup for saving video ---
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_out = cv2.VideoWriter(video_path, fourcc, 20.0, (width, height))

def find_face(img_capture):
    xml_path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), '..',
        'resources', 'haarcascades',
        'haarcascade_frontalface_default.xml'
    ))
    face_cascade = cv2.CascadeClassifier(xml_path)

    img_gray = cv2.cvtColor(img_capture, cv2.COLOR_BGR2GRAY)

    # ← modified parameters for closer detection
    faces = face_cascade.detectMultiScale(
        img_gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(50, 50)
    )
    

    face_center_list, face_area_list = [], []
    for (x, y, w, h) in faces:
        center_x, center_y = x + w//2, y + h//2
        face_center_list.append([center_x, center_y])
        face_area_list.append(w*h)
        cv2.rectangle(img_capture, (x, y), (x+w, y+h), (0,0,255), 2)
        cv2.circle(img_capture, (center_x, center_y), 2, (0,255,0), cv2.FILLED)

    if face_area_list:
        i = face_area_list.index(max(face_area_list))
        return img_capture, [face_center_list[i], face_area_list[i]]
    return img_capture, [[0, 0], 0]

def track_face(face_stats, p_error):
    area = face_stats[1]    
    x, y = face_stats[0]

    # if area == 0:
    #     # No face detected → spin in place (yaw = 30°/s)
    #     drone.send_rc_control(0, 0, 0, 30)
    #     return p_error
    
    forward_backward = 0
    distanceFromCenter = x - width//2

    speed = pid[0]*distanceFromCenter + pid[1]*(distanceFromCenter - p_error)
    speed = int(np.clip(speed, -100, 100))

    if fb_range[0] < area < fb_range[1]:
        forward_backward = 0
    elif area > fb_range[1]:
        forward_backward = -40
    elif area < fb_range[0] and area != 0:
        forward_backward = 40

    if x == 0:
        speed = 0
        distanceFromCenter = 0

    # print("Speed", speed,
    #       "Forward Backward", forward_backward,
    #       "Center", face_stats[0],
    #       "Area", area)

    drone.send_rc_control(0, forward_backward, 0, speed)
    return distanceFromCenter

# --- Drone setup and main loop ---
time.sleep(4)
drone = tello.Tello()
drone.connect()
print("Battery:", drone.get_battery(), "%")

drone.streamon()
drone.takeoff()
drone.send_rc_control(0, 0, 0, 0)
drone.send_rc_control(0, 0, 35, 0)
time.sleep(2.1)

# cancel residual climb so it hovers
drone.send_rc_control(0, 0, 0, 0)

try:
    while True:
        frame = drone.get_frame_read().frame
        frame = cv2.resize(frame, (width, height))

        # enhance brightness/contrast if needed
        frame = adjust_brightness_contrast(frame)

        img_face, face_stats = find_face(frame)
        p_error = track_face(face_stats, p_error)

        video_out.write(img_face)

        cv2.imshow("Tello Drone Footage", img_face)
        cv2.waitKey(1)

except:
    print('Ending...')
    drone.end()
    video_out.release()
    cv2.destroyAllWindows()
    print('Shutting down...')
    log_file.close()
    sys.exit()