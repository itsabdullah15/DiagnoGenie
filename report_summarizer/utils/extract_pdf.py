import fitz 
import os
from io import BytesIO

def extract_text_from_pdf(file_path) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_txt(file_obj) -> str:
    return file_obj.read().decode('utf-8').strip()

def extract_data_from_medical_report(file_obj, filename: str) -> str:
    ext = os.path.splitext(filename)[-1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_obj)
    elif ext == ".txt":
        return extract_text_from_txt(file_obj)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
