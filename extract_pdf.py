import os
import fitz
import pdfplumber
from PIL import Image

def extract_images(pdf_file, output_folder):
    doc = fitz.open(pdf_file)
    image_count = 0

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]

            img_path = os.path.join(output_folder, f'image_{image_count}.png')
            with open(img_path, 'wb') as img_file:
                img_file.write(image_data)
                print(f'Saved image {image_count} at {img_path}')
                image_count += 1

    return image_count

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
