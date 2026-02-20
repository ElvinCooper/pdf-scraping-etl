# tests/test_scraper.py

import requests
from bs4 import BeautifulSoup

from src.scraper import scrape_website


class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error {self.status_code}")


def mock_requests_get(url, **kwargs):
    if url == "https://example.com":
        return MockResponse(
            "<html><head><title>Example</title></head><body><p>Hello, World!</p></body></html>", 200
        )
    return MockResponse("Not Found", 404)


def test_scrape_website_success(monkeypatch):
    """
    Tests successful website scraping.
    """
    monkeypatch.setattr(requests, "get", mock_requests_get)
    result = scrape_website("https://example.com")
    assert result is not None

    soup = BeautifulSoup(result, "lxml")
    assert soup.title.string.strip() == "Example"
    assert soup.p.string.strip() == "Hello, World!"


def test_extract_metadata():
    """
    Tests extraction of metadata from HTML.
    """
    from src.scraper import extract_metadata

    html = "<html><head><title>Test Title</title></head><body><p>Test Para</p></body></html>"
    metadata = extract_metadata(html)
    assert metadata["title"] == "Test Title"
    assert metadata["main_text"] == "Test Para"


def test_scrape_website_failure(monkeypatch):
    """
    Tests website scraping failure.
    """
    monkeypatch.setattr(requests, "get", mock_requests_get)
    result = scrape_website("https://nonexistent.com")
    assert result is None
