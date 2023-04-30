import os
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image

def extract_images(pdf_file, output_folder):
    images = convert_from_path(pdf_file)
    for i, image in enumerate(images):
        img_path = os.path.join(output_folder, f'image_{i}.png')
        image.save(img_path, 'PNG')
        print(f'Saved image {i} at {img_path}')
    return len(images)

def extract_text(pdf_file, output_folder, num_images):
    with pdfplumber.open(pdf_file) as pdf:
        output_txt = os.path.join(output_folder, 'output.txt')

        with open(output_txt, 'w', encoding='utf-8') as txt_file:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                txt_file.write(f'Page {page_num + 1}:\n{text}\n')

                for i in range(num_images):
                    if f'image_{i}.png' in text:
                        txt_file.write(f'[Image {i} is located on this page]\n')

            print(f'Text saved at {output_txt}')

def extract_pdf_content(pdf_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    num_images = extract_images(pdf_file, output_folder)
    extract_text(pdf_file, output_folder, num_images)

if __name__ == '__main__':
    pdf_file = 'input.pdf'
    output_folder = '/home/dualmono/Transforming_PDF/Nodejs_pdf_extraction/output'
    extract_pdf_content(pdf_file, output_folder)
