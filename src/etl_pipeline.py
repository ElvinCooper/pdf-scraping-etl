# src/etl_pipeline.py

import logging
import os
import re
import pandas as pd
from src.scraper import scrape_website
from src.pdf_extractor import extract_text_from_pdf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text):
    """
    Cleans text by removing extra whitespace and standardizing newlines.
    """
    if text is None:
        return None
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = text.strip()  # Remove leading/trailing whitespace
    return text

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
    transformed_data = {}

    # --- Transform PDF text ---
    if 'pdf_text' in data and data['pdf_text']:
        transformed_data['cleaned_pdf_text'] = clean_text(data['pdf_text'])
    else:
        logging.warning("No PDF text found for transformation.")

    # --- Transform Web Scraped Data ---
    if 'web_scraped_data' in data and data['web_scraped_data']:
        cleaned_web_data = []
        for item in data['web_scraped_data']:
            cleaned_content = clean_text(item.get('content'))
            if cleaned_content:
                cleaned_web_data.append({
                    "url": item.get('url'),
                    "cleaned_content": cleaned_content
                })
        if cleaned_web_data:
            transformed_data['web_data_dataframe'] = pd.DataFrame(cleaned_web_data)
        else:
            logging.warning("No web scraped data found after cleaning.")
    else:
        logging.warning("No web scraped data found for transformation.")

    logging.info("Finished TRANSFORM phase.")
    return transformed_data

def load(data):
    """
    Load the transformed data into a destination.
    This could be a CSV, JSON, database, etc.
    """
    logging.info("Starting LOAD phase...")
    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

    # --- Load Cleaned PDF Text ---
    if 'cleaned_pdf_text' in data and data['cleaned_pdf_text']:
        output_path = os.path.join(output_dir, "extracted_text.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(data['cleaned_pdf_text'])
        logging.info(f"Cleaned PDF text loaded to: {output_path}")
    else:
        logging.warning("No cleaned PDF text found for loading.")

    # --- Load Web Data DataFrame ---
    if 'web_data_dataframe' in data and not data['web_data_dataframe'].empty:
        output_path = os.path.join(output_dir, "cleaned_data.csv")
        data['web_data_dataframe'].to_csv(output_path, index=False, encoding='utf-8')
        logging.info(f"Web data DataFrame loaded to: {output_path}")
    else:
        logging.warning("No web data DataFrame found for loading.")

    logging.info("Finished LOAD phase.")

def main():
    """

    Main function to run the ETL pipeline.
    """
    logging.info("ETL pipeline started.")
    
    # Extract
    extracted_data = extract()
    
    # Transform
    if extracted_data: # Check if dictionary is not empty
        transformed_data = transform(extracted_data)
    else:
        transformed_data = None
        logging.warning("No data extracted, skipping TRANSFORM phase.")

    # Load
    if transformed_data: # Check if dictionary is not empty
        load(transformed_data)
    else:
        logging.warning("No data transformed, skipping LOAD phase.")
        
    logging.info("ETL pipeline finished.")

if __name__ == "__main__":
    main()
