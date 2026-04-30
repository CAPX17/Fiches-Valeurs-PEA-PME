"""Wrapper yfinance avec cache SQLite local.

Toute valeur indisponible est renvoyée comme None : le renderer
affichera 'n/d' à la place. Aucune donnée n'est jamais inventée.
"""
from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

CACHE_DIR = Path(".cache")
CACHE_DB = CACHE_DIR / "yfinance.sqlite"
CACHE_TTL_MINUTES = 30


@dataclass
class MarketData:
    """Conteneur des données marché retournées par le fetcher."""

    ticker: str
    fetched_at: datetime
    price: float | None = None
    change_pct: float | None = None
    volume: int | None = None
    market_cap: float | None = None
    shares_outstanding: float | None = None
    beta: float | None = None
    pe_ratio: float | None = None
    high_52w: float | None = None
    low_52w: float | None = None
    currency: str | None = None
    history_1y: pd.DataFrame = field(default_factory=pd.DataFrame)
    history_30d: pd.DataFrame = field(default_factory=pd.DataFrame)
    errors: list[str] = field(default_factory=list)


def _ensure_cache() -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS info_cache (
                ticker TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                fetched_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history_cache (
                ticker TEXT NOT NULL,
                period TEXT NOT NULL,
                payload TEXT NOT NULL,
                fetched_at TEXT NOT NULL,
                PRIMARY KEY (ticker, period)
            )
            """
        )


def _cache_get_info(ticker: str) -> dict[str, Any] | None:
    _ensure_cache()
    with sqlite3.connect(CACHE_DB) as conn:
        row = conn.execute(
            "SELECT payload, fetched_at FROM info_cache WHERE ticker = ?",
            (ticker,),
        ).fetchone()
    if not row:
        return None
    payload, fetched_at = row
    if datetime.fromisoformat(fetched_at) < datetime.now(timezone.utc) - timedelta(minutes=CACHE_TTL_MINUTES):
        return None
    return json.loads(payload)


def _cache_put_info(ticker: str, info: dict[str, Any]) -> None:
    _ensure_cache()
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO info_cache (ticker, payload, fetched_at) VALUES (?, ?, ?)",
            (ticker, json.dumps(info, default=str), datetime.now(timezone.utc).isoformat()),
        )


def _cache_get_history(ticker: str, period: str) -> pd.DataFrame | None:
    _ensure_cache()
    with sqlite3.connect(CACHE_DB) as conn:
        row = conn.execute(
            "SELECT payload, fetched_at FROM history_cache WHERE ticker = ? AND period = ?",
            (ticker, period),
        ).fetchone()
    if not row:
        return None
    payload, fetched_at = row
    if datetime.fromisoformat(fetched_at) < datetime.now(timezone.utc) - timedelta(minutes=CACHE_TTL_MINUTES):
        return None
    df = pd.read_json(payload, orient="split")
    df.index = pd.to_datetime(df.index)
    return df


def _cache_put_history(ticker: str, period: str, df: pd.DataFrame) -> None:
    _ensure_cache()
    payload = df.to_json(orient="split", date_format="iso")
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO history_cache (ticker, period, payload, fetched_at) VALUES (?, ?, ?, ?)",
            (ticker, period, payload, datetime.now(timezone.utc).isoformat()),
        )


def _safe_float(value: Any) -> float | None:
    """Convertit en float, retourne None si invalide."""
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if pd.isna(v):
        return None
    return v


def _safe_int(value: Any) -> int | None:
    f = _safe_float(value)
    return int(f) if f is not None else None


def fetch_info(ticker: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Récupère le dict yfinance.info, avec cache."""
    if use_cache:
        cached = _cache_get_info(ticker)
        if cached is not None:
            logger.debug("info cache hit %s", ticker)
            return cached
    try:
        info = dict(yf.Ticker(ticker).info or {})
    except Exception as exc:  # noqa: BLE001
        logger.warning("yfinance info failed for %s: %s", ticker, exc)
        return {}
    _cache_put_info(ticker, info)
    return info


def fetch_history(ticker: str, period: str, *, use_cache: bool = True) -> pd.DataFrame:
    """Récupère l'historique OHLCV pour un ticker. period yfinance: '1y','1mo'..."""
    if use_cache:
        cached = _cache_get_history(ticker, period)
        if cached is not None:
            logger.debug("history cache hit %s %s", ticker, period)
            return cached
    try:
        df = yf.Ticker(ticker).history(period=period, auto_adjust=False)
    except Exception as exc:  # noqa: BLE001
        logger.warning("yfinance history failed for %s %s: %s", ticker, period, exc)
        return pd.DataFrame()
    if df.empty:
        return df
    _cache_put_history(ticker, period, df)
    return df


def fetch_market_data(ticker: str, *, use_cache: bool = True) -> MarketData:
    """Charge l'ensemble des données marché nécessaires à la fiche."""
    md = MarketData(ticker=ticker, fetched_at=datetime.now(timezone.utc))

    info = fetch_info(ticker, use_cache=use_cache)
    if not info:
        md.errors.append("yfinance.info indisponible")

    md.price = _safe_float(info.get("regularMarketPrice") or info.get("currentPrice"))
    prev_close = _safe_float(info.get("regularMarketPreviousClose") or info.get("previousClose"))
    if md.price is not None and prev_close not in (None, 0):
        md.change_pct = (md.price - prev_close) / prev_close * 100
    md.volume = _safe_int(info.get("regularMarketVolume") or info.get("volume"))
    md.market_cap = _safe_float(info.get("marketCap"))
    md.shares_outstanding = _safe_float(info.get("sharesOutstanding"))
    md.beta = _safe_float(info.get("beta"))
    md.pe_ratio = _safe_float(info.get("trailingPE"))
    md.high_52w = _safe_float(info.get("fiftyTwoWeekHigh"))
    md.low_52w = _safe_float(info.get("fiftyTwoWeekLow"))
    md.currency = info.get("currency")

    md.history_1y = fetch_history(ticker, "1y", use_cache=use_cache)
    md.history_30d = fetch_history(ticker, "1mo", use_cache=use_cache)

    if md.history_1y.empty:
        md.errors.append("historique 1y indisponible")
    if md.history_30d.empty:
        md.errors.append("historique 30j indisponible")

    # Fallback 52w depuis l'historique si info incomplet
    if not md.history_1y.empty:
        if md.high_52w is None:
            md.high_52w = _safe_float(md.history_1y["High"].max())
        if md.low_52w is None:
            md.low_52w = _safe_float(md.history_1y["Low"].min())
        if md.price is None:
            md.price = _safe_float(md.history_1y["Close"].iloc[-1])

    return md
