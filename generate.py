"""Point d'entrée : génère docs/index.html + docs/<TICKER>.html pour
chaque fichier YAML dans content/.

Usage:
    python generate.py [--ticker ALSEN.PA] [--no-cache]

Sans --ticker, toutes les fiches `content/*.yaml` sont régénérées et
un index `docs/index.html` est produit.
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
from src.renderer import build_context, build_index_summary, render, render_index
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


def load_editorial(yaml_path: Path) -> dict:
    """Charge un fichier YAML éditorial."""
    with yaml_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def list_yaml_files() -> list[Path]:
    """Retourne tous les fichiers content/*.yaml triés."""
    return sorted(CONTENT_DIR.glob("*.yaml"))


def render_fiche(yaml_path: Path, *, use_cache: bool) -> dict:
    """Rend une fiche : génère docs/<BASE>.html + dumps data/, retourne le résumé index."""
    editorial = load_editorial(yaml_path)
    ticker = editorial.get("ticker") or yaml_path.stem
    base = ticker.split(".")[0]

    logger.info("=== %s (%s) ===", base, ticker)

    market = fetch_market_data(ticker, use_cache=use_cache)
    if market.errors:
        for err in market.errors:
            logger.warning("Données partielles %s: %s", ticker, err)
    logger.info(
        "Cours=%s var=%s cap=%s 52w=[%s; %s]",
        market.price, market.change_pct, market.market_cap, market.low_52w, market.high_52w,
    )

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

    context = build_context(editorial, market, indic)
    html = render(context, TEMPLATES_DIR)

    out_html = DOCS_DIR / f"{base}.html"
    out_html.write_text(html, encoding="utf-8")
    logger.info("Écrit fiche: %s (%d KB)", out_html, out_html.stat().st_size // 1024)

    # Dumps Markdown pour les routines Claude
    DATA_DIR.mkdir(exist_ok=True)
    synth_path = DATA_DIR / f"{base}_synthese_input.md"
    synth_path.write_text(build_synthesis_dump(editorial, market, indic), encoding="utf-8")
    edit_path = DATA_DIR / f"{base}_editorial_input.md"
    edit_path.write_text(build_editorial_dump(editorial), encoding="utf-8")

    return build_index_summary(editorial, market, indic, base=base)


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère les fiches d'analyse + index.")
    parser.add_argument("--ticker", help="Ne régénère qu'un ticker (le YAML correspondant doit exister)")
    parser.add_argument("--no-cache", action="store_true", help="Ignore le cache yfinance local")
    args = parser.parse_args()

    use_cache = not args.no_cache

    DOCS_DIR.mkdir(exist_ok=True)

    # Sélection des YAML à traiter
    if args.ticker:
        base = args.ticker.split(".")[0]
        yaml_path = CONTENT_DIR / f"{base}.yaml"
        if not yaml_path.exists():
            logger.error("Fichier introuvable: %s", yaml_path)
            return 1
        yaml_files = [yaml_path]
    else:
        yaml_files = list_yaml_files()
        if not yaml_files:
            logger.error("Aucun fichier dans %s", CONTENT_DIR)
            return 1

    logger.info("Traitement de %d fiche(s)", len(yaml_files))

    # Pour --ticker isolé, on ne régénère pas l'index (les autres fiches
    # n'ont pas été rafraîchies, leurs données indices seraient stale).
    # On régénère l'index uniquement pour un build complet.
    summaries: list[dict] = []
    for yp in yaml_files:
        try:
            summary = render_fiche(yp, use_cache=use_cache)
            summaries.append(summary)
        except Exception as exc:  # noqa: BLE001
            logger.error("Erreur sur %s: %s", yp.name, exc, exc_info=True)
            continue

    # CSS toujours copié
    css_src = STATIC_DIR / "style.css"
    css_dst = DOCS_DIR / "style.css"
    shutil.copyfile(css_src, css_dst)

    # Index : régénéré uniquement en build complet (toutes fiches refresh)
    if not args.ticker and summaries:
        index_html = render_index(summaries, TEMPLATES_DIR)
        index_path = DOCS_DIR / "index.html"
        index_path.write_text(index_html, encoding="utf-8")
        logger.info("Écrit index: %s (%d KB)", index_path, index_path.stat().st_size // 1024)

    return 0


if __name__ == "__main__":
    sys.exit(main())
