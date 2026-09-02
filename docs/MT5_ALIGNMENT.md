# MT5 ALIGNMENT

A GitHub-hosted Python runner cannot directly read the local broker's MT5 terminal.

Therefore:
- Deriv is the authoritative source for this bot.
- `pip_size` is taken from Deriv's instrument metadata.
- Prices are normalized to instrument precision.
- The bot never claims broker MT5 price is identical unless an MT5 bridge supplies that quote.

If exact broker alignment is required, deploy an MT5 Expert Advisor/bridge on the same Windows/VPS machine and send the broker quote to a persistent HTTPS endpoint. Then add a `broker_reference` gate comparing:
`abs(deriv_price - mt5_price) <= allowed_deviation`.
If the deviation is above the configured threshold: NO SIGNAL.
