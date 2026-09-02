def score_signal(m30, m15, levels):
    score = 0
    reasons = []
    if m30["bias"] in ("BULLISH","BEARISH"):
        score += 25; reasons.append("M30_BIAS")
    if m15["direction"]:
        score += 25; reasons.append("M15_SETUP")
    if "MOMENTUM_CONFIRMATION" in m15["reasons"]:
        score += 15; reasons.append("MOMENTUM")
    if "LIQUIDITY_SWEEP_BULLISH" in m15["reasons"] or "LIQUIDITY_SWEEP_BEARISH" in m15["reasons"]:
        score += 15; reasons.append("LIQUIDITY_SWEEP")
    if m15["adx"] >= 20:
        score += 10; reasons.append("ADX")
    if m15["volatility"] == "NORMAL":
        score += 10; reasons.append("NORMAL_VOLATILITY")
    return min(score,100), reasons
