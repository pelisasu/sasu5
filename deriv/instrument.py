from .client import DerivClient

class InstrumentResolver:
    def __init__(self, client):
        self.client = client

    def resolve_xauusd(self, preferred="frxXAUUSD"):
        symbols = self.client.active_symbols()
        
        # Lamun server mulihkeun daptar simbol, saring sapertos biasana
        if symbols:
            for s in symbols:
                sym = str(s.get("symbol", ""))
                underlying = str(s.get("underlying_symbol", ""))
                if preferred.lower() in sym.lower() or preferred.lower() in underlying.lower():
                    return s

            for s in symbols:
                name = str(s.get("display_name", "")).upper()
                sym = str(s.get("symbol", "")).upper()
                underlying = str(s.get("underlying_symbol", "")).upper()
                if any(k in name or k in sym or k in underlying for k in ["XAU", "GOLD", "MET"]):
                    return s
            
            # Lamun teu kapanggih tapi aya simbol, pulihkeun simbol munggaran
            return symbols[0]

        # Cadangan bener-bener kosong: balikkeun objek simbol manual pikeun frxXAUUSD
        return {
            "symbol": preferred,
            "display_name": "Gold vs US Dollar",
            "underlying_symbol": "XAUUSD"
        }

    def get(self, preferred):
        return self.resolve_xauusd(preferred)
