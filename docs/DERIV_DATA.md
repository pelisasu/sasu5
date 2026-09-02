# DERIV DATA

Current Deriv market-data integration:
- `active_symbols`
- `ticks_history`
- `ticks`

The client uses the public WebSocket endpoint and does not require a trading token for market-data calls.

The resolver prefers `frxXAUUSD` and checks the current active-symbol response. If exact XAUUSD is unavailable, it fails closed rather than silently substituting another instrument.
