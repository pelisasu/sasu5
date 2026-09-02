from .client import DerivClient

class InstrumentResolver:
    def __init__(self, client):
        self.client = client

    def resolve_xauusd(self, preferred="frxXAUUSD"):
        symbols = self.client.active_symbols()
        
        # 1. Cek cocog pas dumasar kana preferred symbol
        for s in symbols:
            sym = str(s.get("symbol", ""))
            underlying = str(s.get("underlying_symbol", ""))
            if preferred.lower() in sym.lower() or preferred.lower() in underlying.lower():
                return s

        # 2. Cek kandidat nu ngandung kecap gold/xau/metal
        candidates = []
        for s in symbols:
            name = str(s.get("display_name", "")).upper()
            sym = str(s.get("symbol", "")).upper()
            underlying = str(s.get("underlying_symbol", "")).upper()
            if any(k in name or k in sym or k in underlying for k in ["XAU", "GOLD", "MET"):
                candidates.append(s)

        if candidates:
            return candidates[0]

        # 3. Lamun tetep teu manggihan, cokot simbol munggaran tina daptar aktif salaku tés atawa tampilkeun sadaya simbol
        all_syms = [s.get("symbol") for s in symbols[:20]] # Témbongkeun 20 simbol pertama
        raise RuntimeError(f"Symbol {preferred} not found. Sample available symbols from server: {', '.join(map(str, all_syms))}")

    def get(self, preferred):
        return self.resolve_xauusd(preferred)
