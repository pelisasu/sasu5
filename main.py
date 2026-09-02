import os
from deriv.client import DerivClient
from deriv.instrument import InstrumentResolver
from deriv.data import fetch_closed_candles
from ai.validator import validate_with_ai
from telegram.notifier import send_telegram, signal_text, error_text
from config.settings import SETTINGS

def run_once():
    try:
        client = DerivClient()
        
        # 1. Resolusi simbol supaya bener jadi frxXAUUSD
        resolver = InstrumentResolver(client)
        symbol_info = resolver.get(SETTINGS.deriv_symbol)
        symbol_name = symbol_info.get("symbol", "frxXAUUSD")
        
        # 2. Tarik data candles M30 jeung M15
        m30df = fetch_closed_candles(client, symbol_info, count=50, granularity=1800)
        m15df = fetch_closed_candles(client, symbol_info, count=50, granularity=900)
        
        # Bungkus data kana payload pikeun AI Validator
        payload = {
            "symbol": symbol_name,
            "m30_candles_count": len(m30df),
            "m15_candles_count": len(m15df),
            "candles_m30": m30df[-5:], 
            "candles_m15": m15df[-5:]
        }
        
        # 3. Validasi sinyal ngagunakeun AI (Gemini)
        ai_client = None 
        model_name = getattr(SETTINGS, "openai_model", "gpt-5.6-luna")
        
        validation_result = validate_with_ai(ai_client, model_name, payload)
        
        decision = validation_result.get("decision", "REJECT")
        confidence = validation_result.get("confidence", 0)
        reasons = validation_result.get("reasons", [])
        
        # 4. Jieun struktur data sinyal luyu jeung format ti notifier.py
        # Candak harga panungtung tina data m15 bilih peryogi, atawa estimasi saderhana
        last_close = m15df[-1].get("close", 0) if m15df else 0
        
        signal_data = {
            "direction": "BUY" if decision == "APPROVE" else "HOLD/REJECT",
            "symbol": symbol_name,
            "entry": last_close,
            "sl": last_close - 5.0,  # Conto SL
            "tp1": last_close + 5.0,
            "tp1_pips": 50,
            "tp2": last_close + 10.0,
            "tp2_pips": 100,
            "tp3": last_close + 15.0,
            "tp3_pips": 150,
            "rr": 1.5,
            "score": 75.0,
            "ai_confidence": confidence,
            "m30_bias": "Bullish",
            "m15_setup": "Valid Setup",
            "reasons": reasons if reasons else ["AI Approved signal validation"]
        }
        
        # 5. Kirim ka Telegram gumantung kana putusan (APPROVE / REJECT)
        token = getattr(SETTINGS, "telegram_bot_token", None) or os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = getattr(SETTINGS, "telegram_chat_id", None) or os.getenv("TELEGRAM_CHAT_ID")
        
        if decision == "APPROVE":
            message = signal_text(signal_data)
        else:
            message = error_text(f"Analisa ditolak (REJECT). Alesan: {', '.join(reasons)}")
            
        print(message)
        send_telegram(token, chat_id, message)
        return message

    except Exception as e:
        err_msg = f"Kasalahan dina bot run_once: {str(e)}"
        print(err_msg)
        token = getattr(SETTINGS, "telegram_bot_token", None) or os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = getattr(SETTINGS, "telegram_chat_id", None) or os.getenv("TELEGRAM_CHAT_ID")
        try:
            send_telegram(token, chat_id, error_text(err_msg))
        except:
            pass
        raise e

def main():
    run_once()

if __name__ == "__main__":
    main()
