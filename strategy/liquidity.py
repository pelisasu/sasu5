def liquidity_sweep(df, lookback=20):
    if len(df) < lookback + 2:
        return {"bullish":False, "bearish":False}
    prior = df.iloc[-lookback-1:-1]
    last = df.iloc[-1]
    prev_low = float(prior["low"].min())
    prev_high = float(prior["high"].max())
    bullish = last["low"] < prev_low and last["close"] > prev_low
    bearish = last["high"] > prev_high and last["close"] < prev_high
    return {"bullish":bool(bullish), "bearish":bool(bearish)}
