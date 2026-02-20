# src/pdf_extractor.py

from typing import List, Optional

import pdfplumber

from src.logger import logger


def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extracts text from a PDF file using pdfplumber.
    """
    logger.info(f"Extracting text from PDF: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        logger.info(f"Successfully extracted text from {pdf_path}")
        return full_text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
        return None


def extract_tables_from_pdf(pdf_path: str) -> Optional[List[List[List[str]]]]:
    """
    Extracts tables from a PDF file using pdfplumber.
    Returns a list of tables, where each table is a list of rows,
    and each row is a list of cells.
    """
    logger.info(f"Extracting tables from PDF: {pdf_path}")
    all_tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    all_tables.extend(tables)
        logger.info(f"Successfully extracted tables from {pdf_path}")
        return all_tables
    except Exception as e:
        logger.error(f"Error extracting tables from PDF {pdf_path}: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    sample_pdf_path = "data/input/sample.pdf"

    # Text extraction
    extracted_text = extract_text_from_pdf(sample_pdf_path)
    if extracted_text:
        print(f"Extracted text from {sample_pdf_path} (first 500 characters):")
        print(extracted_text[:500])

    # Table extraction
    extracted_tables = extract_tables_from_pdf(sample_pdf_path)
    if extracted_tables:
        print(f"\nExtracted tables from {sample_pdf_path}:")
        for i, table in enumerate(extracted_tables):
            print(f"Table {i + 1}: {table}")
