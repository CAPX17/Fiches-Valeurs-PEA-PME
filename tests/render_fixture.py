"""Test visuel hors-ligne : génère docs/index.html à partir d'un fixture JSON.

Utile dans un environnement sans accès yfinance. La structure
MarketData/Indicators est construite à partir d'un snapshot des
valeurs documentées dans la source d'analyse, et d'historiques
synthétiques cohérents avec le range 52s observé.

Usage:
    python tests/render_fixture.py [fixture.json]
"""
from __future__ import annotations

import json
import math
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.fetcher import MarketData  # noqa: E402
from src.indicators import Indicators, _compute_fibo, _range_position  # noqa: E402
from src.renderer import build_context, render  # noqa: E402


def synth_history(low: float, high: float, current: float, days: int) -> pd.DataFrame:
    """Construit une série OHLCV synthétique cohérente avec [low, high] et finissant sur current."""
    end = datetime.now(timezone.utc).replace(hour=17, minute=30, second=0, microsecond=0)
    idx = pd.date_range(end=end, periods=days, freq="B", tz=timezone.utc)
    # Marche aléatoire déterministe
    span = high - low
    closes = []
    for i in range(days):
        t = i / max(1, days - 1)
        # Trajectoire qui passe par high (~1/4), low (~3/4), puis remonte vers current
        wave = (
            low
            + 0.95 * span * (1 - abs(2 * t - 0.25))
            + 0.05 * span * math.sin(t * 12.0)
        )
        wave = max(low, min(high, wave))
        closes.append(wave)
    closes[-1] = current
    closes_s = pd.Series(closes, index=idx)
    df = pd.DataFrame(
        {
            "Open": closes_s.shift(1).fillna(closes_s.iloc[0]),
            "High": closes_s * 1.012,
            "Low": closes_s * 0.988,
            "Close": closes_s,
            "Volume": [int(900_000 + 250_000 * math.sin(i * 0.7)) for i in range(days)],
        },
        index=idx,
    )
    return df


def main() -> int:
    fixture_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tests" / "fixtures" / "ALSEN_29042026.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    md = MarketData(
        ticker=fixture["ticker"],
        fetched_at=datetime.now(timezone.utc),
        price=fixture["price"],
        change_pct=fixture["change_pct"],
        volume=fixture.get("volume"),
        market_cap=fixture["market_cap"],
        shares_outstanding=fixture["shares_outstanding"],
        beta=fixture.get("beta"),
        pe_ratio=fixture.get("pe_ratio"),
        high_52w=fixture["high_52w"],
        low_52w=fixture["low_52w"],
        currency=fixture.get("currency", "EUR"),
        history_1y=synth_history(fixture["low_52w"], fixture["high_52w"], fixture["price"], days=252),
        history_30d=synth_history(fixture["low_52w"], fixture["high_52w"], fixture["price"], days=22),
        errors=[],
    )

    indic = Indicators(
        rsi_14=fixture.get("rsi_14"),
        rsi_zone="neutre" if 30 <= (fixture.get("rsi_14") or 50) <= 70 else ("survente" if (fixture.get("rsi_14") or 50) < 30 else "surachat"),
        macd=fixture.get("macd"),
        macd_signal=fixture.get("macd_signal"),
        macd_trend="haussier" if (fixture.get("macd") or 0) >= (fixture.get("macd_signal") or 0) else "baissier",
        ma_50=fixture.get("ma_50"),
        ma_200=fixture.get("ma_200"),
        fibonacci=_compute_fibo(md.low_52w, md.high_52w, md.price),
        range_position_pct=_range_position(md.price, md.low_52w, md.high_52w),
    )

    editorial = yaml.safe_load((ROOT / "content" / "ALSEN.yaml").read_text(encoding="utf-8"))

    context = build_context(editorial, md, indic)
    html = render(context, ROOT / "templates")

    out_html = ROOT / "docs" / "index.html"
    out_html.parent.mkdir(exist_ok=True)
    out_html.write_text(html, encoding="utf-8")
    shutil.copyfile(ROOT / "static" / "style.css", ROOT / "docs" / "style.css")

    print(f"OK fixture render → {out_html} ({out_html.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
