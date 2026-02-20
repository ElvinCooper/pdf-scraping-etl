# tests/test_etl_pipeline.py

from src import etl_pipeline


def test_main_full_run(monkeypatch):
    """
    Tests the main function of the ETL pipeline for a full run.
    """
    # Mock extract, transform, and load functions
    monkeypatch.setattr(etl_pipeline, "extract", lambda: {"data": "dummy"})
    monkeypatch.setattr(etl_pipeline, "transform", lambda data: {"transformed_data": "dummy"})
    monkeypatch.setattr(etl_pipeline, "load", lambda data: None)

    # Spy on the functions to check if they were called
    extract_called = []
    transform_called = []
    load_called = []

    monkeypatch.setattr(
        etl_pipeline, "extract", lambda: extract_called.append(True) or {"data": "dummy"}
    )
    monkeypatch.setattr(
        etl_pipeline,
        "transform",
        lambda data: transform_called.append(True) or {"transformed_data": "dummy"},
    )
    monkeypatch.setattr(etl_pipeline, "load", lambda data: load_called.append(True))

    etl_pipeline.main()

    assert extract_called
    assert transform_called
    assert load_called


def test_main_no_extract_data(monkeypatch):
    """
    Tests the main function when no data is extracted.
    """
    monkeypatch.setattr(etl_pipeline, "extract", lambda: {})
    monkeypatch.setattr(etl_pipeline, "transform", lambda data: {"transformed_data": "dummy"})
    monkeypatch.setattr(etl_pipeline, "load", lambda data: None)

    extract_called = []
    transform_called = []
    load_called = []

    monkeypatch.setattr(etl_pipeline, "extract", lambda: extract_called.append(True) or {})
    monkeypatch.setattr(
        etl_pipeline,
        "transform",
        lambda data: transform_called.append(True) or {"transformed_data": "dummy"},
    )
    monkeypatch.setattr(etl_pipeline, "load", lambda data: load_called.append(True))

    etl_pipeline.main()

    assert extract_called
    assert not transform_called
    assert not load_called


def test_main_no_transform_data(monkeypatch):
    """
    Tests the main function when no data is transformed.
    """
    monkeypatch.setattr(etl_pipeline, "extract", lambda: {"data": "dummy"})
    monkeypatch.setattr(etl_pipeline, "transform", lambda data: {})
    monkeypatch.setattr(etl_pipeline, "load", lambda data: None)

    extract_called = []
    transform_called = []
    load_called = []

    monkeypatch.setattr(
        etl_pipeline, "extract", lambda: extract_called.append(True) or {"data": "dummy"}
    )
    monkeypatch.setattr(etl_pipeline, "transform", lambda data: transform_called.append(True) or {})
    monkeypatch.setattr(etl_pipeline, "load", lambda data: load_called.append(True))

    etl_pipeline.main()

    assert extract_called
    assert transform_called
    assert not load_called
