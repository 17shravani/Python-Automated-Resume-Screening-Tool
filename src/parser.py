import pdfplumber
from docx import Document
from pathlib import Path
import re

class ResumeParser:
    """
    Elite Parser for extracting clean text from various resume formats.
    """
    @staticmethod
    def extract_text_from_pdf(file_path):
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return ResumeParser.clean_text(text)

    @staticmethod
    def extract_text_from_docx(file_path):
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
        return ResumeParser.clean_text(text)

    @staticmethod
    def clean_text(text):
        """
        Premium text cleaning: removes extra whitespace and non-standard characters.
        """
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        # Remove non-ascii characters (optional, but keeps it clean)
        text = text.encode("ascii", "ignore").decode()
        return text.strip()

    @staticmethod
    def parse(file_path):
        path = Path(file_path)
        if path.suffix.lower() == '.pdf':
            return ResumeParser.extract_text_from_pdf(file_path)
        elif path.suffix.lower() == '.docx':
            return ResumeParser.extract_text_from_docx(file_path)
        elif path.suffix.lower() == '.txt':
            return ResumeParser.clean_text(path.read_text(encoding='utf-8', errors='ignore'))
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

if __name__ == "__main__":
    # Test block
    print("ResumeParser initialized.")
