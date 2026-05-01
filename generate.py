"""Point d'entrée : génère docs/index.html à partir du YAML éditorial.

Usage:
    python generate.py [--ticker ALSEN.PA] [--no-cache]
"""
from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

import yaml

from src.fetcher import fetch_market_data
from src.indicators import compute_indicators
from src.renderer import build_context, render
from src.synthesis_dump import build_editorial_dump, build_synthesis_dump

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DOCS_DIR = ROOT / "docs"
DATA_DIR = ROOT / "data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("generate")


def load_editorial(ticker: str) -> dict:
    """Charge le YAML éditorial pour un ticker (fichier <SYMBOLE>.yaml)."""
    symbol = ticker.split(".")[0]
    yaml_path = CONTENT_DIR / f"{symbol}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"Fichier éditorial introuvable: {yaml_path}")
    with yaml_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère la fiche d'analyse.")
    parser.add_argument("--ticker", default="ALSEN.PA", help="Ticker yfinance (défaut: ALSEN.PA)")
    parser.add_argument("--no-cache", action="store_true", help="Ignore le cache yfinance local")
    args = parser.parse_args()

    ticker = args.ticker
    use_cache = not args.no_cache

    logger.info("Chargement YAML éditorial pour %s", ticker)
    editorial = load_editorial(ticker)

    logger.info("Récupération des données marché (yfinance)")
    market = fetch_market_data(ticker, use_cache=use_cache)
    if market.errors:
        for err in market.errors:
            logger.warning("Données partielles: %s", err)
    logger.info(
        "Cours=%s var=%s cap=%s 52w=[%s; %s]",
        market.price, market.change_pct, market.market_cap, market.low_52w, market.high_52w,
    )

    logger.info("Calcul des indicateurs techniques")
    indic = compute_indicators(
        market.history_1y,
        current_price=market.price,
        high_52w=market.high_52w,
        low_52w=market.low_52w,
    )
    logger.info(
        "RSI=%s MACD=%s MA50=%s MA200=%s pos52w=%s%%",
        indic.rsi_14, indic.macd, indic.ma_50, indic.ma_200, indic.range_position_pct,
    )

    logger.info("Construction du contexte Jinja")
    context = build_context(editorial, market, indic)

    logger.info("Rendu du template")
    html = render(context, TEMPLATES_DIR)

    DOCS_DIR.mkdir(exist_ok=True)
    out_html = DOCS_DIR / "index.html"
    out_html.write_text(html, encoding="utf-8")

    css_src = STATIC_DIR / "style.css"
    css_dst = DOCS_DIR / "style.css"
    shutil.copyfile(css_src, css_dst)

    logger.info("Écrit: %s (%d KB) + %s", out_html, out_html.stat().st_size // 1024, css_dst.name)

    # Dumps Markdown destinés aux routines Claude hebdomadaires
    DATA_DIR.mkdir(exist_ok=True)
    symbol = ticker.split(".")[0]

    synth_path = DATA_DIR / f"{symbol}_synthese_input.md"
    synth_path.write_text(build_synthesis_dump(editorial, market, indic), encoding="utf-8")
    logger.info("Écrit dump synthèse: %s (%d KB)", synth_path, synth_path.stat().st_size // 1024)

    edit_path = DATA_DIR / f"{symbol}_editorial_input.md"
    edit_path.write_text(build_editorial_dump(editorial), encoding="utf-8")
    logger.info("Écrit dump éditorial: %s (%d KB)", edit_path, edit_path.stat().st_size // 1024)

    return 0


if __name__ == "__main__":
    sys.exit(main())
