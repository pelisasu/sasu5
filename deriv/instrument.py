from .client import DerivClient

class InstrumentResolver:
    def __init__(self, client):
        self.client = client

    def resolve_xauusd(self, preferred="frxXAUUSD"):
        symbols = self.client.active_symbols()
        exact = [s for s in symbols if s.get("underlying_symbol") == preferred]
        if exact:
            return exact[0]

        candidates = []
        for s in symbols:
            name = str(s.get("underlying_symbol_name", "")).upper()
            sym = str(s.get("underlying_symbol", "")).upper()
            if "XAU" in name or "GOLD" in name or "XAU" in sym:
                candidates.append(s)

        if candidates:
            raise RuntimeError(
                "Exact XAUUSD symbol not found. Candidates: " +
                ", ".join(str(x.get("underlying_symbol")) for x in candidates)
            )
        raise RuntimeError("No XAU/GOLD symbol found in active_symbols.")

    def get(self, preferred):
        return self.resolve_xauusd(preferred)
