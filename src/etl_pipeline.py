# src/etl_pipeline.py

import logging
import os
from src.scraper import scrape_website
from src.pdf_extractor import extract_text_from_pdf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract():
    """
    Extract data from source.
    This could be from a website (scraping) or a local file.
    """
    logging.info("Starting EXTRACT phase...")
    extracted_data = {}

    # --- PDF Extraction ---
    sample_pdf_path = "data/input/sample.pdf"
    if os.path.exists(sample_pdf_path):
        pdf_text = extract_text_from_pdf(sample_pdf_path)
        if pdf_text:
            extracted_data['pdf_text'] = pdf_text
    else:
        logging.warning(f"PDF file not found: {sample_pdf_path}. Skipping PDF extraction.")

    # --- Web Scraping ---
    sample_url_file = "data/input/sample_url.txt"
    scraped_contents = []
    if os.path.exists(sample_url_file):
        with open(sample_url_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        if urls:
            for url in urls:
                content = scrape_website(url)
                if content:
                    scraped_contents.append({"url": url, "content": content})
        else:
            logging.info(f"No URLs found in {sample_url_file}. Skipping web scraping.")
    else:
        logging.warning(f"URL list file not found: {sample_url_file}. Skipping web scraping.")

    if scraped_contents:
        extracted_data['web_scraped_data'] = scraped_contents

    logging.info("Finished EXTRACT phase.")
    return extracted_data

def transform(data):
    """
    Transform the extracted data.
    This involves cleaning, processing, and structuring the data.
    """
    logging.info("Starting TRANSFORM phase...")
    # TODO: Implement data transformation logic
    logging.info("Finished TRANSFORM phase.")
    return None

def load(data):
    """
    Load the transformed data into a destination.
    This could be a CSV, JSON, database, etc.
    """
    logging.info("Starting LOAD phase...")
    # TODO: Implement data loading logic
    logging.info("Finished LOAD phase.")

def main():
    """

    Main function to run the ETL pipeline.
    """
    logging.info("ETL pipeline started.")
    
    # Extract
    extracted_data = extract()
    
    # Transform
    if extracted_data is not None:
        transformed_data = transform(extracted_data)
    else:
        transformed_data = None
        logging.warning("No data extracted, skipping TRANSFORM phase.")

    # Load
    if transformed_data is not None:
        load(transformed_data)
    else:
        logging.warning("No data transformed, skipping LOAD phase.")
        
    logging.info("ETL pipeline finished.")

if __name__ == "__main__":
    main()
