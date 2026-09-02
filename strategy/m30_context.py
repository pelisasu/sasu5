from .indicators import ema, rsi, atr, adx
from .structure import structure_state
from .volatility import volatility_state

def analyze_m30(df):
    x = df.copy()
    x["ema20"] = ema(x["close"],20)
    x["ema50"] = ema(x["close"],50)
    x["rsi"] = rsi(x["close"])
    x["atr"] = atr(x)
    x["adx"] = adx(x)
    st = structure_state(x)
    price = float(x["close"].iloc[-1])
    trend = "BULLISH" if price > x["ema20"].iloc[-1] > x["ema50"].iloc[-1] else \
            "BEARISH" if price < x["ema20"].iloc[-1] < x["ema50"].iloc[-1] else "NEUTRAL"
    if trend == "BULLISH" and st["state"] == "BULLISH":
        bias = "BULLISH"
    elif trend == "BEARISH" and st["state"] == "BEARISH":
        bias = "BEARISH"
    else:
        bias = "NEUTRAL"
    return {
        "bias": bias, "trend": trend, "structure": st["state"],
        "rsi": float(x["rsi"].iloc[-1]), "atr": float(x["atr"].iloc[-1]),
        "adx": float(x["adx"].iloc[-1]), "volatility": volatility_state(float(x["atr"].iloc[-1]), price),
        "price": price
    }
