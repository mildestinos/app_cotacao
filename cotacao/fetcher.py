"""Helpers for fetching currency exchange rates."""

from __future__ import annotations

import requests

URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"


def fetch_cotacao(url: str = URL) -> float:
    """Fetch USD to BRL rate from *url* and return the bid price as float.

    Raises RuntimeError if the request fails or the response structure is
    unexpected.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError("Failed to fetch cotação") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Invalid JSON received") from exc

    try:
        bid = data["USDBRL"]["bid"]
        return float(bid)
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("Unexpected response format") from exc
