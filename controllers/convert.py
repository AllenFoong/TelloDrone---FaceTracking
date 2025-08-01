from moviepy.editor import VideoFileClip

# Load the video
clip = VideoFileClip("D:/1. Agent Design - drone/to upload/controllers/result/flight_2.avi")

# Save as MP4
clip.write_videofile("D:/1. Agent Design - drone/to upload/controllers/result/flight_2.mp4", codec="libx264")
