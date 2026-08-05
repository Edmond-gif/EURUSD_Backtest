import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_descriptive_analysis(input_file="data/cleaned_data/EURUSD_H4_2021_2025_Clean.csv"):
    # 1. Load Cleaned Dataset
    print(f"Loading cleaned dataset from {input_file}...")
    df = pd.read_csv(input_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year'] = df['timestamp'].dt.year

    # 2. Derive Key Technical Metrics
    df['candle_range_pips'] = (df['high'] - df['low']) * 10000
    df['candle_body_pips'] = (df['close'] - df['open']).abs() * 10000
    df['price_return_pct'] = df['close'].pct_change() * 100
    df['is_bullish'] = df['close'] >= df['open']

    # 3. Compute Summary Statistics
    stats = df[['open', 'high', 'low', 'close', 'candle_range_pips', 'candle_body_pips', 'price_return_pct']].describe().T
    print("\n--- OVERALL DESCRIPTIVE STATS ---")
    print(stats)

    # 4. Compute Yearly Aggregations
    yearly_summary = df.groupby('year').agg(
        total_candles=('timestamp', 'count'),
        start_price=('open', 'first'),
        end_price=('close', 'last'),
        high_price=('high', 'max'),
        low_price=('low', 'min'),
        avg_range_pips=('candle_range_pips', 'mean'),
        max_range_pips=('candle_range_pips', 'max'),
        pct_bullish=('is_bullish', lambda x: (x.sum() / len(x)) * 100)
    ).reset_index()

    yearly_summary['year_return_pct'] = ((yearly_summary['end_price'] - yearly_summary['start_price']) / yearly_summary['start_price']) * 100
    print("\n--- YEARLY PERFORMANCE SUMMARY ---")
    print(yearly_summary)

    # 5. Export Summary CSV Files
    stats.to_csv('EURUSD_4H_Descriptive_Stats.csv')
    yearly_summary.to_csv('EURUSD_4H_Yearly_Summary.csv', index=False)
    print("\nSaved summary stats and yearly performance CSVs.")

    # 6. Generate Overview Charts
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Close Price Trend
    axes[0, 0].plot(df['timestamp'], df['close'], color='#1f77b4', linewidth=1)
    axes[0, 0].set_title('EUR/USD 4H Close Price Trend (2021–2025)', fontweight='bold')
    axes[0, 0].set_ylabel('Exchange Rate (USD per EUR)')

    # Candle Range Distribution
    sns.histplot(df['candle_range_pips'], kde=True, ax=axes[0, 1], color='#ff7f0e', bins=40)
    axes[0, 1].set_title('4H Candlestick Range Distribution (Pips)', fontweight='bold')
    axes[0, 1].set_xlabel('Candle Range (Pips)')

    # Average Range by Year
    sns.barplot(data=yearly_summary, x='year', y='avg_range_pips', ax=axes[1, 0], palette='Blues_d')
    axes[1, 0].set_title('Average 4H Candle Volatility (Pips by Year)', fontweight='bold')
    axes[1, 0].set_xlabel('Year')
    axes[1, 0].set_ylabel('Avg Range (Pips)')

    # Yearly Return Percentage
    sns.barplot(data=yearly_summary, x='year', y='year_return_pct', ax=axes[1, 1], palette='Spectral')
    axes[1, 1].axhline(0, color='black', linestyle='--', linewidth=0.8)
    axes[1, 1].set_title('EUR/USD Yearly Return (%)', fontweight='bold')
    axes[1, 1].set_xlabel('Year')
    axes[1, 1].set_ylabel('Return (%)')

    plt.tight_layout()
    chart_output = 'visuals/eurusd_descriptive_analysis_overview.png'
    plt.savefig('eurusd_descriptive_analysis_overview.png', dpi=300)
    print("Saved visualization chart.")

if __name__ == "__main__":
    perform_descriptive_analysis()
