import os
import re
import unicodedata
import tkinter as tk
from tkinter import filedialog
from unidecode import unidecode


def select_files():
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(
        title="Select TXT files", filetypes=[("Text files", "*.txt")])
    return files


def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    output_folder = filedialog.askdirectory(title="Select output folder")
    return output_folder


def clean_text(text):
    # Normalize the text to NFD (Normalization Form D)
    text = unicodedata.normalize('NFD', text)
    # Remove diacritics
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # Transliterate non-ASCII characters to their ASCII equivalents
    text = unidecode(text)
    # Remove remaining non-ASCII characters, except for specific punctuation and line breaks
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    # removing link
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
    text = re.sub(url_pattern, '', text)
    # # Add line breaks after commas, periods, semicolons, and exclamation marks (excluding numbers)
    text = re.sub(r'(?<=\D)[.] ', '.\n', text)
    text = re.sub(r'(?<=\D)[,;] ', ',\n', text)
    text = re.sub(r'(?<=\D)[!] ', '!\n', text)
    text = re.sub(r'(?<=\D)[?] ', '?\n', text)
    text = re.sub(r'(?<=\D)["] ', '"\n', text)
    text = re.sub(r'(\d+)/(\d+)', r'\1 out of \2', text)

    text = re.sub(r'[<>]', '', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\b([a-zA-Z]+)\d+\b', r'\1', text)
    return text


def process_file(input_file, output_folder):
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()
        cleaned_content = clean_text(content)
        output_file = os.path.join(output_folder, os.path.basename(input_file))
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(cleaned_content)


if __name__ == "__main__":
    input_files = select_files()
    output_folder = select_output_folder()

    if not input_files or not output_folder:
        print("No files selected or output folder not specified.")
    else:
        for file in input_files:
            process_file(file, output_folder)
        print(f"Processed {len(input_files)
                           } files. Cleaned files saved in {output_folder}")
