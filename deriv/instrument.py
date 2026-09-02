from .client import DerivClient

class InstrumentResolver:
    def __init__(self, client):
        self.client = client

    def resolve_xauusd(self, preferred="frxXAUUSD"):
        symbols = self.client.active_symbols()
        
        # Cek cocog pas di field 'symbol' atanapi 'underlying_symbol'
        for s in symbols:
            sym = str(s.get("symbol", ""))
            underlying = str(s.get("underlying_symbol", ""))
            if preferred.lower() in sym.lower() or preferred.lower() in underlying.lower():
                return s

        # Alternatif: Cari manual nu ngandung kecap XAU atawa GOLD
        candidates = []
        for s in symbols:
            name = str(s.get("display_name", "")).upper()
            sym = str(s.get("symbol", "")).upper()
            underlying = str(s.get("underlying_symbol", "")).upper()
            if "XAU" in name or "GOLD" in name or "XAU" in sym or "XAU" in underlying:
                candidates.append(s)

        if candidates:
            # Lamun manggihan kandidat, langsung cokot anu munggaran tanpa error
            return candidates[0]

        raise RuntimeError("No XAU/GOLD symbol found in active_symbols.")

    def get(self, preferred):
        return self.resolve_xauusd(preferred)
