# src/etl_pipeline.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract():
    """
    Extract data from source.
    This could be from a website (scraping) or a local file.
    """
    logging.info("Starting EXTRACT phase...")
    # TODO: Implement data extraction logic
    logging.info("Finished EXTRACT phase.")
    return None

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
