# 🛸 DJI Tello Face Tracking Drone (with Console Control)

This project demonstrates a computer vision-based face tracking system for the DJI Tello drone. Using Python and the Tello SDK, the drone can automatically follow a human face by adjusting its horizontal (left/right) and forward/backward movements — keeping the face centered on the screen.

The drone **does not adjust its height via code**. Instead, it uses its **built-in downward sensors** to automatically increase its altitude if something is detected below (such as a hand).

---

## 🎯 Features

- ✅ **Face Tracking**: Drone automatically adjusts its position to keep the detected human face centered.
- ✅ **Console Control**: Keyboard inputs allow for takeoff, landing, and manual movement. In this case, is using 8Bitdo controller.
- ✅ **Flight Recording**: Each tracking session is saved as a `.avi` video along with the terminal output.
- ✅ **PID Controller**: Smooth tracking response without aggressive shaking.
- 🚫 **No Hand Gesture**: Removed due to high battery consumption during flip execution.

---

## ⚙️ System Overview

### ➤ Tracking Logic
- Uses **OpenCV** and **Haar Cascade** or similar method to detect a human face.
- Applies a basic **PID controller** to calculate how far off-center the face is and send movement commands accordingly.
- Does **not** adjust altitude — manual height control is required.

### ➤ PID Control
- pid = [0.4, 0.3, 0.05]
- P (Proportional): 0.4 – Moves the drone more when the face is further off-center.
- I (Integral): 0.3 – Helps compensate for accumulated error over time.
- D (Derivative): 0.05 – Reduces overshooting and minimizes jitter.


## 📂 Project Structure

/controllers/
└── result/
├── video_YYYYMMDD_HHMMSS.avi
└── terminal_YYYYMMDD_HHMMSS.txt
main.py
README.md


All flight sessions are automatically saved in the `/controllers/result/` folder.

Each result includes:
- 🎥 The recorded video footage (`.avi`)
- 🖥️ The terminal log output (`.txt`) for debugging or analysis

---

## ⚠️ Limitations

- 🔋 **Battery Limit**: Below 14% battery, the drone may no longer respond reliably to commands. Always ensure enough charge before flying.
- 🚫 **No Auto Height Control**: The drone will not adjust its height if the face is above or below. However, you can **raise your hand underneath the drone** to trigger height increase using the built-in bottom sensors.
- 🌀 **No Face Recovery Rotation**: The drone does not rotate to search for a face if none is detected. The code for this is included but set to `0` (disabled) due to instability.

---

## 🚀 How to Use

1. Connect the DJI Tello to your PC via Wi-Fi.
2. Run `python control.py facetrack`.
3. Face tracking starts automatically once a face is detected.
4. Use keyboard commands:
   - `Ctrl + Z`: End the flight session 
---

## 🛠️ Requirements

- Python 3.7+
- `opencv-python`
- `djitellopy`
- *(Optional)* `numpy`, `keyboard`, or other helper libraries depending on your code

Install all dependencies:
```bash
pip install -r requirements.txt
```
--- 

## 🌱 Future Improvements
- Add automatic altitude control to follow faces at different vertical positions.
- Implement search-and-rotate behavior when no face is detected (currently disabled).
- Explore more robust face detection models such as Mediapipe.

## 📸 Preview

## 📄 License
- This project is for educational and experimental use only. Use at your own risk.