# ACCURACY CONTROL

The project does not fake a 95% accuracy number.

The 95% figure is a target gate:
- minimum resolved trades: 100
- rolling window: latest 100 resolved trades
- target win rate: 95%
- below target => new signals pause

For a scientifically useful result, maintain:
- out-of-sample backtest
- walk-forward test
- forward demo/paper journal
- MAE/MFE
- profit factor
- expectancy
- max drawdown
- losing streak
- signal count

A confidence score from an AI model is not the same thing as realized trading win rate.
