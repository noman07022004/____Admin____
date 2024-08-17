import os
from tkinter import Tk, filedialog
import re

def split_text(text, max_len=35):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_len:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    lines.append(current_line.strip())
    return lines

def convert_sbv_to_srt(sbv_content):
    srt_content = []
    entries = sbv_content.strip().split("\n\n")
    
    for i, entry in enumerate(entries):
        lines = entry.split("\n")
        if len(lines) < 2:
            continue
        start_time, end_time = lines[0].split(",")
        
        start_time = start_time.strip().replace(".", ",")
        end_time = end_time.strip().replace(".", ",")
        formatted_time = f"{start_time} --> {end_time}"

        text_lines = " ".join(lines[1:])
        split_lines = split_text(text_lines)
        
        srt_content.append(f"{i + 1}")
        srt_content.append(formatted_time)
        for line in split_lines:
            srt_content.append(line)
        srt_content.append("")  # Newline after each subtitle block
    
    return "\n".join(srt_content)

def main():
    Tk().withdraw()  # Hide the root window
    sbv_files = filedialog.askopenfilenames(title="Select SBV files", filetypes=[("SBV files", "*.sbv")])
    output_dir = filedialog.askdirectory(title="Select output directory")
    
    if not sbv_files or not output_dir:
        print("No files selected or no output directory specified.")
        return
    
    for sbv_file in sbv_files:
        with open(sbv_file, 'r', encoding='utf-8') as file:
            sbv_content = file.read()
        
        srt_content = convert_sbv_to_srt(sbv_content)
        
        srt_filename = os.path.join(output_dir, os.path.basename(sbv_file).replace('.sbv', '.srt'))
        with open(srt_filename, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)
        
        print(f"Converted {os.path.basename(sbv_file)} to {os.path.basename(srt_filename)}")

if __name__ == "__main__":
    main()
