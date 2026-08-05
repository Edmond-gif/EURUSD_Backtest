Executive Summary
This quantitative data analysis project evaluates the structural behavior, volatility regimes, and directional balance of the EUR/USD forex currency pair across a 5-year period (2021–2025). Operating on a 4-hour (4H) timeframe aggregated from over 1.8 million raw 1-minute tick records, the dataset comprises 8,020 total 4-hour candlestick periods.

The primary objective of this analysis is to determine whether an unfiltered 20 EMA / 50 SMA Moving Average Crossover strategy provides a statistical edge in forex trading. The key findings reveal that directional distribution is almost perfectly symmetric (50.53% Bullish vs. 49.47% Bearish), and intrabar wick noise accounts for over 51% of overall candle movement. Consequently, simple moving average crossovers generate frequent false signals ("whipsaws") during low-volatility or ranging environments. To achieve profitability, the strategy must incorporate a macro trend filter (e.g., 200 SMA) and dynamic volatility-based risk parameters (e.g., ATR-based stop losses).

Annual Market Performance & Volatility Summary
Year	Total 4H Bars	Open Price	High Price	Low Price	Close Price	Avg Range (Pips)	Bullish Bars (%)	Yearly Return (%)
2021	1,604	1.224	1.2349	1.1186	1.1369	23.06 pips	48.88%	-7.12%
2022	1,609	1.1369	1.1495	0.9536	1.0705	37.65 pips	49.29%	-5.84%
2023	1,589	1.0697	1.1276	1.0448	1.1036	26.01 pips	50.79%	+3.17%
2024	1,612	1.1042	1.1214	1.0333	1.0353	21.71 pips	51.24%	-6.24%
2025	1,606	1.035	1.1919	1.0177	1.1746	30.82 pips	52.49%	+13.48%

Methodology
The data engineering pipeline and quantitative workflow were executed in Python using standard data analysis libraries (pandas, numpy, matplotlib, seaborn):Data Ingestion & Cleaning:Ingested 5 yearly 1-minute OHLCV datasets (EURUSD_M1_2021.csv through EURUSD_M1_2025.csv).Removed 240 duplicate timestamp entries to maintain strict chronological integrity.Converted separate date and time columns into unified, timezone-aware UTC datetime objects.Timeframe Aggregation (4-Hour Resampling):Applied pandas continuous temporal resampling (resample('4h')) to aggregate 1-minute data into 4-hour candles.Computed OHLC metrics: $\text{Open} = \text{First}$, $\text{High} = \text{Max}$, $\text{Low} = \text{Min}$, $\text{Close} = \text{Last}$, and $\text{Volume} = \text{Sum}$.Feature Engineering:Derived Candle Range in Pips: $(\text{High} - \text{Low}) \times 10,000$.Derived Candle Body in Pips: $\vert{}\text{Close} - \text{Open}\vert{} \times 10,000$.Derived Percentage Return: $((\text{Close} - \text{Open}) / \text{Open}) \times 100$.Formatted Boolean classification for candle direction (Is_Bullish).

Strategic Recommendations
Incorporate a Trend Filter (200 SMA): Filter out counter-trend crossover entries by requiring long trades to occur strictly above the 200 SMA and short trades below it.

Adopt Dynamic Risk Management (ATR Stop Loss): Implement a dynamic 1.5x Average True Range (ATR) stop-loss model to adjust for expanding volatility regimes (such as 2022’s 37.65 pip average range) versus contracting market regimes (such as 2024’s 21.71 pip average range).

Account for Real-World Friction: Factor in a baseline execution drag of 1.2 pips (spread + slippage) per trade to ensure the strategy maintains positive expectancy during live trading.