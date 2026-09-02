import argparse, traceback
from config.settings import SETTINGS
from deriv.client import DerivClient
from deriv.instrument import InstrumentResolver
from deriv.data import fetch_closed_candles
from strategy.m30_context import analyze_m30
from strategy.m15_setup import analyze_m15
from strategy.dynamic_tp import dynamic_levels
from strategy.scoring import score_signal
from risk.gate import hard_gate
from risk.performance import performance_gate
from telegram.notifier import send_telegram, signal_text, error_text
from telegram.anti_spam import allow
from database.journal import log_event

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

def run_once():
    if not SETTINGS.telegram_bot_token or not SETTINGS.telegram_chat_id:
        # Do not stop analysis; only notification is disabled.
        pass

    client=DerivClient()
    instrument=InstrumentResolver(client).get(SETTINGS.deriv_symbol)
    symbol=instrument["underlying_symbol"]
    pip_size=float(instrument.get("pip_size") or 0.01)

    m30df=fetch_closed_candles(client,symbol,30,SETTINGS.lookback_m30)
    m15df=fetch_closed_candles(client,symbol,15,SETTINGS.lookback_m15)
    if len(m30df)<100 or len(m15df)<100:
        raise RuntimeError("Insufficient closed candles.")

    m30=analyze_m30(m30df)
    m15=analyze_m15(m15df,m30)

    if not m15["direction"]:
        return {"status":"NO_SIGNAL","reason":"NO_VALID_M15_SETUP"}

    levels=dynamic_levels(m15,m30,pip_size,SETTINGS.min_tp_pips,SETTINGS.min_rr)
    score,reasons=score_signal(m30,m15,levels)

    ai_result={"decision":"REJECT","confidence":0,"reasons":[]}
    if SETTINGS.openai_api_key and OpenAI:
        ai=OpenAI(api_key=SETTINGS.openai_api_key)
        ai_payload={"symbol":symbol,"pip_size":pip_size,"m30":m30,"m15":m15,"levels":levels,"score":score,"reasons":reasons}
        from ai.validator import validate_with_ai
        ai_result=validate_with_ai(ai,SETTINGS.openai_model,ai_payload)

    perf_ok,perf_msg=performance_gate(SETTINGS)
    if not perf_ok:
        return {"status":"PAUSED","reason":perf_msg}

    ok,gate_reason=hard_gate(m30,m15,levels,score,SETTINGS,ai_result)
    if not ok:
        return {"status":"NO_SIGNAL","reason":gate_reason}

    signal={
        "symbol":symbol,"direction":m15["direction"],
        "entry":round(levels["entry"],8),"sl":round(levels["sl"],8),
        "tp1":round(levels["tp1"],8),"tp2":round(levels["tp2"],8),"tp3":round(levels["tp3"],8),
        "tp1_pips":levels["tp1_pips"],"tp2_pips":levels["tp2_pips"],"tp3_pips":levels["tp3_pips"],
        "rr":levels["rr_tp1"],"score":score,
        "ai_confidence":ai_result["confidence"],
        "m30_bias":m30["bias"],"m15_setup":m15["structure"],
        "reasons":reasons + ai_result.get("reasons",[])
    }

    allowed,fp=allow(signal,SETTINGS.cooldown_minutes*60)
    if not allowed:
        return {"status":"NO_SIGNAL","reason":"DUPLICATE_OR_COOLDOWN","fingerprint":fp}

    log_event({"type":"SIGNAL","result":"PENDING","fingerprint":fp,**signal})
    send_telegram(SETTINGS.telegram_bot_token,SETTINGS.telegram_chat_id,signal_text(signal))
    return {"status":"SIGNAL_SENT","fingerprint":fp,**signal}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--once",action="store_true")
    args=p.parse_args()
    try:
        print(run_once())
    except Exception as e:
        msg=f"{type(e).__name__}: {e}"
        print(msg)
        try:
            send_telegram(SETTINGS.telegram_bot_token,SETTINGS.telegram_chat_id,error_text(msg))
        except Exception:
            pass
        raise

if __name__=="__main__":
    main()
