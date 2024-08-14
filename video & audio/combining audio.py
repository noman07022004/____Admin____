"""
 Here's the script creation process summarized in one paragraph with step-by-step prompts: Begin by prompting the user to select multiple MP3 files with the message "Please select MP3 files:". Once files are chosen, iterate through them, printing each file path alongside its index number under the header "Selected MP3 files:". Next, ask the user to select a folder for the output files using "Please select a folder where the output files will be placed:". Then, request the user to input the number of MP3 files they want to combine into each output file with the query "How many files do you want to combine?". During the file combination process, display a progress bar labeled "Combining MP3 Files" to visually indicate progress. Upon completion, notify the user with "Combining MP3 files completed. Output files are in {output_directory}", confirming the location of the combined MP3 files.
 
"""
import os
from tkinter import Tk, filedialog, simpledialog
from pydub import AudioSegment
from tqdm import tqdm
import pprint

def select_files():
    print("Please select MP3 files:")
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    files = filedialog.askopenfilenames(title="Select MP3 files", filetypes=[("MP3 Files", "*.mp3")])
    return list(files)

def select_output_directory():
    print("\nPlease select a folder where the output files will be placed:")
    Tk().withdraw()
    directory = filedialog.askdirectory(title="Select Output Directory")
    return directory

def combine_files(files, output_directory, num_files_to_combine):
    total_files = len(files)
    num_combinations = total_files // num_files_to_combine
    
    progress = tqdm(total=num_combinations, desc="Combining MP3 Files", unit="file")
    
    for i in range(0, total_files, num_files_to_combine):
        segment = files[i:i + num_files_to_combine]
        combined = AudioSegment.empty()
        start_num = os.path.basename(segment[0]).split('.')[0]
        end_num = os.path.basename(segment[-1]).split('.')[0]
        
        for file in segment:
            audio = AudioSegment.from_mp3(file)
            combined += audio
        
        combined.export(os.path.join(output_directory, f"{start_num}-{end_num}.mp3"), format="mp3")
        progress.update(1)
    
    progress.close()
    print(f"\nCombining MP3 files completed. Output files are in {output_directory}")

def main():
    print("Welcome to MP3 File Combiner!")
    
    files = select_files()
    if not files:
        print("No files selected. Exiting.")
        return
    
    print("\nSelected MP3 files:")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")
    
    output_directory = select_output_directory()
    if not output_directory:
        print("No output directory selected. Exiting.")
        return
    
    num_files_to_combine = simpledialog.askinteger("Input", "How many files do you want to combine?",
                                                   minvalue=1, maxvalue=len(files))
    if not num_files_to_combine:
        print("Invalid number. Exiting.")
        return
    
    print(f"\nSelected {len(files)} MP3 files to combine into {len(files) // num_files_to_combine} files.")
    
    combine_files(files, output_directory, num_files_to_combine)

if __name__ == "__main__":
    main()
