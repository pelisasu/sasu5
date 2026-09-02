def dynamic_levels(setup, m30, pip_size, min_tp_pips=200, min_rr=2.0):
    p = setup["price"]
    atr = max(setup["atr"], pip_size)
    min_dist = min_tp_pips * pip_size
    direction = setup["direction"]

    # Conservative dynamic SL based on volatility.
    sl_dist = max(1.15 * atr, min_dist / min_rr)
    tp1_dist = max(min_dist, min_rr * sl_dist)
    tp2_dist = max(tp1_dist * 1.6, min_dist * 2.0)
    tp3_dist = max(tp2_dist * 1.5, min_dist * 3.0)

    if direction == "BUY":
        sl, tp1, tp2, tp3 = p-sl_dist, p+tp1_dist, p+tp2_dist, p+tp3_dist
    else:
        sl, tp1, tp2, tp3 = p+sl_dist, p-tp1_dist, p-tp2_dist, p-tp3_dist

    return {
        "entry": p, "sl": sl, "tp1": tp1, "tp2": tp2, "tp3": tp3,
        "sl_pips": sl_dist/pip_size,
        "tp1_pips": tp1_dist/pip_size,
        "tp2_pips": tp2_dist/pip_size,
        "tp3_pips": tp3_dist/pip_size,
        "rr_tp1": tp1_dist/sl_dist
    }
