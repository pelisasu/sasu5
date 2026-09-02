from deriv.client import DerivClient
from deriv.instrument import InstrumentResolver
from deriv.data import fetch_closed_candles
from config.settings import SETTINGS

def run_once():
    client = DerivClient()
    
    # Resolusi simbol (bakal mulihkeun frxXAUUSD sacara leres)
    resolver = InstrumentResolver(client)
    symbol_info = resolver.get(SETTINGS.deriv_symbol)
    
    # Tarik data M30 nganggo fungsi data.py anu anyar
    m30df = fetch_closed_candles(client, symbol_info, count=30, granularity=1800)
    
    return f"Berhasil narik data market pikeun: {symbol_info.get('symbol')}"

def main():
    print(run_once())

if __name__ == "__main__":
    main()
