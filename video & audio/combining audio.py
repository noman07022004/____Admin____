"""
I have many mp3 files and their naming conventions are like 1.mp3, 2.mp3 and 3.mp3. Now create a Python script that will ask me to select the mp3 files. After that, It will ask me to select the output folder for the files. Afterward, it will ask me how many files I want to combine at a time to convert them into one file. Show me all the instructions on the terminal. It will convert the instructed numbered files into one file, and their names will be the starting-ending numbers of their files. you must have to show me the progress bar in terminal using tqdm

"""
import os
from tkinter import Tk, filedialog
from pydub import AudioSegment
from tqdm import tqdm

def select_files():
    root = Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(title="Select MP3 files", filetypes=[("MP3 files", "*.mp3")])
    return list(files)

def select_output_folder():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Output Folder")
    return folder

def combine_mp3_files(files, output_folder, group_size):
    total_files = len(files)
    num_combinations = (total_files + group_size - 1) // group_size  # Calculate the number of combinations

    with tqdm(total=num_combinations, desc="Combining Files") as pbar:
        for i in range(0, total_files, group_size):
            chunk = files[i:i + group_size]
            combined = AudioSegment.empty()
            
            for file in chunk:
                audio = AudioSegment.from_mp3(file)
                combined += audio

            start_num = os.path.basename(chunk[0]).split('.')[0]
            end_num = os.path.basename(chunk[-1]).split('.')[0]
            output_filename = os.path.join(output_folder, f"{start_num}-{end_num}.mp3")
            
            combined.export(output_filename, format="mp3")
            #print(f"Combined {start_num}.mp3 to {end_num}.mp3 into {output_filename}")
            
            pbar.update(1)  # Update the progress bar after each combination

    print("All files have been combined.")

def main():
    print("Now select MP3 files...")
    files = select_files()
    if not files:
        print("No files selected. Exiting...")
        return
    
    print("Now select a folder where the output files will be placed...")
    output_folder = select_output_folder()
    if not output_folder:
        print("No output folder selected. Exiting...")
        return
    
    group_size = int(input("Enter the number of files to combine at a time: "))
    
    print(f"Combining {group_size} files at a time...")
    combine_mp3_files(files, output_folder, group_size)

if __name__ == "__main__":
    main()
