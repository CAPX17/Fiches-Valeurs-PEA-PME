"""Génère un dump Markdown des données factuelles d'une valeur.

Deux dumps sont produits :
- `build_synthesis_dump` → input pour la routine Claude SYNTHÈSE IA
  (régénère `synthese_ia` du YAML chaque lundi).
- `build_editorial_dump` → input pour la routine Claude ÉDITORIALE
  (modifie `alertes`/`pipeline`/`perspectives` chaque lundi, avec
  auto-audit obligatoire).

Toutes les valeurs proviennent du même pipeline que la fiche HTML :
yfinance + indicators + YAML éditorial. Aucune extrapolation.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from .fetcher import MarketData
from .indicators import Indicators

NA = "n/d"


def _fmt_price(value: float | None, currency: str = "€") -> str:
    if value is None:
        return NA
    if abs(value) < 1:
        decimals = 4
    elif abs(value) < 10:
        decimals = 3
    else:
        decimals = 2
    s = f"{value:.{decimals}f}".replace(".", ",")
    return f"{s} {currency}"


def _fmt_pct(value: float | None, *, signed: bool = True, decimals: int = 2) -> str:
    if value is None:
        return NA
    fmt = f"{{:+.{decimals}f}}" if signed else f"{{:.{decimals}f}}"
    return fmt.format(value).replace(".", ",") + " %"


def _fmt_compact_money(value: float | None, currency: str = "€") -> str:
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
    if value is None:
        return NA
    if abs(value) >= 1e9:
        return f"{value / 1e9:.2f}".replace(".", ",") + " Md"
    if abs(value) >= 1e6:
        return f"{value / 1e6:.1f}".replace(".", ",") + " M"
    if abs(value) >= 1e3:
        return f"{value / 1e3:.0f}".replace(".", ",") + " k"
    return f"{int(value)}"


def _variation_n_business_days(history: pd.DataFrame, n: int) -> float | None:
    """Variation en % entre le dernier close et celui de N jours ouvrés plus tôt."""
    if history is None or history.empty or "Close" not in history.columns:
        return None
    closes = history["Close"].dropna()
    if len(closes) <= n:
        return None
    last = float(closes.iloc[-1])
    past = float(closes.iloc[-(n + 1)])
    if past == 0:
        return None
    return (last - past) / past * 100


def _variation_full_period(history: pd.DataFrame) -> float | None:
    """Variation entre le premier et le dernier close de l'historique."""
    if history is None or history.empty or "Close" not in history.columns:
        return None
    closes = history["Close"].dropna()
    if len(closes) < 2:
        return None
    first = float(closes.iloc[0])
    last = float(closes.iloc[-1])
    if first == 0:
        return None
    return (last - first) / first * 100


def _delta_vs_ma(price: float | None, ma: float | None) -> float | None:
    if price is None or ma in (None, 0):
        return None
    return (price - ma) / ma * 100


def _fibo_status_label(status: str) -> str:
    return {
        "current": "Cours actuel",
        "support": "Support",
        "resistance": "Résistance",
    }.get(status, status)


def _fmt_alertes(alertes: list[dict]) -> str:
    if not alertes:
        return "_Aucune alerte documentée._"
    lines = []
    for a in alertes:
        cat = a.get("categorie", "")
        titre = a.get("titre", "")
        desc = (a.get("description") or "").strip()
        lines.append(f"**[{cat}] {titre}**\n\n{desc}\n")
    return "\n".join(lines)


def _fmt_pipeline(pipeline: list[dict]) -> str:
    if not pipeline:
        return "_Pipeline non documenté._"
    rows = ["| Programme | Indication | Stade | Prochaine étape |", "|---|---|---|---|"]
    for p in pipeline:
        rows.append(
            "| {prog} | {ind} | {stade} | {next} |".format(
                prog=p.get("programme", ""),
                ind=p.get("indication", ""),
                stade=p.get("stade", ""),
                next=p.get("prochaine_etape", ""),
            )
        )
    return "\n".join(rows)


def _fmt_perspectives(perspectives: dict) -> str:
    if not perspectives:
        return "_Perspectives non documentées._"
    blocs = []
    for cle, label in (
        ("court_terme", "Court terme"),
        ("moyen_terme", "Moyen terme"),
        ("long_terme", "Long terme"),
    ):
        section = perspectives.get(cle) or {}
        horizon = section.get("horizon", "")
        points = section.get("points") or []
        bloc = [f"**{label}** ({horizon})"]
        for p in points:
            bloc.append(f"- {p}")
        blocs.append("\n".join(bloc))
    return "\n\n".join(blocs)


def _fmt_synthese_precedente(synthese: dict) -> str:
    if not synthese:
        return "_Aucune synthèse IA précédente._"
    score = synthese.get("score") if synthese.get("score") is not None else synthese.get("note", NA)
    force = synthese.get("force_signal") or synthese.get("intensite") or NA
    date_gen = synthese.get("date_generation")
    if hasattr(date_gen, "strftime"):
        date_str = date_gen.strftime("%Y-%m-%d")
    else:
        date_str = str(date_gen) if date_gen else NA
    texte = (synthese.get("texte_synthese") or synthese.get("texte") or "").strip()
    pos = synthese.get("facteurs_positifs") or []
    neg = synthese.get("facteurs_negatifs") or []
    out = [
        f"- Score précédent : {score}",
        f"- Force du signal précédente : {force}",
        f"- Date génération précédente : {date_str}",
        "- Texte de synthèse précédent :",
    ]
    if texte:
        for line in texte.splitlines():
            out.append(f"  > {line}" if line.strip() else "  >")
    else:
        out.append("  > _vide_")
    out.append("- Facteurs positifs précédents :")
    for f in pos:
        out.append(f"  - {f}")
    if not pos:
        out.append("  - _aucun_")
    out.append("- Facteurs négatifs précédents :")
    for f in neg:
        out.append(f"  - {f}")
    if not neg:
        out.append("  - _aucun_")
    return "\n".join(out)


def build_synthesis_dump(
    editorial: dict[str, Any],
    market: MarketData,
    indic: Indicators,
) -> str:
    """Produit le contenu Markdown du dump pour une valeur."""
    nom = editorial.get("nom", "")
    ticker = editorial.get("ticker", market.ticker)
    currency = market.currency or "€"

    pos_range = indic.range_position_pct

    var_1d = market.change_pct
    var_7d = _variation_n_business_days(market.history_1y, 5)
    var_30d = _variation_full_period(market.history_30d)
    var_90d = _variation_n_business_days(market.history_1y, 63)
    var_1y = _variation_full_period(market.history_1y)

    delta_ma50 = _delta_vs_ma(market.price, indic.ma_50)
    delta_ma200 = _delta_vs_ma(market.price, indic.ma_200)

    macd_str = (
        f"{indic.macd:+.4f}".replace(".", ",")
        if indic.macd is not None
        else NA
    )
    macd_trend = indic.macd_trend or NA

    # Fibonacci table
    if indic.fibonacci:
        fib_rows = ["| Niveau | Prix | Δ vs cours | Statut |", "|---|---|---|---|"]
        for lvl in indic.fibonacci:
            niveau = f"{lvl.ratio * 100:.1f} %".replace(".", ",")
            fib_rows.append(
                "| {n} | {p} | {d} | {s} |".format(
                    n=niveau,
                    p=_fmt_price(lvl.price, currency),
                    d=_fmt_pct(lvl.distance_pct, signed=True, decimals=2),
                    s=_fibo_status_label(lvl.status),
                )
            )
        fib_block = "\n".join(fib_rows)
    else:
        fib_block = "_Niveaux Fibonacci non calculables._"

    pea = "éligible" if editorial.get("pea_pme_eligible") else "non éligible"
    liens = editorial.get("liens", {}) or {}
    site_ir = liens.get("site_ir", NA)

    synthese_prev = editorial.get("synthese_ia") or editorial.get("avis") or {}

    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    sections = [
        f"# Données pour synthèse IA — {nom} ({ticker})",
        "",
        f"**Date de génération du dump** : {now_iso}",
        f"**Source** : yfinance + content/{ticker.split('.')[0]}.yaml",
        "",
        "---",
        "",
        "## 1. Données de marché (yfinance, dernier cours connu)",
        "",
        f"- Cours : {_fmt_price(market.price, currency)}",
        f"- Variation jour : {_fmt_pct(var_1d, signed=True, decimals=2)}",
        f"- Volume jour : {_fmt_int_compact(market.volume)}",
        f"- Capitalisation : {_fmt_compact_money(market.market_cap, currency)}",
        f"- Nombre d'actions : {_fmt_int_compact(market.shares_outstanding)}",
        f"- Plus-haut 52 semaines : {_fmt_price(market.high_52w, currency)}",
        f"- Plus-bas 52 semaines : {_fmt_price(market.low_52w, currency)}",
        f"- Position dans range 52s : {_fmt_pct(pos_range, signed=False, decimals=1) if pos_range is not None else NA}",
        "",
        "## 2. Indicateurs techniques",
        "",
        f"- RSI(14) : {(_fmt_pct(indic.rsi_14, signed=False, decimals=1).replace(' %','') if indic.rsi_14 is not None else NA)}"
        f" (zone {indic.rsi_zone or NA})",
        f"- MACD : {macd_str} (signal {macd_trend})",
        f"- MA50 : {_fmt_price(indic.ma_50, currency)}",
        f"- MA200 : {_fmt_price(indic.ma_200, currency)}",
        f"- Cours vs MA50 : {_fmt_pct(delta_ma50, signed=True, decimals=2)}",
        f"- Cours vs MA200 : {_fmt_pct(delta_ma200, signed=True, decimals=2)}",
        "",
        "## 3. Niveaux Fibonacci (range 52s)",
        "",
        fib_block,
        "",
        "## 4. Variations historiques",
        "",
        f"- Variation 1 jour : {_fmt_pct(var_1d, signed=True, decimals=2)}",
        f"- Variation 7 jours : {_fmt_pct(var_7d, signed=True, decimals=2)}",
        f"- Variation 30 jours : {_fmt_pct(var_30d, signed=True, decimals=2)}",
        f"- Variation 90 jours : {_fmt_pct(var_90d, signed=True, decimals=2)}",
        f"- Variation 1 an : {_fmt_pct(var_1y, signed=True, decimals=2)}",
        "",
        "## 5. Métadonnées société (depuis YAML éditorial)",
        "",
        f"- Nom : {editorial.get('nom', NA)}",
        f"- ISIN : {editorial.get('isin', NA)}",
        f"- Marché : {editorial.get('marche', NA)}",
        f"- Secteur : {editorial.get('secteur', NA)}",
        f"- PEA-PME : {pea}",
        f"- Liens IR : {site_ir}",
        "",
        "## 6. Contexte éditorial actuel (depuis YAML éditorial)",
        "",
        "### Alertes & catalyseurs documentés",
        "",
        _fmt_alertes(editorial.get("alertes", []) or []),
        "",
        "### Pipeline",
        "",
        _fmt_pipeline(editorial.get("pipeline", []) or []),
        "",
        "### Perspectives",
        "",
        _fmt_perspectives(editorial.get("perspectives", {}) or {}),
        "",
        "## 7. Synthèse IA précédente (pour comparaison)",
        "",
        _fmt_synthese_precedente(synthese_prev),
        "",
    ]
    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Dump éditorial — input pour la routine ÉDITORIALE hebdomadaire
# ---------------------------------------------------------------------------

# Audits de référence figés. Ces garde-fous sont indexés par ticker :
# la routine éditoriale ne doit JAMAIS produire une modification qui les
# contredit. Voir data/<TICKER>_audit_<DATE>.md pour la justification
# détaillée de chaque garde-fou.
AUDIT_REFERENCE_RAPPEL: dict[str, list[str]] = {
    "ALSEN.PA": [
        "Concurrence : **Lilly = Akouos** (rachat oct 2022), **Regeneron = Decibel/Otarmeni** "
        "(rachat sept 2023, AMM FDA accélérée avril 2026). Toute formulation inversée "
        "(« Akouos via Regeneron » ou « Decibel via Lilly ») est interdite.",
        "Sanofi : **13,9 % du capital post-offre** (PAS « ~11 % »), source "
        "BusinessWire 27/01/2026.",
        "SENS-40 : programme **historique Phase 2b**, statut à reconfirmer "
        "post-pivot gène-thérapie. Aucune relance « SENS-40 multi-indications "
        "Phase 2 active » sans communiqué Sensorion 2026 explicite.",
    ],
    "BE": [
        "Bloom Energy = **SOFC haute température** (PAS PEM comme Plug/Ballard, "
        "PAS MCFC comme FuelCell Energy). Toute confusion technologique est interdite.",
        "Société américaine NYSE — **NON éligible PEA-PME**. Aucune routine ne doit "
        "reclasser BE en cadre PEA-PME.",
        "Deal Oracle au 27/04/2026 = **2,8 GW total** (1,2 GW déjà sous contrat) "
        "+ **Project Jupiter 2,45 GW** (BorderPlex, New Mexico) + **warrant Oracle 400 M$** "
        "sur le stock BE.",
        "Deal AEP janvier 2026 = **2,65 Md$ pour 1 GW de SOFC**. AWS et Cologix sont "
        "derrière le premier déploiement Ohio (PUCO juin 2025, 72,9 MW initiaux).",
        "Crédit hydrogène 45V **raboté** par la One Big Beautiful Bill Act signée par "
        "Donald Trump le **04/07/2025** (construction obligatoire avant 31/12/2027). "
        "Le crédit ITC § 48E pour fuel cells reste préservé jusqu'à phase-out post-2032.",
        "Q1 2026 publié **28/04/2026** : revenus **751,1 M$ (+130,4 % YoY)**, EPS "
        "**0,44 $**. Guidance FY2026 relevée à **3,4-3,8 Md$** (mid 3,6 Md$).",
        "Cours **283,36 $ / capi ~80,6 Md$ au 01/05/2026, +134 % YTD 2026** ; "
        "ratio implicite **~22x mid-guidance FY2026** (calcul transparent capi/guidance).",
    ],
}


def build_editorial_dump(editorial: dict[str, Any]) -> str:
    """Produit le Markdown d'input pour la routine ÉDITORIALE hebdomadaire.

    Les garde-fous figés (AUDIT_REFERENCE_RAPPEL) sont injectés UNIQUEMENT
    pour le ticker courant — pas de pollution croisée entre fiches.
    """
    nom = editorial.get("nom", "")
    ticker = editorial.get("ticker", "")
    sources = editorial.get("sources", []) or []

    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if sources:
        sources_block = "\n".join(f"- {s}" for s in sources)
    else:
        sources_block = "_Aucune source référencée._"

    rappels = AUDIT_REFERENCE_RAPPEL.get(ticker, [])
    if rappels:
        rappels_block = "\n".join(f"- {r}" for r in rappels)
    else:
        rappels_block = (
            "_Aucun garde-fou figé pour ce ticker. La routine éditoriale "
            "doit s'appuyer uniquement sur les sources primaires datées._"
        )

    sections = [
        f"# Données pour mise à jour éditoriale — {nom} ({ticker})",
        "",
        f"**Date de génération du dump** : {now_iso}",
        f"**Source** : content/{ticker.split('.')[0]}.yaml (état actuel)",
        "",
        "Ce fichier est l'input de la routine Claude ÉDITORIALE hebdomadaire.",
        "Il reflète l'état actuel des sections éditoriales et rappelle les",
        f"garde-fous issus de l'audit baseline de {ticker}.",
        "",
        "---",
        "",
        "## État actuel des sections éditoriales",
        "",
        "### Alertes (état actuel)",
        "",
        _fmt_alertes(editorial.get("alertes", []) or []),
        "",
        "### Pipeline (état actuel)",
        "",
        _fmt_pipeline(editorial.get("pipeline", []) or []),
        "",
        "### Perspectives (état actuel)",
        "",
        _fmt_perspectives(editorial.get("perspectives", {}) or {}),
        "",
        "## Sources actuellement référencées",
        "",
        sources_block,
        "",
        f"## Garde-fous figés pour {ticker} (audit baseline)",
        "",
        "Ces points NE DOIVENT PAS être contredits dans une modification future.",
        "",
        rappels_block,
        "",
    ]
    return "\n".join(sections)
