import os
from deriv.client import DerivClient
from deriv.instrument import InstrumentResolver
from deriv.data import fetch_closed_candles
from ai.validator import validate_with_ai
from config.settings import SETTINGS

def run_once():
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
        "candles_m30": m30df[-5:], # Candles terakhir pikeun acuan
        "candles_m15": m15df[-5:]
    }
    
    # 3. Validasi sinyal ngagunakeun AI (Gemini)
    # Catetan: Pastikeun client AI diatur atanapi diset luyu jeung konfigurasi proyék anjeun
    ai_client = None # Upama nganggo client khusus, sambungkeun ka dieu
    model_name = getattr(SETTINGS, "openai_model", "gpt-5.6-luna")
    
    validation_result = validate_with_ai(ai_client, model_name, payload)
    
    decision = validation_result.get("decision", "REJECT")
    confidence = validation_result.get("confidence", 0)
    reasons = validation_result.get("reasons", [])
    
    result_msg = (
        f"📊 **XAUUSD Signal Analysis**\n"
        f"Symbol: {symbol_name}\n"
        f"Decision: **{decision}** (Confidence: {confidence}%)\n"
        f"Reasons: {', '.join(reasons)}"
    )
    
    # 4. Kirim Notifikasi ka Telegram upama disatujuan (APPROVE) atanapi dicetak
    # (Logika pengiriman telegram tiasa diintegrasikeun langsung ka dieu)
    print(result_msg)
    return result_msg

def main():
    run_once()

if __name__ == "__main__":
    main()
