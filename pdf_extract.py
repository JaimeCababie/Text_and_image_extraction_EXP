import os
import fitz

def remove_unnecessary_spaces(text):
    lines = text.split('\n')
    lines = [line.strip() for line in lines]

    combined_lines = []
    for line in lines:
        if not line:
            continue
        if combined_lines and not combined_lines[-1][-1] in {'.', ':', ';', '(', ')', '[', ']', ',', '?', '!'}:
            combined_lines[-1] += ' ' + line
        else:
            combined_lines.append(line)

    text = '\n'.join(combined_lines)
    return text

def extract_images(pdf_file, output_folder):
    doc = fitz.open(pdf_file)
    img_dir = output_folder
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    img_refs = []
    processed_images = set()

    for page_num in range(doc.page_count):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            if xref in processed_images:
                continue
            processed_images.add(xref)
            base_image = doc.extract_image(xref)
            img_path = os.path.join(img_dir, f"image{page_num}_{img_index}.{base_image['ext']}")
            with open(img_path, "wb") as f:
                f.write(base_image["image"])
            img_refs.append((page_num, img_index, img_path))

    return img_refs

def extract_text(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def add_image_references(text, img_refs):
    lines = text.split('\n')
    img_ref_idx = 0
    new_lines = []

    for line in lines:
        new_lines.append(line)
        if img_ref_idx < len(img_refs) and img_refs[img_ref_idx][0] == len(new_lines):
            reference_note = f"[Image (Page {img_refs[img_ref_idx][0]}, Image {img_refs[img_ref_idx][1]}): {img_refs[img_ref_idx][2]}]"
            new_lines.append(reference_note)
            img_ref_idx += 1

    return '\n'.join(new_lines)

def main(pdf_file, output_folder, txt_file):
    img_refs = extract_images(pdf_file, output_folder)
    extracted_text = extract_text(pdf_file)
    text_without_spaces = remove_unnecessary_spaces(extracted_text)
    text_with_references = add_image_references(text_without_spaces, img_refs)
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text_with_references)

if __name__ == '__main__':
    pdf_file = 'input2.pdf'
    output_folder = 'images'
    txt_file = 'output.txt'
    
    main(pdf_file, output_folder, txt_file)
