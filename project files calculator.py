import os
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import math

# Utility function to convert bytes to human-readable format
# ANSI escape sequences for text colors


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def convert_bytes(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

# Utility function to convert seconds to hours and minutes


def convert_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours} hours {minutes} minutes"


def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_folder(folder_path)


def select_files():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        process_files(file_paths)


def process_folder(folder_path):
    txt_files_count = 0
    txt_total_chars = 0
    txt_total_words = 0

    jpeg_files_count = 0
    jpeg_total_size = 0

    mp3_files_count = 0
    mp3_total_length = 0
    mp3_total_size = 0

    mp4_files_count = 0
    mp4_total_length = 0
    mp4_total_size = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.txt'):
                txt_files_count += 1
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    txt_total_chars += len(content)
                    txt_total_words += len(content.split())

            elif file.lower().endswith('.jpeg') or file.lower().endswith('.jpg'):
                jpeg_files_count += 1
                jpeg_total_size += os.path.getsize(file_path)

            elif file.lower().endswith('.mp3'):
                mp3_files_count += 1
                audio = MP3(file_path)
                mp3_total_length += audio.info.length
                mp3_total_size += os.path.getsize(file_path)

            elif file.lower().endswith('.mp4'):
                mp4_files_count += 1
                video = MP4(file_path)
                mp4_total_length += video.info.length
                mp4_total_size += os.path.getsize(file_path)

    # Print results only if there are files of that type
    print(Color.RED+"===================================="+Color.END)
    if txt_files_count > 0:
        print(f"{Color.CYAN}.txt:-{Color.END}")
        print(f"  Total {Color.YELLOW}.txt files: {Color.GREEN}{txt_files_count}{Color.END}")
        print(f"  Total {Color.YELLOW}characters: {Color.GREEN}{txt_total_chars}{Color.END}")
        print(f"  Total {Color.YELLOW}words: {Color.GREEN}{txt_total_words}{Color.END}")
        print("")

    if jpeg_files_count > 0:
        print(f"{Color.CYAN}.jpeg:-{Color.END}")
        print(f"  Total{Color.YELLOW} .jpeg/.jpg files:{Color.GREEN} {jpeg_files_count}{Color.END}")
        print(f"  Total{Color.YELLOW} size:{Color.GREEN} {convert_bytes(jpeg_total_size)}{Color.END}")
        print("")

    if mp3_files_count > 0:
        print(f"{Color.CYAN}.mp3:-{Color.END}")
        print(f"  Total {Color.YELLOW}.mp3 files:{Color.GREEN} {mp3_files_count}{Color.END}")
        print(f"  Total {Color.YELLOW}length:{Color.GREEN} {convert_seconds(mp3_total_length)}{Color.END}")
        print(f"  Total {Color.YELLOW}size:{Color.GREEN} {convert_bytes(mp3_total_size)}{Color.END}")
        print("")

    if mp4_files_count > 0:
        print(f"{Color.CYAN}.mp4:-{Color.END}")
        print(f"  Total {Color.YELLOW}.mp4 files:{Color.GREEN} {mp4_files_count}{Color.END}")
        print(f"  Total {Color.YELLOW}length:{Color.GREEN} {convert_seconds(mp4_total_length)}{Color.END}")
        print(f"  Total {Color.YELLOW}size:{Color.GREEN} {convert_bytes(mp4_total_size)}{Color.END}")
        print("")
    print(Color.RED+"===================================="+Color.END)


def process_files(file_paths):
    txt_files_count = 0
    txt_total_chars = 0
    txt_total_words = 0

    jpeg_files_count = 0
    jpeg_total_size = 0

    mp3_files_count = 0
    mp3_total_length = 0
    mp3_total_size = 0

    mp4_files_count = 0
    mp4_total_length = 0
    mp4_total_size = 0

    for file_path in file_paths:
        if os.path.isfile(file_path):
            if file_path.lower().endswith('.txt'):
                txt_files_count += 1
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    txt_total_chars += len(content)
                    txt_total_words += len(content.split())

            elif file_path.lower().endswith('.jpeg') or file_path.lower().endswith('.jpg'):
                jpeg_files_count += 1
                jpeg_total_size += os.path.getsize(file_path)

            elif file_path.lower().endswith('.mp3'):
                mp3_files_count += 1
                audio = MP3(file_path)
                mp3_total_length += audio.info.length
                mp3_total_size += os.path.getsize(file_path)

            elif file_path.lower().endswith('.mp4'):
                mp4_files_count += 1
                video = MP4(file_path)
                mp4_total_length += video.info.length
                mp4_total_size += os.path.getsize(file_path)

    # Print results only if there are files of that type

    print(Color.RED+"===================================="+Color.END)
    if txt_files_count > 0:
        print(f"{Color.CYAN}.txt:-{Color.END}")
        print(f"  Total {Color.YELLOW}.txt files: {Color.GREEN}{txt_files_count}{Color.END}")
        print(f"  Total {Color.YELLOW}characters: {Color.GREEN}{txt_total_chars}{Color.END}")
        print(f"  Total {Color.YELLOW}words: {Color.GREEN}{txt_total_words}{Color.END}")
        print("")

    if jpeg_files_count > 0:
        print(f"{Color.CYAN}.jpeg:-{Color.END}")
        print(f"  Total{Color.YELLOW} .jpeg/.jpg files:{Color.GREEN} {jpeg_files_count}{Color.END}")
        print(f"  Total{Color.YELLOW} size:{Color.GREEN} {convert_bytes(jpeg_total_size)}{Color.END}")
        print("")

    if mp3_files_count > 0:
        print(f"{Color.CYAN}.mp3:-{Color.END}")
        print(f"  Total {Color.YELLOW}.mp3 files:{Color.GREEN} {mp3_files_count}{Color.END}")
        print(f"  Total {Color.YELLOW}length:{Color.GREEN} {convert_seconds(mp3_total_length)}{Color.END}")
        print(f"  Total {Color.YELLOW}size:{Color.GREEN} {convert_bytes(mp3_total_size)}{Color.END}")
        print("")

    if mp4_files_count > 0:
        print(f"{Color.CYAN}.mp4:-{Color.END}")
        print(f"  Total {Color.YELLOW}.mp4 files:{Color.GREEN} {mp4_files_count}{Color.END}")
        print(f"  Total {Color.YELLOW}length:{Color.GREEN} {convert_seconds(mp4_total_length)}{Color.END}")
        print(f"  Total {Color.YELLOW}size:{Color.GREEN} {convert_bytes(mp4_total_size)}{Color.END}")
        print("")
    print(Color.RED+"===================================="+Color.END)


# GUI setup
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    y -= math.floor(0.2 * screen_height)  # Adjusting y by 20% above the center

    root.geometry(f'{width}x{height}+{x}+{y}')


root = tk.Tk()
root.title("File Statistics")

window_width = 400
window_height = 150
center_window(root, window_width, window_height)

folder_button = tk.Button(root, text="Select Folder", command=select_folder)
folder_button.pack(pady=20)

files_button = tk.Button(root, text="Select Files", command=select_files)
files_button.pack()

root.mainloop()
