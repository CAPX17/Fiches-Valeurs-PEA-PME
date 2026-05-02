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

    # Section 8 : garde-fous d'audit (structurels + hebdo durcis)
    # Injectés pour permettre aux sous-agents A et B (Pattern C+ allégé)
    # de tester leurs propositions contre les conclusions des audits.
    struct_block, hebdo_block = _format_audit_rappel(ticker)
    sections.extend([
        f"## 8. Garde-fous d'audit pour {ticker}",
        "",
        "### Garde-fous structurels (faits stables — ne pas contredire)",
        "",
        struct_block,
        "",
        "### Garde-fous hebdo durcis (règles procédurales pour les routines)",
        "",
        hebdo_block,
        "",
    ])
    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Dump éditorial — input pour la routine ÉDITORIALE hebdomadaire
# ---------------------------------------------------------------------------

# Audits de référence figés. Structure imbriquée par ticker :
#   - garde_fous_structurels : conclusions des audits baseline + recalCplus
#       (faits factuels stables qu'aucune routine ne doit contredire).
#   - garde_fous_hebdo_durcis : règles procédurales que les routines hebdo
#       (Pattern C+ allégé) doivent appliquer à toute modification candidate.
# Voir data/<TICKER>_audit_<DATE>.md et data/<TICKER>_recalCplus_*.md pour
# la justification détaillée des garde-fous structurels.

# Règles procédurales communes aux routines hebdo de toutes les fiches.
# Chaque ticker peut surcharger via une liste spécifique si besoin.
HEBDO_DURCIS_DEFAULTS: list[str] = [
    "Toute modification d'un chiffre clé (cours, capi, trésorerie, "
    "% de détention, dilution) requiert **3 sources primaires concordantes** "
    "datées < 7 jours.",
    "Toute **suppression d'alerte présente depuis < 30 jours** est bloquée "
    "sauf si l'événement de la semaine la rend explicitement obsolète "
    "(source primaire à l'appui).",
    "Toute modification touchant un **garde-fou structurel** est bloquée "
    "automatiquement par la règle R3/R6 du méta-audit C.",
    "Toute claim de confiance **FAIBLE** chez A ou B est ignorée — "
    "pas de mode « Selon [source unique] » sur claim faible.",
    "Toute modification du **score IA > 1 point en valeur absolue** "
    "requiert une justification factuelle nouvelle, datée et sourcée "
    "dans la fenêtre 7 jours. Sinon score inchangé.",
]

AUDIT_REFERENCE_RAPPEL: dict[str, dict[str, list[str]]] = {
    "ALSEN.PA": {
        "garde_fous_structurels": [
            "Concurrence : **Lilly = Akouos** (rachat oct 2022, AK-OTOF en essai Phase 1/2 "
            "NCT05821959 fin estimée octobre 2028), **Regeneron = Decibel/Otarmeni** "
            "(rachat sept 2023, AMM FDA accélérée 23/04/2026). Toute formulation inversée "
            "(« Akouos via Regeneron » ou « Decibel via Lilly ») est interdite.",
            "Sanofi : **13,9 % du capital post-offre** (PAS « ~11 % »), source "
            "BusinessWire 27/01/2026. Tour 60 M€ via émission de 214 285 714 actions à "
            "0,28 €, **dilution ~71 % du capital antérieur**.",
            "**SENS-401** (et non « SENS-40 ») = arazasétron, petite molécule. Indications "
            "historiques : SSNHL Phase 2b achevée selon BioSpace 18/03/2026 · implant "
            "cochléaire Phase 2a en partenariat Cochlear Limited (critère pharmacocinétique "
            "atteint en 2024) · cisplatine/CIO Phase 2 NOTOXIS achevée au T1 2026 selon "
            "Sensorion FY2025 PR. Statut secondaire post-pivot gène-thérapie.",
            "**Démission CEO Nawal Ouzren le 16/02/2026** (PR primaire BusinessWire ; "
            "certains relais secondaires datent l'annonce du 17/02). Amit Munshi (président "
            "CA) assure l'intérim ; CEO permanent à nommer. Toute mise à jour future doit "
            "refléter le statut intérim jusqu'à nomination du successeur.",
            "**Épidémiologie scientifique** : OTOF = 1-8 % des surdités congénitales non "
            "syndromiques (GeneReviews) ; GJB2 = jusqu'à 50 % des surdités AR non syndromiques "
            "prélinguales (OMIM, Genetics in Medicine). Les formulations antérieures "
            "« 30-40 % GJB2 » ou « ~1 % OTOF » sont interdites.",
            "**Programmes Pasteur à ce jour** : SENS-501 (OTOF-GT) et SENS-601 (GJB2-GT). "
            "L'accord-cadre prolongé jusqu'au 31/12/2028 laisse la possibilité de programmes "
            "additionnels mais aucune source publique 2025-2026 n'en confirme un troisième actif.",
            "**SENS-501 Cohorte 2** (Audiogene NCT06370351) : 6 patients traités au total "
            "(2 cohortes), 2/3 patients dose haute (4,5×10¹¹ vg/oreille) ont conservé à 6 mois "
            "des gains audiométriques de l'ordre de 60-70 dB HL aux fréquences les plus "
            "performantes (Sensorion PR 23/03/2026). 0 EI grave rapporté.",
        ],
        "garde_fous_hebdo_durcis": HEBDO_DURCIS_DEFAULTS,
    },
    "BE": {
        "garde_fous_structurels": [
            "Bloom Energy = **SOFC haute température** (PAS PEM comme Plug/Ballard, "
            "PAS MCFC comme FuelCell Energy). Toute confusion technologique est interdite.",
            "Société américaine NYSE — **NON éligible PEA-PME**. Aucune routine ne doit "
            "reclasser BE en cadre PEA-PME.",
            "Deal Oracle au 27/04/2026 = **2,8 GW total** (1,2 GW déjà sous contrat) "
            "+ **Project Jupiter 2,45 GW** (BorderPlex, New Mexico) + **warrant Oracle 400 M$** "
            "sur le stock BE (émis 09/04/2026, termes annoncés 30/10/2025).",
            "Deal AEP janvier 2026 = **2,65 Md$ pour 1 GW de SOFC** (~20 ans d'offtake). "
            "Premier déploiement Ohio : site Hilliard 72,9 MW (PUCO 28/05/2025) — "
            "AWS contrat 6 ans, Cologix contrat 15 ans.",
            "Crédit hydrogène 45V **raboté** par la One Big Beautiful Bill Act signée par "
            "Donald Trump le **04/07/2025** (construction obligatoire avant 31/12/2027). "
            "Le 45V reste **exempté des restrictions FEoC** (Baker Botts, K&L Gates). "
            "Le crédit ITC § 48E pour fuel cells reste préservé à 30 % jusqu'à phase-out "
            "à partir de 2034.",
            "Q1 2026 publié **28/04/2026** : revenus **751,1 M$ (+130,4 % YoY)**, "
            "**EPS GAAP dilué 0,23 $** (vs perte 0,10 $) et **EPS non-GAAP 0,44 $**. "
            "Marge brute Q1 GAAP 30,0 %, non-GAAP 31,5 %. Guidance FY2026 relevée à "
            "**3,4-3,8 Md$** (mid 3,6 Md$).",
            "Cours **283,36 $ / capi ~80,6 Md$ au 01/05/2026, +134 % YTD 2026** ; "
            "ratio implicite **~22x mid-guidance FY2026** (calcul transparent capi/guidance).",
            "**Cummins/Accelera NON concurrent SOFC stationnaire data centers** au 02/05/2026 "
            "(revue stratégique nov 2025 + charge non-cash 240 M$ + cession activité fuel cell "
            "rail à Alstom avril 2026). Toute mention future de Cummins comme concurrent SOFC "
            "data centers doit être corroborée par un communiqué primaire 2026+.",
            "**CFO Simon Edwards effectif 13/04/2026** (ex-Groq, en remplacement de Daniel "
            "Berenbaum). KR Sridhar reste fondateur, président du conseil et CEO depuis 2001.",
            "**Bilan Q1 2026** : cash + restreint **2,52 Md$**, dette totale 2,60 Md$, "
            "**dette nette ~80 M$** ; **OCF Q1 2026 +73,6 M$** (vs −110,7 M$ Q1 2025) — "
            "retournement cash structurel. 75 M$ crédits 48C reçus avril 2024 (expansion Fremont).",
            "**Backlog ~20 Md$** (~6 Md$ produit + ~14 Md$ service) = chiffre d'analystes "
            "tier 2 (TIKR, EnkiAI), **NON confirmé par communiqué Bloom officiel**. Toute "
            "mention doit utiliser une attribution prudente jusqu'à confirmation 10-K.",
            "**« 5 GW/an » = vision long terme non datée** (claim management). Seul l'objectif "
            "**2 GW/an d'ici fin 2026** est officiellement daté par Bloom IR.",
        ],
        "garde_fous_hebdo_durcis": HEBDO_DURCIS_DEFAULTS,
    },
}


def _format_audit_rappel(ticker: str) -> tuple[str, str]:
    """Retourne (bloc_structurels, bloc_hebdo_durcis) en Markdown.

    Si le ticker n'a pas de garde-fous, retourne des messages neutres.
    """
    rappels = AUDIT_REFERENCE_RAPPEL.get(ticker, {})
    structurels = rappels.get("garde_fous_structurels", []) if isinstance(rappels, dict) else rappels
    hebdo = rappels.get("garde_fous_hebdo_durcis", []) if isinstance(rappels, dict) else []

    if structurels:
        struct_block = "\n".join(f"- {s}" for s in structurels)
    else:
        struct_block = (
            "_Aucun garde-fou structurel figé pour ce ticker. La routine "
            "doit s'appuyer uniquement sur les sources primaires datées._"
        )

    if hebdo:
        hebdo_block = "\n".join(f"- {h}" for h in hebdo)
    else:
        hebdo_block = (
            "_Aucune règle hebdo durcie spécifique. Appliquer la checklist "
            "T1-T6 et le méta-audit M1-M5 sans contrainte additionnelle._"
        )

    return struct_block, hebdo_block


def build_editorial_dump(editorial: dict[str, Any]) -> str:
    """Produit le Markdown d'input pour la routine ÉDITORIALE hebdomadaire.

    Les garde-fous figés (AUDIT_REFERENCE_RAPPEL) sont injectés UNIQUEMENT
    pour le ticker courant — pas de pollution croisée entre fiches.
    Deux blocs distincts sont produits :
      - garde-fous structurels (faits stables issus de l'audit baseline)
      - garde-fous hebdo durcis (règles procédurales pour les routines)
    """
    nom = editorial.get("nom", "")
    ticker = editorial.get("ticker", "")
    sources = editorial.get("sources", []) or []

    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if sources:
        sources_block = "\n".join(f"- {s}" for s in sources)
    else:
        sources_block = "_Aucune source référencée._"

    struct_block, hebdo_block = _format_audit_rappel(ticker)

    sections = [
        f"# Données pour mise à jour éditoriale — {nom} ({ticker})",
        "",
        f"**Date de génération du dump** : {now_iso}",
        f"**Source** : content/{ticker.split('.')[0]}.yaml (état actuel)",
        "",
        "Ce fichier est l'input de la routine Claude ÉDITORIALE hebdomadaire",
        "(Pattern C+ allégé : sous-agents A et B indépendants + méta-audit C).",
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
        f"## Garde-fous structurels figés pour {ticker}",
        "",
        "Ces faits issus de l'audit baseline + recalibrage Pattern C+ NE",
        "DOIVENT PAS être contredits par une modification future. Toute",
        "modification les touchant est bloquée par R3/R6 du méta-audit C.",
        "",
        struct_block,
        "",
        f"## Garde-fous hebdo durcis pour les routines de {ticker}",
        "",
        "Règles procédurales que les sous-agents A, B et C de la routine",
        "hebdomadaire doivent appliquer à toute modification candidate.",
        "",
        hebdo_block,
        "",
    ]
    return "\n".join(sections)
