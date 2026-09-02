import pandas as pd
import time

def candles_to_df(response):
    candles = response.get("candles") or []
    if not candles:
        raise RuntimeError("No candles returned.")
    rows = []
    for c in candles:
        rows.append({
            "time": pd.to_datetime(int(c["epoch"]), unit="s", utc=True),
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"]),
        })
    df = pd.DataFrame(rows).sort_values("time").drop_duplicates("time")
    return df.reset_index(drop=True)

def fetch_closed_candles(client, symbol, minutes, count):
    resp = client.ticks_history(
        symbol,
        count=count,
        granularity=minutes * 60
    )
    df = candles_to_df(resp)
    # Remove current/incomplete candle based on epoch boundary.
    now = int(time.time())
    period = minutes * 60
    current_bucket = now - (now % period)
    return df[df["time"].astype("int64") // 10**9 < current_bucket].copy()
