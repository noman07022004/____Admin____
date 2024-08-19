"""
I have many txt files and their naming conventions are like 1.txt, 2.txt and 3.txt. Now create a Python script that will ask me to select the text files. After that, It will ask me to select the output folder for the files. Afterward, it will ask me how many files I want to combine at a time to convert them into one file. Show me all the instructions on the terminal. It will convert the instructed numbered files into one file, and their names will be the starting and ending numbers of their files.
"""
import os
import tkinter as tk
from tkinter import filedialog

# Function to select text files
def select_text_files():
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(title="Select text files", filetypes=[("Text files", "*.txt")])
    print("Total files : ",len(files))
    return list(files)

# Function to select output folder
def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select output folder")
    return folder

# Function to combine files
def combine_files(selected_files, output_folder, group_size):
    for i in range(0, len(selected_files), group_size):
        group = selected_files[i:i+group_size]
        if not group:
            continue
        start_num = os.path.splitext(os.path.basename(group[0]))[0]
        end_num = os.path.splitext(os.path.basename(group[-1]))[0]
        output_filename = f"{start_num}-{end_num}.txt"
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, 'w') as outfile:
            for file in group:
                with open(file, 'r') as infile:
                    outfile.write(infile.read())
                outfile.write("\n")  # Optional: Add a newline between files

# Main script
if __name__ == "__main__":
    print("Now select the text files you want to combine.")
    selected_files = select_text_files()
    
    if not selected_files:
        print("No files selected. Exiting the program.")
        exit()

    print("Now select the output folder where the combined files will be saved.")
    output_folder = select_output_folder()

    if not output_folder:
        print("No output folder selected. Exiting the program.")
        exit()

    while True:
        try:
            group_size = int(input("Enter the number of files you want to combine at a time: "))
            if group_size <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer.")

    combine_files(sorted(selected_files, key=lambda x: int(os.path.splitext(os.path.basename(x))[0])), output_folder, group_size)

    print("Files have been successfully combined and saved to the output folder.")
