import tkinter as tk
from tkinter import ttk, filedialog
import cv2

def resize_video(input_video_path, output_video_path, new_width):
    # Open the input video
    input_cap = cv2.VideoCapture(input_video_path)

    # Get the original video's dimensions
    original_width = int(input_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(input_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate new height to maintain aspect ratio
    new_height = int((new_width / original_width) * original_height)

    # Define the codec and create the output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
    output_cap = cv2.VideoWriter(output_video_path, fourcc, 30, (new_width, new_height))  # 30 frames per second

    while True:
        ret, frame = input_cap.read()
        if not ret:
            break

        # Convert the frame to RGB color space (assuming BGR original color space)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize the frame
        resized_frame = cv2.resize(frame_rgb, (new_width, new_height))

        # Convert the resized frame back to BGR color space
        resized_frame_bgr = cv2.cvtColor(resized_frame, cv2.COLOR_RGB2BGR)

        # Write the resized frame to the output video
        output_cap.write(resized_frame_bgr)

    # Release the video captures and writer
    input_cap.release()
    output_cap.release()

def play_video():
    global is_playing, cap
    is_playing = True
    while is_playing:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_height, img_width, _ = frame.shape
            label_aspect_ratio = label_width / label_height
            frame_aspect_ratio = img_width / img_height
            if frame_aspect_ratio > label_aspect_ratio:
                new_width = label_width
                new_height = int(new_width / frame_aspect_ratio)
            else:
                new_height = label_height
                new_width = int(new_height * frame_aspect_ratio)
            img = cv2.resize(frame, (new_width, new_height))
            img = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
            video_label.config(image=img)
            video_label.image = img
            root.update()
            delay = int(1000 / cap.get(cv2.CAP_PROP_FPS))
            root.after(delay, lambda: None)
        else:
            # Video has reached the end, restart playback from the beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

def upload_video():
    global cap, label_width, label_height
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")])
    if video_path:
        resize_video(video_path, "resized_video.mp4", label_width)  # Resize the video
        cap = cv2.VideoCapture("resized_video.mp4")  # Open the resized video
        label_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        label_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        play_video()

def pause_video():
    global is_playing
    is_playing = False

root = tk.Tk()
root.title("Gait Analysis")

# Create a frame to hold video and controls
video_frame = ttk.Frame(root)
video_frame.grid(row=0, column=0, padx=10, pady=10)

# Create label for video display
label_width, label_height = 640, 480  # Default dimensions
video_label = ttk.Label(video_frame)
video_label.grid(row=0, column=0, columnspan=3)

# Create buttons for controls
play_button = ttk.Button(video_frame, text="Play", command=play_video)
pause_button = ttk.Button(video_frame, text="Pause", command=pause_video)
upload_button = ttk.Button(video_frame, text="Upload Video", command=upload_video)

play_button.grid(row=1, column=0, padx=5, pady=5)
pause_button.grid(row=1, column=1, padx=5, pady=5)
upload_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

cap = None
is_playing = False

root.mainloop()
