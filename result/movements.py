import re
import pandas as pd
import matplotlib.pyplot as plt

def parse_rc_logs(logpath):
    """
    Parses lines like:
      [INFO] ... Send command (no response expected): 'rc LR FB UD YW'
    and returns a DataFrame with columns ['LeftRight','ForwardBack','UpDown','Yaw'].
    """
    pattern = re.compile(r"rc\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)")
    data = []
    with open(logpath, "r") as f:
        for line in f:
            m = pattern.search(line)
            if m:
                lr, fb, ud, yw = map(int, m.groups())
                data.append((lr, fb, ud, yw))
    return pd.DataFrame(data, columns=["LeftRight", "ForwardBack", "UpDown", "Yaw"])

def plot_movements(df):
    """
    Plots four subplots for Left/Right, Forward/Backward, Up/Down, and Yaw (rotation).
    """
    plt.figure(figsize=(12, 10))

    # Left/Right
    plt.subplot(4,1,1)
    plt.plot(df["LeftRight"], label="Left/Right", linewidth=1)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title("Drone Left/Right Movement Over Time")
    plt.ylabel("Speed")
    plt.legend()

    # Forward/Backward
    plt.subplot(4,1,2)
    plt.plot(df["ForwardBack"], label="Forward/Backward", color="green", linewidth=1)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title("Drone Forward/Backward Movement Over Time")
    plt.ylabel("Speed")
    plt.legend()

    # Up/Down
    plt.subplot(4,1,3)
    plt.plot(df["UpDown"], label="Up/Down", color="purple", linewidth=1)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title("Drone Up/Down Movement Over Time")
    plt.ylabel("Speed")
    plt.legend()

    # Yaw (Rotation)
    plt.subplot(4,1,4)
    plt.plot(df["Yaw"], label="Yaw (Rotation)", color="orange", linewidth=1)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title("Drone Yaw (Rotation) Over Time")
    plt.ylabel("Rotational Speed")
    plt.xlabel("Frame Index")
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    log_file = "flight_2_result.txt"
    df = parse_rc_logs(log_file)
    if df.empty:
        print(f"No RC commands found in {log_file}.")
        return
    plot_movements(df)

if __name__ == "__main__":
    main()
