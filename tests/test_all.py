import pandas as pd
from strategy.indicators import ema, rsi, atr, adx
from strategy.structure import structure_state
from strategy.dynamic_tp import dynamic_levels

def test_math():
    close=[100,101,100.5,102,101.2,103,102.4,104,103.1,105,104.2,106,105.1,107,106.2,108,
           107.0,109,108.1,110,109.0,111,110.2,109.4,111.5,110.3,112.0,111.1,113.2,112.0,
           114.0,113.0,115.1,114.2,116.0,115.0,117.2,116.1,118.0,117.0,119.0,118.1,120.0,
           119.0,121.0,120.1,122.0,121.0,123.0,122.0,124.0,123.0,125.0,124.0,126.0,125.0,
           124.2,126.5,125.3,127.0,126.0,128.0,127.0,129.0,128.0,130.0,129.0,131.0,130.0,
           132.0,131.0,133.0,132.0,134.0,133.0,135.0,134.0,136.0,135.0,137.0,136.0,138.0]
    df=pd.DataFrame({
        "open":[x-0.2 for x in close],
        "high":[x+0.5 for x in close],
        "low":[x-0.5 for x in close],
        "close":close
    })
    assert ema(df.close,20).notna().any()
    assert rsi(df.close).notna().any()
    assert atr(df).notna().any()
    assert adx(df).notna().any()
    assert structure_state(df)["state"] in ("BULLISH","BEARISH","RANGE","NEUTRAL")

def test_tp():
    setup={"price":3000.0,"atr":5.0,"direction":"BUY"}
    levels=dynamic_levels(setup,{"bias":"BULLISH"},0.01,200,2)
    assert levels["tp1_pips"] >= 200
    assert levels["rr_tp1"] >= 2

if __name__=="__main__":
    test_math()
    test_tp()
    print("ALL_TESTS_PASS")
