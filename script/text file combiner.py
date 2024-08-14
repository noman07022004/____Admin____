"""
I have many txt files and their naming conventions are like 1.txt, 2.txt and 3.txt. Now create a Python script that will ask me to select the text files. After that, It will ask me to select the output folder for the files. Afterward, it will ask me how many files I want to combine at a time to convert them into one file. Show me all the instructions on the terminal. It will convert the instructed numbered files into one file, and their names will be the starting and ending numbers of their files. Show me the progress in the terminal and also use pprint

"""
import os
from tkinter import Tk, filedialog
from pprint import pprint
from tqdm import tqdm

def select_txt_files():
    Tk().withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(
        title="Please select txt files:",
        filetypes=[("Text files", "*.txt")]
    )
    return file_paths

def select_output_folder():
    Tk().withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(
        title="Please select a folder where the output files will be placed:"
    )
    return folder_path

def combine_files(file_paths, output_folder, files_per_combination):
    for i in range(0, len(file_paths), files_per_combination):
        combined_files = file_paths[i:i + files_per_combination]
        if not combined_files:
            continue
        
        start_num = os.path.basename(combined_files[0]).split('.')[0]
        end_num = os.path.basename(combined_files[-1]).split('.')[0]
        output_file_path = os.path.join(output_folder, f"{start_num}-{end_num}.txt")
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for file_path in combined_files:
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    output_file.write(input_file.read())
                    output_file.write('\n')
        
        print(f"Created: {output_file_path}")

def main():
    print("Please select txt files:")
    txt_files = select_txt_files()
    if not txt_files:
        print("No files selected. Exiting...")
        return

    print("\nSelected txt files:")
    pprint(txt_files)

    print("\nPlease select a folder where the output files will be placed:")
    output_folder = select_output_folder()
    if not output_folder:
        print("No folder selected. Exiting...")
        return

    files_per_combination = int(input("\nHow many files do you want to combine? "))

    print("\nCombining txt Files:")
    for _ in tqdm(range(0, len(txt_files), files_per_combination)):
        combine_files(txt_files, output_folder, files_per_combination)

    print(f"\nCombining txt files completed. Output files are in {output_folder}")

if __name__ == "__main__":
    main()
