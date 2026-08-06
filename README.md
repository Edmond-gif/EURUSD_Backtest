# 📊 EUR/USD 4-Hour Forex ETL Pipeline & MA Crossover Analysis

An end-to-end quantitative data analysis and ETL framework evaluating the structural behavior, volatility regimes, and directional efficiency of the **EUR/USD** currency pair across a 5-year period (2021–2025). 

This project processes over **1.8 million raw 1-minute tick records** into continuous 4-hour (4H) candlestick data ($n = 8,020$ bars) to rigorously evaluate whether an unfiltered 20 EMA / 50 SMA Moving Average Crossover strategy offers a statistically viable trading edge.

---

## 📁 Repository Structure

```text
EURUSD_Backtest/
│
├── data/
│   ├── raw_data/              # Raw 1-minute OHLCV files (git-ignored)
│   └── cleaned_data/          # Aggregated continuous 4H dataset
│       └── EURUSD_H4_2021_2025_Clean.csv
│
├── scripts/
│   ├── clean_eurusd_data.py   # ETL pipeline for ingestion, deduplication & resampling
│   └── descriptive_analysis.py# Statistical modeling, metrics derivation & visual generation
│
├── visuals/
│   └── eurusd_descriptive_analysis_overview.png
│
├── .gitignore                 # Excludes raw M1 tick datasets from Git tracking
└── README.md                  # Project overview and executive summary

💡 Strategic Takeaways
Macro Trend Filtering: Implement a 200 SMA filter to restrict long entry signals to uptrends and short entry signals to downtrends.

Dynamic Volatility Stops: Use a 1.5x Average True Range (ATR) model to adjust stop-loss parameters dynamic to changing market regimes.

Execution Drag: Factor in a baseline friction cost of 1.2 pips per trade for accurate backtest expectancy modeling.
