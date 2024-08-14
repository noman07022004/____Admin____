import os
import moviepy.editor as mp
from tqdm import tqdm
from tkinter import Tk, filedialog


def select_files():
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
    return list(files)


def select_output_directory(initial_dir):
    Tk().withdraw()
    directory = filedialog.askdirectory(initialdir=initial_dir)
    return directory


def convert_mp3_to_mp4(mp3_files, output_dir):
    for mp3_file in tqdm(mp3_files, desc="Converting files"):
        audio = mp.AudioFileClip(mp3_file)
        duration = audio.duration

        # Create a black video clip
        video = mp.ColorClip(size=(256, 144), color=(0, 0, 0), duration=duration)
        video = video.set_fps(1)
        video = video.set_audio(audio)

        # Create output file path
        base_name = os.path.basename(mp3_file)
        output_file = os.path.join(output_dir, os.path.splitext(base_name)[0] + ".mp4")

        # Write the video file
        video.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=1)


def main():
    mp3_files = select_files()
    if not mp3_files:
        print("No files selected.")
        return

    initial_dir = os.path.dirname(mp3_files[0])
    output_dir = select_output_directory(initial_dir)
    if not output_dir:
        print("No output directory selected.")
        return

    convert_mp3_to_mp4(mp3_files, output_dir)
    print("Conversion complete.")


if __name__ == "__main__":
    main()
