# src/pdf_extractor.py

import logging
import pdfplumber

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    logging.info(f"Extracting text from PDF: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
        logging.info(f"Successfully extracted text from {pdf_path}")
        return full_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF {pdf_path}: {e}")
        return None

def extract_tables_from_pdf(pdf_path):
    """
    Extracts tables from a PDF file using pdfplumber.
    """
    logging.info(f"Extracting tables from PDF: {pdf_path}")
    all_tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    all_tables.extend(tables)
        logging.info(f"Successfully extracted tables from {pdf_path}")
        return all_tables
    except Exception as e:
        logging.error(f"Error extracting tables from PDF {pdf_path}: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    # Ensure you have a sample.pdf in the data/input directory
    sample_pdf_path = "data/input/sample.pdf" 
    
    # Text extraction
    extracted_text = extract_text_from_pdf(sample_pdf_path)
    if extracted_text:
        print(f"""Extracted text from {sample_pdf_path}:
{extracted_text[:500]}...""")

    # Table extraction
    extracted_tables = extract_tables_from_pdf(sample_pdf_path)
    if extracted_tables:
        print(f"""
Extracted tables from {sample_pdf_path}:""")
        for i, table in enumerate(extracted_tables):
            print(f"Table {i+1}: {table}")
