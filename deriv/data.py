from deriv.client import DerivClient

def fetch_closed_candles(client: DerivClient, symbol_obj, count=500, granularity=60):
    """
    Mawa data candles (riwayat harga) ti server Deriv.
    Ngaronjatkeun kasalametan simbol ku cara milih string 'symbol' tina objek,
    atawa ngarobah XAUUSD jadi frxXAUUSD otomatis.
    """
    # Tangkap string simbol tina objek symbol lamun wujudna dikirim salaku dictionary
    if isinstance(symbol_obj, dict):
        symbol_name = symbol_obj.get("symbol", "frxXAUUSD")
    else:
        symbol_name = str(symbol_obj)

    # Antisipasi bilih simbolna masih XAUUSD polos, robah otomatis jadi frxXAUUSD
    if symbol_name.upper() == "XAUUSD":
        symbol_name = "frxXAUUSD"

    resp = client.ticks_history(
        symbol=symbol_name,
        count=count,
        granularity=granularity
    )
    
    # Tarik data candles tina réspon API
    candles = resp.get("candles", [])
    return candles
