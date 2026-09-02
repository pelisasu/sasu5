def volatility_state(atr_value, price):
    ratio = atr_value / price if price else 0
    if ratio < 0.0005:
        return "LOW"
    if ratio > 0.0035:
        return "EXTREME"
    return "NORMAL"
