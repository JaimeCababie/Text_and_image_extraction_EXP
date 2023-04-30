import os
import re
import docx2txt

def remove_unnecessary_spaces(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    text = '\n'.join(lines)
    return text

def extract_images(docx_file, output_folder):
    images = docx2txt.process(docx_file, output_folder)
    text = images.replace("<[Image]:", "\n\n[Image:")
    return text, images

def add_image_references(text, output_folder):
    images = os.listdir(output_folder)
    for i, image in enumerate(images, start=1):
        image_path = os.path.abspath(os.path.join(output_folder, image))
        reference_note = f'[Image {i}: {image_path}]'
        text = text.replace(f'[Image: {image}]', reference_note)
    return text

def main(docx_file, output_folder, txt_file):
    os.makedirs(output_folder, exist_ok=True)
    
    text, images = extract_images(docx_file, output_folder)
    text_with_references = add_image_references(text, output_folder)
    cleaned_text = remove_unnecessary_spaces(text_with_references)
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

if __name__ == '__main__':
    docx_file = 'input.docx'
    output_folder = 'images'
    txt_file = 'output.txt'
    
    main(docx_file, output_folder, txt_file)
