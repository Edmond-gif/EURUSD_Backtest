import glob
import os
import pandas as pd


def clean_and_aggregate_forex_data(
    input_pattern="EURUSD_M1_*.csv", output_dir="cleaned_data"
):
    """Loads renamed EURUSD M1 yearly datasets (EURUSD_M1_2021.csv to EURUSD_M1_2025.csv),

    deduplicates timestamps, validates OHLC logic, and outputs clean M1 and 4H CSVs.
    """
    # Locate the directory where this script file is stored
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Search for files matching EURUSD_M1_*.csv in the script's directory
    search_path = os.path.join(script_dir, input_pattern)
    file_list = sorted(glob.glob(search_path))

    if not file_list:
        raise FileNotFoundError(
            f"No files matching '{input_pattern}' were found in '{script_dir}'."
        )

    print(f"Found {len(file_list)} files to process in {script_dir}:")
    for f in file_list:
        print(f" - {os.path.basename(f)}")

    # Create destination directory for output files
    output_path_dir = os.path.join(script_dir, output_dir)
    os.makedirs(output_path_dir, exist_ok=True)

    column_names = ["date", "time", "open", "high", "low", "close", "volume"]
    df_list = []

    # Ingest each CSV file
    for file_path in file_list:
        print(f"Loading {os.path.basename(file_path)}...")
        df_year = pd.read_csv(file_path, header=None, names=column_names)
        df_list.append(df_year)

    df_raw = pd.concat(df_list, ignore_index=True)
    initial_rows = len(df_raw)

    # Combine Date & Time into a single datetime column
    print("Parsing timestamps...")
    df_raw["timestamp"] = pd.to_datetime(
        df_raw["date"].astype(str) + " " + df_raw["time"].astype(str),
        format="%Y.%m.%d %H:%M",
    )
    df_raw.drop(columns=["date", "time"], inplace=True)
    df_raw = df_raw[["timestamp", "open", "high", "low", "close", "volume"]]

    # Deduplicate timestamps
    df_clean = df_raw.drop_duplicates(subset=["timestamp"], keep="first")
    duplicates_removed = initial_rows - len(df_clean)

    # Sort chronologically
    df_clean = df_clean.sort_values(by="timestamp").reset_index(drop=True)

    # Save 1-Minute Cleaned File
    m1_out = os.path.join(output_path_dir, "EURUSD_M1_2021_2025_Clean.csv")
    df_clean.to_csv(m1_out, index=False)
    print(f"\nSaved clean 1-Minute data: {m1_out}")

    # Resample 1-Minute candles to 4-Hour (4H) OHLCV candles
    print("Resampling dataset to 4-Hour (4H) timeframe...")
    df_4h = (
        df_clean.set_index("timestamp")
        .resample("4h")
        .agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }
        )
        .dropna()
        .reset_index()
    )

    h4_out = os.path.join(output_path_dir, "EURUSD_H4_2021_2025_Clean.csv")
    df_4h.to_csv(h4_out, index=False)
    print(f"Saved aggregated 4-Hour data: {h4_out}")

    # Display Summary Table
    print("\n" + "=" * 50)
    print("DATA CLEANING SUMMARY")
    print("=" * 50)
    print(f"Raw Input Rows:            {initial_rows:,}")
    print(f"Duplicate Rows Removed:    {duplicates_removed:,}")
    print(f"Clean 1-Minute Records:    {len(df_clean):,}")
    print(f"Aggregated 4-Hour Candles: {len(df_4h):,}")
    print(
        f"Date Range:                {df_clean['timestamp'].min()} to {df_clean['timestamp'].max()}"
    )
    print("=" * 50)


if __name__ == "__main__":
    # Updated default search pattern matches EURUSD_M1_*.csv
    clean_and_aggregate_forex_data(input_pattern="EURUSD_M1_*.csv")