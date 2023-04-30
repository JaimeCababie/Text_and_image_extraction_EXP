import os
import PyPDF2
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

# Set the path for tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def pdf_to_text_images(pdf_path, output_txt_path, output_image_folder):
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)

    # Extract images from the PDF
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_image_folder, f'image_{i}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)

    # Extract text from the PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ''
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            extracted_image = Image.frombytes('RGB', (page.cropBox.getWidth(), page.cropBox.getHeight()), page._contentStream.rawdata)
            extracted_text = pytesseract.image_to_string(extracted_image)
            text += extracted_text

    # Save the text to the output txt file
    with open(output_txt_path, 'w') as txt_file:
        txt_file.write(text)

# Set the input PDF path, output txt path, and output image folder path
input_pdf_path = 'input.pdf'
output_txt_path = 'output.txt'
output_image_folder = 'output_images'

pdf_to_text_images(input_pdf_path, output_txt_path, output_image_folder)
