# src/scraper.py

from typing import Optional

import requests
from bs4 import BeautifulSoup

from src.logger import logger


def scrape_website(url: str) -> Optional[str]:
    """
    Performs web scraping on the given URL.
    Returns the HTML content as a string if successful, None otherwise.
    """
    logger.info(f"Scraping data from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        # Use lxml parser as it's efficient
        soup = BeautifulSoup(response.text, "lxml")
        logger.info(f"Successfully scraped: {url}")
        return soup.prettify()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error scraping {url}: {e}")
        return None


def extract_metadata(html_content: str) -> dict:
    """
    Extracts basic metadata (title, paragraphs) from HTML content.
    """
    if not html_content:
        return {}

    soup = BeautifulSoup(html_content, "lxml")

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text().strip() if title_tag else "No Title"

    # Extract main text from paragraphs
    paragraphs = soup.find_all("p")
    main_text = " ".join([p.get_text().strip() for p in paragraphs])

    return {"title": title, "main_text": main_text}


if __name__ == "__main__":
    # Example usage:
    sample_url = "http://example.com"
    scraped_content = scrape_website(sample_url)
    if scraped_content:
        metadata = extract_metadata(scraped_content)
        print(f"Metadata from {sample_url}:")
        print(f"Title: {metadata['title']}")
        print(f"Main Text: {metadata['main_text'][:200]}...")
