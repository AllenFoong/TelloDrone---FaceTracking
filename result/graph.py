import pandas as pd
import matplotlib.pyplot as plt
import re

# --- Load the text log file ---
file_path = "flight_1_result.txt"  # Change this path if needed
with open(file_path, "r") as file:
    lines = file.readlines()

# --- Extract relevant data using regex ---
data = []
pattern = re.compile(r"Speed (-?\d+)\s+Forward Backward (-?\d+)\s+Center \[(\d+), (\d+)\]\s+Area (\d+)")

for line in lines:
    match = pattern.search(line)
    if match:
        speed = int(match.group(1))
        fb = int(match.group(2))
        center_x = int(match.group(3))
        center_y = int(match.group(4))
        area = int(match.group(5))
        data.append((speed, fb, center_x, center_y, area))

# --- Convert to a DataFrame ---
df = pd.DataFrame(data, columns=["Speed", "Forward/Backward", "Center_X", "Center_Y", "Area"])

# --- Plot graphs ---

plt.figure(figsize=(12, 6))

# Plot Face Center X over Time
plt.subplot(2, 1, 1)
plt.plot(df["Center_X"], label="Face X-Position")
plt.axhline(df["Center_X"].mean(), color='r', linestyle='--', label="Mean X-Position")
plt.ylabel("X Position")
plt.title("Face X Position Over Time")
plt.legend()

# Plot Face Area over Time
plt.subplot(2, 1, 2)
plt.plot(df["Area"], label="Face Area")
plt.axhline(df["Area"].mean(), color='g', linestyle='--', label="Mean Face Area")
plt.ylabel("Area")
plt.title("Face Area Over Time")
plt.legend()

plt.tight_layout()
plt.show()
