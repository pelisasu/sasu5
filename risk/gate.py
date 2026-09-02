def hard_gate(m30, m15, levels, score, settings, ai_result):
    if m30["bias"] not in ("BULLISH","BEARISH"):
        return False, "M30_BIAS_INVALID"
    if not m15["direction"]:
        return False, "M15_SETUP_INVALID"
    if score < settings.strategy_score_threshold:
        return False, f"SCORE_BELOW_THRESHOLD:{score:.1f}"
    if levels["tp1_pips"] < settings.min_tp_pips:
        return False, "TP_MINIMUM_NOT_REACHED"
    if levels["rr_tp1"] < settings.min_rr:
        return False, "RR_TOO_LOW"
    if settings.openai_api_key:
        if ai_result["decision"] != "APPROVE":
            return False, "AI_REJECT"
        if ai_result["confidence"] < settings.ai_confidence_threshold:
            return False, "AI_CONFIDENCE_LOW"
    return True, "PASS"
