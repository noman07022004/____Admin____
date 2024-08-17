import os
from tkinter import Tk, filedialog
from pprint import pprint

def get_files():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(title="Select MP3 or TXT files", filetypes=[("MP3 files", "*.mp3"), ("TXT files", "*.txt")])
    return [os.path.basename(path) for path in file_paths]

def check_missing_files(files):
    # Extract file numbers and extensions
    file_dict = {}
    for file in files:
        name, ext = os.path.splitext(file)
        if name.isdigit():
            file_dict[int(name)] = ext
    
    # Find missing files in the sequence
    all_numbers = list(file_dict.keys())
    if all_numbers:
        missing_files = []
        for i in range(1, max(all_numbers) + 1):
            if i not in file_dict:
                missing_files.append(f"{i}{file_dict[all_numbers[0]]}")
        
        if missing_files:
            pprint(missing_files)
            print(f"Total missing files: {len(missing_files)}")
        else:
            print("No files are missing.")
    else:
        print("No valid numbered files found.")

if __name__ == "__main__":
    files = get_files()
    check_missing_files(files)
