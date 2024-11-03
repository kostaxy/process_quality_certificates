import os
import re
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

def extract_info_from_text(text):
    passport_number_match = re.search(r'(Паспорт качества №|Quality certificate no.)\s*([\d/]+)', text, re.IGNORECASE)
    passport_number = passport_number_match.group(2) if passport_number_match else 'unknown'
    passport_number = passport_number.replace('/', '-')
    print(passport_number)
    return passport_number

def split_pdf(input_path, output_folder):
    pages = convert_from_path(input_path)
    for page_num, page in enumerate(pages):
        image_filename = f'page_{page_num + 1}.png'
        page.save(image_filename, 'PNG')
        text = pytesseract.image_to_string(page, lang='rus+eng')
        passport_number = extract_info_from_text(text)
        output_filename = f"{passport_number}.pdf"
        output_path = os.path.join(output_folder, output_filename)
        # Если файл уже существует, добавляем порядковый номер
        counter = 1
        while os.path.exists(output_path):
            output_filename = f"{passport_number} ({counter}).pdf"
            output_path = os.path.join(output_folder, output_filename)
            counter += 1

        # Вставляем изображение в PDF
        image_page = Image.open(image_filename)
        image_page.save(output_path, 'PDF', resolution=100.0)

        os.remove(image_filename)

# имя файла
input_pdf_path = './doc21571920240913120021.pdf'
# имя папки
output_folder_path = 'new-folder'
os.makedirs(output_folder_path, exist_ok=True)
split_pdf(input_pdf_path, output_folder_path)
