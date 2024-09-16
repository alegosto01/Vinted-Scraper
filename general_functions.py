from openpyxl import load_workbook
import os


def empty_excel(path):
    wb = load_workbook(path)
    ws = wb['Sheet1']  # Change 'Sheet1' to your specific sheet name

    # Loop through all rows and columns to clear content
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.value = None

    # Save the workbook
    wb.save(path)


    
def remove_illegal_characters(value):
    """Removes illegal characters that Excel does not support."""
    ILLEGAL_CHARACTERS = [chr(i) for i in range(32) if i not in (9, 10, 13)] + [chr(127)]
    for char in ILLEGAL_CHARACTERS:
        value = value.replace(char, "")
    return value


def ensure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)  # Create directories if they don't exist


def get_last_non_empty_row_excel(file_path):
    wb = load_workbook(file_path)
    ws = wb['Sheet1']  # Change 'Sheet1' to your sheet name
    for row in range(ws.max_row, 0, -1):
        if any(cell.value is not None for cell in ws[row]):
            return row
    return 0  # If all rows are empty