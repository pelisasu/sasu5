from .indicators import ema, rsi, atr, adx
from .structure import structure_state
from .liquidity import liquidity_sweep
from .volatility import volatility_state

def analyze_m15(df, m30):
    x = df.copy()
    x["ema20"] = ema(x["close"],20)
    x["ema50"] = ema(x["close"],50)
    x["rsi"] = rsi(x["close"])
    x["atr"] = atr(x)
    x["adx"] = adx(x)
    st = structure_state(x)
    liq = liquidity_sweep(x)
    p = float(x["close"].iloc[-1])
    direction = None
    reasons = []
    if m30["bias"] == "BULLISH":
        if st["state"] == "BULLISH" and (liq["bullish"] or p > x["ema20"].iloc[-1]):
            direction = "BUY"
            reasons += ["M30_BULLISH","M15_STRUCTURE_BULLISH"]
            if liq["bullish"]: reasons.append("LIQUIDITY_SWEEP_BULLISH")
    elif m30["bias"] == "BEARISH":
        if st["state"] == "BEARISH" and (liq["bearish"] or p < x["ema20"].iloc[-1]):
            direction = "SELL"
            reasons += ["M30_BEARISH","M15_STRUCTURE_BEARISH"]
            if liq["bearish"]: reasons.append("LIQUIDITY_SWEEP_BEARISH")

    r = float(x["rsi"].iloc[-1])
    adxv = float(x["adx"].iloc[-1])
    if direction == "BUY" and r >= 50: reasons.append("MOMENTUM_CONFIRMATION")
    if direction == "SELL" and r <= 50: reasons.append("MOMENTUM_CONFIRMATION")
    if adxv >= 20: reasons.append("ADX_SUPPORT")

    return {
        "direction": direction,
        "price": p,
        "atr": float(x["atr"].iloc[-1]),
        "rsi": r,
        "adx": adxv,
        "structure": st["state"],
        "liquidity": liq,
        "volatility": volatility_state(float(x["atr"].iloc[-1]), p),
        "reasons": reasons
    }
