import requests

def send_telegram(token, chat_id, text):
    if not token or not chat_id:
        return
    url=f"https://api.telegram.org/bot{token}/sendMessage"
    r=requests.post(url,json={"chat_id":chat_id,"text":text},timeout=15)
    r.raise_for_status()

def signal_text(s):
    return (
        f"🟢 XAUUSD VALID SIGNAL\n\n"
        f"Direction: {s['direction']}\n"
        f"Symbol: {s['symbol']}\n"
        f"Price: {s['entry']}\n\n"
        f"SL: {s['sl']}\n"
        f"TP1: {s['tp1']} ({s['tp1_pips']:.0f} pips)\n"
        f"TP2: {s['tp2']} ({s['tp2_pips']:.0f} pips)\n"
        f"TP3: {s['tp3']} ({s['tp3_pips']:.0f} pips)\n"
        f"RR TP1: {s['rr']:.2f}\n\n"
        f"Strategy score: {s['score']:.0f}/100\n"
        f"AI confidence: {s['ai_confidence']:.0f}%\n"
        f"M30: {s['m30_bias']}\n"
        f"M15: {s['m15_setup']}\n"
        f"Reasons: {', '.join(s['reasons'])}\n\n"
        f"⚠️ MANUAL OPEN ONLY"
    )

def error_text(msg):
    return f"🔴 XAUUSD BOT ERROR\n\n{msg}"
