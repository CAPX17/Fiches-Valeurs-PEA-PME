"""Indicateurs techniques calculés à partir de l'historique de cours.

Tout calcul retournant NaN ou non calculable renvoie None pour que le
renderer affiche 'n/d'. Aucune valeur n'est extrapolée.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

import pandas as pd

try:
    import pandas_ta as ta  # type: ignore
    _HAS_PANDAS_TA = True
except Exception:  # noqa: BLE001
    _HAS_PANDAS_TA = False

logger = logging.getLogger(__name__)

FIBO_LEVELS = (0.0, 0.236, 0.382, 0.5, 0.618, 1.0)


@dataclass
class FiboLevel:
    ratio: float
    price: float
    distance_pct: float
    status: str  # 'support' | 'resistance' | 'current'


@dataclass
class Indicators:
    rsi_14: float | None = None
    rsi_zone: str | None = None  # 'survente' | 'neutre' | 'surachat'
    macd: float | None = None
    macd_signal: float | None = None
    macd_trend: str | None = None  # 'haussier' | 'baissier' | None
    ma_50: float | None = None
    ma_200: float | None = None
    fibonacci: list[FiboLevel] = field(default_factory=list)
    range_position_pct: float | None = None  # 0..100, position dans 52w


def _safe_last(series: pd.Series) -> float | None:
    if series is None or series.empty:
        return None
    val = series.dropna()
    if val.empty:
        return None
    v = float(val.iloc[-1])
    if pd.isna(v):
        return None
    return v


def _rsi_fallback(close: pd.Series, length: int = 14) -> pd.Series:
    """RSI de Wilder en fallback pandas pur (compatible pandas_ta).

    Formule Wilder récursive :
        avg_gain_t = (avg_gain_{t-1} * (N-1) + gain_t) / N
        avg_gain_t = (1 - 1/N) * avg_gain_{t-1} + (1/N) * gain_t

    pandas .ewm(alpha=1/N, adjust=False) implémente exactement cette
    récurrence. Ce N'EST PAS un EMA standard (qui utiliserait alpha =
    2/(N+1) = 2/15 pour span=14). Le warm-up des 14 premières barres
    diffère légèrement du Wilder textbook (qui seed via moyenne simple),
    écart négligeable après ~50 périodes ; identique au comportement
    de pandas_ta.rsi().
    """
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / length, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def _macd_fallback(close: pd.Series) -> tuple[pd.Series, pd.Series]:
    """MACD(12,26,9) en fallback."""
    ema_fast = close.ewm(span=12, adjust=False).mean()
    ema_slow = close.ewm(span=26, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal


def compute_indicators(
    history_1y: pd.DataFrame,
    current_price: float | None,
    high_52w: float | None,
    low_52w: float | None,
) -> Indicators:
    """Calcule l'ensemble des indicateurs techniques."""
    out = Indicators()

    if history_1y is None or history_1y.empty or "Close" not in history_1y.columns:
        logger.warning("history_1y vide, indicateurs non calculables")
        out.fibonacci = _compute_fibo(low_52w, high_52w, current_price)
        out.range_position_pct = _range_position(current_price, low_52w, high_52w)
        return out

    close = history_1y["Close"].dropna()
    if close.empty:
        return out

    # RSI(14)
    try:
        if _HAS_PANDAS_TA:
            rsi = ta.rsi(close, length=14)
        else:
            rsi = _rsi_fallback(close, length=14)
        out.rsi_14 = _safe_last(rsi)
    except Exception as exc:  # noqa: BLE001
        logger.warning("RSI calc failed: %s", exc)

    if out.rsi_14 is not None:
        if out.rsi_14 < 30:
            out.rsi_zone = "survente"
        elif out.rsi_14 > 70:
            out.rsi_zone = "surachat"
        else:
            out.rsi_zone = "neutre"

    # MACD(12,26,9)
    try:
        if _HAS_PANDAS_TA:
            macd_df = ta.macd(close, fast=12, slow=26, signal=9)
            if macd_df is not None and not macd_df.empty:
                out.macd = _safe_last(macd_df.iloc[:, 0])
                out.macd_signal = _safe_last(macd_df.iloc[:, 2])
        else:
            macd_s, sig_s = _macd_fallback(close)
            out.macd = _safe_last(macd_s)
            out.macd_signal = _safe_last(sig_s)
    except Exception as exc:  # noqa: BLE001
        logger.warning("MACD calc failed: %s", exc)

    if out.macd is not None and out.macd_signal is not None:
        out.macd_trend = "haussier" if out.macd >= out.macd_signal else "baissier"

    # Moyennes mobiles
    if len(close) >= 50:
        out.ma_50 = _safe_last(close.rolling(50).mean())
    if len(close) >= 200:
        out.ma_200 = _safe_last(close.rolling(200).mean())

    # Fibonacci sur range 52w
    out.fibonacci = _compute_fibo(low_52w, high_52w, current_price)
    out.range_position_pct = _range_position(current_price, low_52w, high_52w)

    return out


def _compute_fibo(
    low: float | None,
    high: float | None,
    current: float | None,
) -> list[FiboLevel]:
    """Calcule les 6 niveaux Fibonacci sur le range [low, high]."""
    if low is None or high is None or high <= low:
        return []

    span = high - low
    levels: list[FiboLevel] = []

    # Quel niveau est le plus proche du cours actuel ?
    if current is not None:
        prices = [low + r * span for r in FIBO_LEVELS]
        nearest_idx = min(range(len(prices)), key=lambda i: abs(prices[i] - current))
    else:
        nearest_idx = -1

    for i, ratio in enumerate(FIBO_LEVELS):
        price = low + ratio * span
        distance = ((price - current) / current * 100) if current not in (None, 0) else 0.0
        if i == nearest_idx:
            status = "current"
        elif current is not None and price < current:
            status = "support"
        else:
            status = "resistance"
        levels.append(
            FiboLevel(
                ratio=ratio,
                price=price,
                distance_pct=distance,
                status=status,
            )
        )
    return levels


def _range_position(
    current: float | None,
    low: float | None,
    high: float | None,
) -> float | None:
    """Position du cours dans la range 52w en pourcentage 0-100."""
    if current is None or low is None or high is None or high <= low:
        return None
    pct = (current - low) / (high - low) * 100
    return max(0.0, min(100.0, pct))
