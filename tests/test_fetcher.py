import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
import requests

from cotacao import fetch_cotacao


class MockResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json_data = json_data or {}
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"{self.status_code} Error")


def test_fetch_cotacao_success(monkeypatch):
    payload = {"USDBRL": {"bid": "5.10"}}

    def mock_get(url):
        return MockResponse(payload)

    monkeypatch.setattr(requests, "get", mock_get)
    assert fetch_cotacao() == 5.10


def test_fetch_cotacao_http_error(monkeypatch):
    def mock_get(url):
        raise requests.RequestException("network error")

    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(RuntimeError):
        fetch_cotacao()


def test_fetch_cotacao_invalid_json(monkeypatch):
    class BadResponse(MockResponse):
        def json(self):
            raise ValueError("invalid json")

    def mock_get(url):
        return BadResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(RuntimeError):
        fetch_cotacao()
