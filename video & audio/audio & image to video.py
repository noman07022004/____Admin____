import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import *
from pprint import pprint


width = 1920
height = 1080


# Function to get mp3 and jpeg files from user
def select_files(title, file_types):
    pprint("Select files for the video")
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(title=title, filetypes=file_types)
    if not files:
        messagebox.showerror("Error", f"No {file_types[0][0]} files selected. Please select files to proceed.")
        exit()  # Exit if no files are selected
    pprint(files)
    return list(files)  # Convert tuple to list

# Function to get output file name from user
def get_output_name():
    root = tk.Tk()
    root.withdraw()
    output_name = filedialog.asksaveasfilename(title="Save As", defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not output_name:
        messagebox.showerror("Error", "No output file name provided. Please specify an output file name to proceed.")
        exit()  # Exit if no output name is given
    return output_name

# Select mp3 files
mp3_files = select_files("Select MP3 Files", [("MP3 files", "*.mp3")])

# Select jpeg files
jpeg_files = select_files("Select JPEG Files", [("JPEG files", "*.jpeg"), ("JPG files", "*.jpg")])

# Ask for output file name
output_path = get_output_name()

# Sorting files based on numeric prefix
try:
    mp3_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    jpeg_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
except ValueError as e:
    messagebox.showerror("Error", f"File names must be numeric. {e}")
    exit()

# Checking if corresponding mp3 and jpeg files match
for mp3, jpeg in zip(mp3_files, jpeg_files):
    mp3_name = os.path.splitext(os.path.basename(mp3))[0]
    jpeg_name = os.path.splitext(os.path.basename(jpeg))[0]
    if mp3_name != jpeg_name:
        messagebox.showerror("Error", f"MP3 file {mp3_name}.mp3 does not match JPEG file {jpeg_name}.jpeg.")
        exit()

# Function to resize image while preserving aspect ratio to fit within frame
def resize_image_to_fit(image_clip, frame_size):
    img_width, img_height = image_clip.size
    frame_width, frame_height = frame_size
    
    # Calculate scaling factors to fit image within frame
    width_ratio = frame_width / img_width
    height_ratio = frame_height / img_height
    
    # Determine the limiting dimension based on aspect ratio
    if width_ratio < height_ratio:
        # Fit horizontally
        new_width = frame_width
        new_height = int(img_height * width_ratio)
    else:
        # Fit vertically
        new_width = int(img_width * height_ratio)
        new_height = frame_height
        
    # Resize image while preserving aspect ratio
    resized_clip = image_clip.resize((new_width, new_height))
    
    # Calculate new position to center the image within frame
    x_pos = (frame_width - resized_clip.w) / 2
    y_pos = (frame_height - resized_clip.h) / 2
    
    return resized_clip.set_position((x_pos, y_pos))

# Create video
video_clips = []
for mp3, jpeg in zip(mp3_files, jpeg_files):
    mp3_clip = AudioFileClip(mp3)
    jpeg_clip = ImageClip(jpeg)
    
    # Resize image to fit within frame (1080p height, preserving aspect ratio)
    resized_clip = resize_image_to_fit(jpeg_clip, (width, height))  # 1080p frame size with 9:16 aspect ratio

    # Calculate duration based on audio clip duration
    duration = mp3_clip.duration

    # Create a black background video clip
    background_clip = ColorClip(size=(width, height), color=(0, 0, 0), duration=duration)  # 1080p frame size

    # Overlay resized image on the black background
    video_clip = CompositeVideoClip([
        background_clip,
        resized_clip.set_duration(duration)
    ])

    # Add audio
    video_clip = video_clip.set_audio(mp3_clip)

    video_clips.append(video_clip)

# Concatenate all video clips
final_clip = concatenate_videoclips(video_clips, method="compose")

# Provide progress feedback during video processing
print("Processing video, please wait...")

# Write the final video to file with enhanced quality settings and optimized threading
try:
    final_clip.write_videofile(
        output_path,
        fps=6,  # Adjusting FPS to 6 for static image video
        codec='libx264',
        bitrate='2000k',  # Higher bitrate for better quality
        audio_codec='aac',
        preset='slower',  # Better quality with slower processing
        threads=4,  # Optimize for 4-core CPU
        ffmpeg_params=[
            '-profile:v', 'high',
            '-level:v', '4.0',
            '-crf', '18'  # Lower CRF for higher quality
        ]
    )
    print(f"Video successfully created and saved at {output_path}")
except Exception as e:
    messagebox.showerror("Error", f"An error occurred during video processing: {e}")
    exit()
