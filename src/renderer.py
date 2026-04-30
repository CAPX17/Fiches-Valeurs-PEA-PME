"""Rendu Jinja2 + construction du contexte template.

Le contexte fusionne :
  - meta + éditorial (YAML)
  - données auto (MarketData via fetcher)
  - indicateurs calculés (Indicators via indicators)
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .fetcher import MarketData
from .indicators import FiboLevel, Indicators

logger = logging.getLogger(__name__)

PARIS_TZ = ZoneInfo("Europe/Paris")
NA = "n/d"


def _fmt_price(value: float | None, currency: str = "€") -> str:
    """Formate un prix en format FR avec décimales adaptées à la magnitude."""
    if value is None:
        return NA
    if abs(value) < 1:
        decimals = 4
    elif abs(value) < 10:
        decimals = 3
    else:
        decimals = 2
    s = f"{value:,.{decimals}f}".replace(",", " ").replace(".", ",")
    return f"{s} {currency}"


def _fmt_pct(value: float | None, *, signed: bool = True, decimals: int = 2) -> str:
    if value is None:
        return NA
    fmt = f"{{:+.{decimals}f}}" if signed else f"{{:.{decimals}f}}"
    return fmt.format(value).replace(".", ",") + " %"


def _fmt_compact_money(value: float | None, currency: str = "€") -> str:
    """Formate en M€ / Md€ selon la magnitude."""
    if value is None:
        return NA
    if abs(value) >= 1e9:
        return f"{value / 1e9:.2f}".replace(".", ",") + f" Md{currency}"
    if abs(value) >= 1e6:
        return f"{value / 1e6:.1f}".replace(".", ",") + f" M{currency}"
    if abs(value) >= 1e3:
        return f"{value / 1e3:.1f}".replace(".", ",") + f" k{currency}"
    return f"{value:.0f} {currency}"


def _fmt_int_compact(value: float | None) -> str:
    """Formate un entier en M / k pour les volumes/actions."""
    if value is None:
        return NA
    if abs(value) >= 1e9:
        return f"{value / 1e9:.2f}".replace(".", ",") + " Md"
    if abs(value) >= 1e6:
        return f"{value / 1e6:.1f}".replace(".", ",") + " M"
    if abs(value) >= 1e3:
        return f"{value / 1e3:.0f}".replace(".", ",") + " k"
    return f"{int(value)}"


def _fmt_signed_value(value: float | None, decimals: int = 3) -> str:
    if value is None:
        return NA
    return f"{value:+.{decimals}f}".replace(".", ",")


def _fmt_unsigned(value: float | None, decimals: int = 1) -> str:
    if value is None:
        return NA
    return f"{value:.{decimals}f}".replace(".", ",")


def _macd_class(trend: str | None) -> str:
    if trend == "haussier":
        return "up"
    if trend == "baissier":
        return "down"
    return ""


def _change_class(pct: float | None) -> str:
    if pct is None:
        return ""
    return "up" if pct >= 0 else "down"


def _build_charts(market: MarketData) -> dict[str, Any]:
    """Construit les arrays JS pour Chart.js (sparkline / 1y / volumes)."""
    charts: dict[str, Any] = {
        "spark_data": [],
        "spark_delta_pct": None,
        "price_labels": [],
        "price_data": [],
        "vol_labels": [],
        "vol_data": [],
    }

    if not market.history_30d.empty and "Close" in market.history_30d.columns:
        closes = market.history_30d["Close"].dropna()
        charts["spark_data"] = [round(float(v), 4) for v in closes.tolist()]
        if len(closes) >= 2 and closes.iloc[0]:
            charts["spark_delta_pct"] = round(
                (float(closes.iloc[-1]) - float(closes.iloc[0])) / float(closes.iloc[0]) * 100, 2
            )

        vols = market.history_30d["Volume"].fillna(0)
        charts["vol_labels"] = [d.strftime("%d/%m") for d in market.history_30d.index]
        charts["vol_data"] = [int(v) for v in vols.tolist()]

    if not market.history_1y.empty and "Close" in market.history_1y.columns:
        df = market.history_1y["Close"].dropna()
        # Échantillonne ~52 points pour rester lisible
        step = max(1, len(df) // 60)
        df = df.iloc[::step]
        charts["price_labels"] = [d.strftime("%b %y") for d in df.index]
        charts["price_data"] = [round(float(v), 4) for v in df.tolist()]

    return charts


def _build_fibonacci(levels: list[FiboLevel]) -> list[dict[str, Any]]:
    out = []
    for lvl in levels:
        if lvl.status == "current":
            tag_label, tag_class = "Cours ≈", "now"
        elif lvl.status == "support":
            tag_label, tag_class = "Support", "sup"
        else:
            tag_label, tag_class = "Résistance", "res"
        out.append(
            {
                "ratio_pct": _fmt_unsigned(lvl.ratio * 100, decimals=1),
                "price": _fmt_price(lvl.price),
                "distance": _fmt_pct(lvl.distance_pct, signed=True, decimals=1),
                "tag_label": tag_label,
                "tag_class": tag_class,
                "is_current": lvl.status == "current",
            }
        )
    return out


def build_context(
    editorial: dict[str, Any],
    market: MarketData,
    indic: Indicators,
) -> dict[str, Any]:
    """Construit le contexte Jinja complet."""
    currency_symbol = "€" if (market.currency in (None, "EUR")) else (market.currency or "€")

    spark_delta = None
    if not market.history_30d.empty and "Close" in market.history_30d.columns:
        closes = market.history_30d["Close"].dropna()
        if len(closes) >= 2 and closes.iloc[0]:
            spark_delta = (float(closes.iloc[-1]) - float(closes.iloc[0])) / float(closes.iloc[0]) * 100

    history_1y_range = ""
    if not market.history_1y.empty:
        history_1y_range = (
            f"{market.history_1y.index[0].strftime('%b %y').capitalize()} — "
            f"{market.history_1y.index[-1].strftime('%b %y').capitalize()}"
        )

    avg_volume = None
    if not market.history_30d.empty and "Volume" in market.history_30d.columns:
        v = market.history_30d["Volume"].dropna()
        if not v.empty:
            avg_volume = float(v.mean())

    synthese = editorial.get("synthese_ia") or editorial.get("avis") or {}
    force_signal_raw = (
        synthese.get("force_signal") or synthese.get("intensite") or ""
    ).upper()
    force_signal_class = {
        "FORT": "fort",
        "MODÉRÉ": "modere",
        "MODERE": "modere",
        "FAIBLE": "faible",
    }.get(force_signal_raw, "modere")
    score = synthese.get("score") if synthese.get("score") is not None else synthese.get("note")
    texte_synthese = synthese.get("texte_synthese") or synthese.get("texte") or ""
    date_gen = synthese.get("date_generation")
    if hasattr(date_gen, "strftime"):
        date_gen_str = date_gen.strftime("%d/%m/%Y")
    elif date_gen:
        date_gen_str = str(date_gen)
    else:
        date_gen_str = None

    now_paris = datetime.now(PARIS_TZ)
    generated_at = now_paris.strftime("%d/%m/%Y %H:%M")
    generated_at_iso = now_paris.isoformat(timespec="seconds")

    return {
        "meta": {
            "ticker": editorial.get("ticker", market.ticker),
            "isin": editorial.get("isin"),
            "nom": editorial.get("nom"),
            "marche": editorial.get("marche"),
            "secteur": editorial.get("secteur"),
            "ville": editorial.get("ville"),
            "pea_pme_eligible": editorial.get("pea_pme_eligible", False),
            "liens": editorial.get("liens", {}) or {},
        },
        "market": {
            "price": _fmt_price(market.price, currency_symbol),
            "change_pct": _fmt_pct(market.change_pct, signed=True, decimals=2),
            "change_pct_class": _change_class(market.change_pct),
            "market_cap": _fmt_compact_money(market.market_cap, currency_symbol),
            "shares_outstanding": _fmt_int_compact(market.shares_outstanding),
            "high_52w": _fmt_price(market.high_52w, currency_symbol),
            "low_52w": _fmt_price(market.low_52w, currency_symbol),
            "history_1y_range": history_1y_range,
            "avg_volume": _fmt_int_compact(avg_volume),
            "errors": market.errors,
        },
        "indic": {
            "rsi_14": _fmt_unsigned(indic.rsi_14, decimals=1),
            "rsi_zone": indic.rsi_zone or NA,
            "macd": _fmt_signed_value(indic.macd, decimals=4),
            "macd_trend": indic.macd_trend or NA,
            "macd_class": _macd_class(indic.macd_trend),
            "ma_50": _fmt_price(indic.ma_50, currency_symbol),
            "ma_200": _fmt_price(indic.ma_200, currency_symbol),
            "fibonacci": _build_fibonacci(indic.fibonacci),
            "range_position_pct": (
                _fmt_unsigned(indic.range_position_pct, decimals=1)
                if indic.range_position_pct is not None
                else NA
            ),
            "range_position_raw": indic.range_position_pct,
        },
        "spark_delta_pct": _fmt_pct(spark_delta, signed=True, decimals=2) if spark_delta is not None else NA,
        "spark_delta_class": _change_class(spark_delta),
        "alertes": editorial.get("alertes", []) or [],
        "pipeline": editorial.get("pipeline", []) or [],
        "perspectives": editorial.get("perspectives", {}) or {},
        "synthese_ia": {
            "score": score,
            "force_signal_label": force_signal_raw or "MODÉRÉ",
            "force_signal_class": force_signal_class,
            "texte": texte_synthese,
            "facteurs_positifs": synthese.get("facteurs_positifs") or [],
            "facteurs_negatifs": synthese.get("facteurs_negatifs") or [],
            "date_generation": date_gen_str,
        },
        "sources": editorial.get("sources", []) or [],
        "footer": {"generated_at": generated_at, "generated_at_iso": generated_at_iso},
        "charts": _build_charts(market),
    }


def render(context: dict[str, Any], template_dir: Path, template_name: str = "fiche.html") -> str:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tpl = env.get_template(template_name)
    return tpl.render(**context)
