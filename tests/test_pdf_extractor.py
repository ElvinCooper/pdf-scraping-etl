# tests/test_pdf_extractor.py

import pdfplumber

from src.pdf_extractor import extract_tables_from_pdf, extract_text_from_pdf


class MockPage:
    def __init__(self, text, tables):
        self._text = text
        self._tables = tables

    def extract_text(self):
        return self._text

    def extract_tables(self):
        return self._tables


class MockPdf:
    def __init__(self, pages):
        self.pages = pages

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def mock_pdfplumber_open(path):
    if path == "dummy.pdf":
        pages = [
            MockPage("This is page 1.", [[["col1", "col2"], ["val1", "val2"]]]),
            MockPage("This is page 2.", []),
        ]
        return MockPdf(pages)
    raise FileNotFoundError("File not found")


def test_extract_text_from_pdf_success(monkeypatch):
    """
    Tests successful text extraction from a PDF.
    """
    monkeypatch.setattr(pdfplumber, "open", mock_pdfplumber_open)
    result = extract_text_from_pdf("dummy.pdf")
    assert result is not None
    assert "This is page 1." in result
    assert "This is page 2." in result
    assert result == "This is page 1.\nThis is page 2.\n"


def test_extract_tables_from_pdf_success(monkeypatch):
    """
    Tests successful table extraction from a PDF.
    """
    monkeypatch.setattr(pdfplumber, "open", mock_pdfplumber_open)
    result = extract_tables_from_pdf("dummy.pdf")
    assert result is not None
    assert len(result) == 1
    assert result[0] == [["col1", "col2"], ["val1", "val2"]]


def test_extract_text_from_pdf_failure(monkeypatch):
    """
    Tests failure when PDF file does not exist.
    """

    def mock_open_raise_error(path):
        raise FileNotFoundError("File not found")

    monkeypatch.setattr(pdfplumber, "open", mock_open_raise_error)
    result = extract_text_from_pdf("nonexistent.pdf")
    assert result is None
