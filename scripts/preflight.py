from config.settings import SETTINGS
from deriv.client import DerivClient
from deriv.instrument import InstrumentResolver

def main():
    client=DerivClient()
    item=InstrumentResolver(client).get(SETTINGS.deriv_symbol)
    print("DERIV CONNECTION: PASS")
    print("XAUUSD SYMBOL:", item.get("underlying_symbol"))
    print("NAME:", item.get("underlying_symbol_name"))
    print("PIP SIZE:", item.get("pip_size"))

if __name__=="__main__":
    main()
