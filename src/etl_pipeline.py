# src/etl_pipeline.py

import os
import re
from typing import Any, Dict, Optional

import pandas as pd

from src.logger import logger
from src.pdf_extractor import extract_text_from_pdf
from src.scraper import extract_metadata, scrape_website


def clean_text(text: Optional[str]) -> Optional[str]:
    """
    Cleans text by removing extra whitespace and standardizing newlines.
    """
    if text is None:
        return None
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces/newlines with a single space
    text = text.strip()  # Remove leading/trailing whitespace
    return text


def extract() -> Dict[str, Any]:
    """
    Extract data from sources: local PDF and external URLs.
    """
    logger.info("Starting EXTRACT phase...")
    extracted_data = {}

    # --- PDF Extraction ---
    sample_pdf_path = os.path.join("data", "input", "sample.pdf")
    if os.path.exists(sample_pdf_path):
        pdf_text = extract_text_from_pdf(sample_pdf_path)
        if pdf_text:
            extracted_data["pdf_text"] = pdf_text
    else:
        logger.warning(f"PDF file not found: {sample_pdf_path}. Skipping PDF extraction.")

    # --- Web Scraping ---
    sample_url_file = os.path.join("data", "input", "sample_url.txt")
    scraped_contents = []
    if os.path.exists(sample_url_file):
        with open(sample_url_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]

        if urls:
            for url in urls:
                content = scrape_website(url)
                if content:
                    scraped_contents.append({"url": url, "content": content})
        else:
            logger.info(f"No URLs found in {sample_url_file}. Skipping web scraping.")
    else:
        logger.warning(f"URL list file not found: {sample_url_file}. Skipping web scraping.")

    if scraped_contents:
        extracted_data["web_scraped_data"] = scraped_contents

    logger.info(f"Finished EXTRACT phase. Collected: {list(extracted_data.keys())}")
    return extracted_data


def transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform the extracted data.
    This involves cleaning, processing, and structuring the data.
    """
    logger.info("Starting TRANSFORM phase...")
    transformed_data = {}

    # --- Transform PDF text ---
    if "pdf_text" in data:
        transformed_data["cleaned_pdf_text"] = clean_text(data["pdf_text"])
    else:
        logger.warning("No PDF text found for transformation.")

    # --- Transform Web Scraped Data ---
    if "web_scraped_data" in data:
        structured_web_data = []
        for item in data["web_scraped_data"]:
            url = item.get("url")
            html_content = item.get("content")

            if html_content:
                metadata = extract_metadata(html_content)
                structured_web_data.append(
                    {
                        "url": url,
                        "title": clean_text(metadata.get("title")),
                        "main_text": clean_text(metadata.get("main_text")),
                    }
                )

        if structured_web_data:
            transformed_data["web_data_dataframe"] = pd.DataFrame(structured_web_data)
        else:
            logger.warning("No structured web data found after processing.")
    else:
        logger.warning("No web scraped data found for transformation.")

    logger.info("Finished TRANSFORM phase.")
    return transformed_data


def load(data: Dict[str, Any]) -> None:
    """
    Load the transformed data into a destination (TXT and CSV files).
    """
    logger.info("Starting LOAD phase...")
    output_dir = os.path.join("data", "output")
    os.makedirs(output_dir, exist_ok=True)

    # --- Load Cleaned PDF Text ---
    if "cleaned_pdf_text" in data and data["cleaned_pdf_text"]:
        output_path = os.path.join(output_dir, "extracted_text.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(data["cleaned_pdf_text"])
        logger.info(f"Cleaned PDF text loaded to: {output_path}")
    else:
        logger.warning("No cleaned PDF text found for loading.")

    # --- Load Web Data DataFrame ---
    web_df = data.get("web_data_dataframe")
    if isinstance(web_df, pd.DataFrame) and not web_df.empty:
        output_path = os.path.join(output_dir, "cleaned_data.csv")
        data["web_data_dataframe"].to_csv(output_path, index=False, encoding="utf-8")
        logger.info(f"Web data DataFrame loaded to: {output_path}")
    else:
        logger.warning("No web data DataFrame found for loading.")

    logger.info("Finished LOAD phase.")


def main() -> None:
    """
    Main entry point for the ETL pipeline.
    """
    logger.info("ETL pipeline started.")

    # Extract
    extracted_data = extract()

    # Transform
    transformed_data = transform(extracted_data) if extracted_data else None

    # Load
    if transformed_data:
        load(transformed_data)
    else:
        logger.warning("No data transformed, skipping LOAD phase.")

    logger.info("ETL pipeline finished.")


if __name__ == "__main__":
    main()
