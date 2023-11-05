import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import webcam_feed as wf
import threading


cap = None
is_playing = False

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



root = tk.Tk()
root.title("Gait Analysis")
root.geometry("1280x720")

# Create a black box (Canvas) for video display
video_canvas = tk.Canvas(root, bg="black", width=1280, height=600)
video_canvas.pack(fill="x")

# Create a frame to hold video and controls
video_frame = ttk.Frame(root)
video_frame.pack(expand=True, fill="both")

# Create label for video display
label_width, label_height = 640, 480 
video_label = ttk.Label(video_frame)
video_label.pack(fill="both", expand=True)


def start_video_capture():
    global cap, is_playing
    cap = cv2.VideoCapture(0)  

    # Create a thread to display the video in the GUI
    is_playing = True
    pose_thread = threading.Thread(target=display_video)
    pose_thread.start()




def display_video():
    global cap, is_playing
    while is_playing:
        frame = wf.pose_estimation(cap)  # Get the processed frame from webcam_feed.py

        if frame is not None:
            update_video_display(frame)




def pause_video_capture():
    global is_playing
    is_playing = False



def update_video_display(frame):
    # Convert the frame to a PhotoImage
    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

    # Update the video canvas with the new frame
    video_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    video_canvas.image = photo



def take_snapshot():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            # Save the snapshot as an image file (e.g., PNG)
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, frame)


# Frame to hold buttons at the bottom
button_frame = ttk.Frame(root)
button_frame.pack(side="bottom")


# Button to start video capture and pose estimation
start_button = ttk.Button(button_frame, text="Start", command=start_video_capture)
start_button.pack(side="left", padx=10, pady=10)

# Button to stop video capture and pose estimation
pause_button = ttk.Button(button_frame, text="Pause", command=pause_video_capture)
pause_button.pack(side="left", padx=10, pady=10)

snapshot_button = ttk.Button(button_frame, text="Take Snapshot", command=take_snapshot)
snapshot_button.pack(side="left", padx=10, pady=10)

# Button to close the application
close_button = ttk.Button(button_frame, text="Close", command=root.destroy)
close_button.pack(side="left", padx=10, pady=10)


root.mainloop()