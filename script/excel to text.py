import pandas as pd
import os
from tkinter import Tk, filedialog
from tqdm import tqdm
import re
import unicodedata
from unidecode import unidecode
from pprint import pprint

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


def select_file(title="Select a file", filetypes=[("Excel files", "*.xlsx;*.xls")]):
    Tk().withdraw()  # Hides the root window
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    pprint(file_path)
    return file_path


def select_folder(title="Select a folder"):
    Tk().withdraw()  # Hides the root window
    folder_path = filedialog.askdirectory(title=title)
    pprint(folder_path)
    return folder_path


def process_line_by_line(sheet, sheet_name, output_folder):
    # Read the single column and drop empty rows
    rows = sheet.iloc[:, 0].dropna()

    for i, row in tqdm(enumerate(rows, 1), total=len(rows), desc=f"Processing rows in {sheet_name}"):
        file_name = os.path.join(output_folder, f"{i}.txt")
        with open(file_name, 'w', encoding='utf-8') as file:
            text = clean_text(str(row))
            file.write(text)


def process_sheet_by_sheet(sheet, sheet_name, output_folder):
    # Read the single column and drop empty rows
    rows = sheet.iloc[:, 0].dropna()
    file_name = os.path.join(output_folder, f"{sheet_name}.txt")

    with open(file_name, 'w', encoding='utf-8') as file:
        for row in tqdm(rows, total=len(rows), desc=f"Processing sheet: {sheet_name}"):
            text = clean_text(str(row))
            file.write(text + '\n')


def main():
    print("Please select the Excel file containing multiple sheets:")
    excel_file = select_file()

    if not excel_file:
        print("No file selected. Exiting...")
        return

    # Read the Excel file and get the sheet names
    xls = pd.ExcelFile(excel_file)
    sheet_names = xls.sheet_names

    print("Please select the output folder:")
    output_folder = select_folder()

    if not output_folder:
        print("No folder selected. Exiting...")
        return

    print("Choose processing option:")
    print("1. Line by line")
    print("2. Sheet by sheet")

    option = input("Enter 1 or 2: ")

    if option == "1":
        print("Available sheets:")
        for i, sheet_name in enumerate(sheet_names):
            print(f"{i + 1}. {sheet_name}")

        sheet_index = int(input("Select a sheet by number: ")) - 1

        if sheet_index < 0 or sheet_index >= len(sheet_names):
            print("Invalid sheet number. Exiting...")
            return

        sheet_name = sheet_names[sheet_index]
        sheet = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        process_line_by_line(sheet, sheet_name, output_folder)

    elif option == "2":
        print("Choose sub-option:")
        print("1. Process only one sheet")
        print("2. Process all sheets (each sheet as a separate file)")

        sub_option = input("Enter 1 or 2: ")

        if sub_option == "1":
            print("Available sheets:")
            for i, sheet_name in enumerate(sheet_names):
                print(f"{i + 1}. {sheet_name}")

            sheet_index = int(input("Select a sheet by number: ")) - 1

            if sheet_index < 0 or sheet_index >= len(sheet_names):
                print("Invalid sheet number. Exiting...")
                return

            sheet_name = sheet_names[sheet_index]
            sheet = pd.read_excel(
                excel_file, sheet_name=sheet_name, header=None)
            process_sheet_by_sheet(sheet, sheet_name, output_folder)

        elif sub_option == "2":
            for sheet_name in sheet_names:
                print(f"Processing sheet: {sheet_name}")
                sheet = pd.read_excel(
                    excel_file, sheet_name=sheet_name, header=None)
                process_sheet_by_sheet(sheet, sheet_name, output_folder)

        else:
            print("Invalid sub-option selected. Exiting...")
            return

    else:
        print("Invalid option selected. Exiting...")
        return

    print("Processing completed.")


if __name__ == "__main__":
    main()
