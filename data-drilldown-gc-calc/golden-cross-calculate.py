import polars as pl

spy_df = pl.scan_csv("SPY_close_price_5Y.csv", try_parse_dates=True)
# print(spy_df.head().collect())

finalspy_df = spy_df.with_columns([
    pl.col("Close").rolling_mean(window_size=50, min_samples=50).alias("ma_50"),
    pl.col("Close").rolling_mean(window_size=200, min_samples=200).alias("ma_200")
]).with_columns([
    ((pl.col("ma_50") > pl.col("ma_200")) & 
     (pl.col("ma_50").shift(1) <= pl.col("ma_200").shift(1))).cast(pl.Int32).alias("gc")
]).filter(pl.col("gc") == 1).collect()

# print(finalspy_df.select(["Date", "Close", "ma_50", "ma_200", "gc"]))
print(finalspy_df)