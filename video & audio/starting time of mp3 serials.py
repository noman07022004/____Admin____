import os
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select MP3 files", filetypes=[("MP3 files", "*.mp3")])
    return sorted(file_paths, key=lambda x: int(os.path.basename(x).split('.')[0]))

def calculate_total_length(mp3_files):
    total_length = 0
    for file in mp3_files:
        audio = AudioSegment.from_mp3(file)
        start_time = total_length
        print(f"File: {os.path.basename(file)}, Start Time: {format_time(start_time)}")
        total_length += len(audio) / 1000
    print(f"Total Length: {format_time(total_length)}")

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"

if __name__ == "__main__":
    mp3_files = select_files()
    if mp3_files:
        calculate_total_length(mp3_files)
    else:
        print("No files selected.")
