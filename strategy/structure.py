def swings(df, lookback=2):
    highs, lows = [], []
    for i in range(lookback, len(df)-lookback):
        h = df.iloc[i]["high"]
        l = df.iloc[i]["low"]
        if h == max(df.iloc[i-lookback:i+lookback+1]["high"]):
            highs.append((i, h))
        if l == min(df.iloc[i-lookback:i+lookback+1]["low"]):
            lows.append((i, l))
    return highs, lows

def structure_state(df):
    highs, lows = swings(df)
    if len(highs) < 2 or len(lows) < 2:
        return {"state":"NEUTRAL", "bos":False}
    hh = highs[-1][1] > highs[-2][1]
    hl = lows[-1][1] > lows[-2][1]
    lh = highs[-1][1] < highs[-2][1]
    ll = lows[-1][1] < lows[-2][1]
    if hh and hl:
        return {"state":"BULLISH", "bos": True}
    if lh and ll:
        return {"state":"BEARISH", "bos": True}
    return {"state":"RANGE", "bos":False}
