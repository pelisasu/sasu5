import os
from deriv.client import DerivClient
from deriv.instrument import InstrumentResolver
from deriv.data import fetch_closed_candles
from ai.validator import validate_with_ai
from telegram.notifier import send_telegram, signal_text, error_text
from config.settings import SETTINGS
from strategy.dynamic_tp import dynamic_levels  # Import fungsi dynamic levels yang sudah kita buat

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
        
        # 4. Kalkulasi harga & TP/SL Dinamis Supados Ngajelegur Badag (Minimal 500 pips)
        last_close = m15df[-1].get("close", 0) if m15df else 0
        
        # Simulasi setup objek pikeun dikirim kana dynamic_levels
        # Menggunakan ATR rata-rata atau estimasi volatilitas emas
        dummy_setup = {
            "price": last_close,
            "atr": 15.0,  # Estimasi ATR XAUUSD harian/sesi
            "direction": "BUY" if decision == "APPROVE" else "SELL"
        }
        
        # Panggil fungsi dynamic_levels dengan min_tp_pips 500 & RR 2.5
        pip_size = 0.01  # Ukuran pip untuk XAUUSD
        levels = dynamic_levels(dummy_setup, m30df, pip_size, min_tp_pips=SETTINGS.min_tp_pips, min_rr=SETTINGS.min_rr)
        
        signal_data = {
            "direction": "BUY" if decision == "APPROVE" else "HOLD/REJECT",
            "symbol": symbol_name,
            "entry": levels["entry"],
            "sl": levels["sl"],
            "tp1": levels["tp1"],
            "tp1_pips": levels["tp1_pips"],
            "tp2": levels["tp2"],
            "tp2_pips": levels["tp2_pips"],
            "tp3": levels["tp3"],
            "tp3_pips": levels["tp3_pips"],
            "rr": levels["rr_tp1"],
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
