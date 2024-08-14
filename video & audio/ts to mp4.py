import os
import subprocess
from tkinter import Tk, filedialog
from tqdm import tqdm

def convert_ts_to_mp4(ts_files, output_folder):
    for ts_file in tqdm(ts_files, desc="Converting files", unit="file"):
        output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(ts_file))[0] + ".mp4")
        command = ["ffmpeg", "-i", ts_file, "-c:v", "copy", "-c:a", "copy", output_path]
        subprocess.run(command, check=True)
    print("Conversion complete.")

def select_ts_files():
    print("Now select TS files.")
    root = Tk()
    root.withdraw()  # Hide the root window
    ts_files = filedialog.askopenfilenames(title="Select TS Files", filetypes=[("TS files", "*.ts")])
    return ts_files

def select_output_folder():
    print("Now select a folder where the output files will be placed.")
    root = Tk()
    root.withdraw()  # Hide the root window
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    return output_folder

if __name__ == "__main__":
    ts_files = select_ts_files()
    if ts_files:
        output_folder = select_output_folder()
        if output_folder:
            convert_ts_to_mp4(ts_files, output_folder)
        else:
            print("No output folder selected.")
    else:
        print("No TS files selected.")
