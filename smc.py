# smc.py

import pandas as pd

def detect_smc_signals(df: pd.DataFrame) -> dict:
    """
    Ανιχνεύει SMC μοτίβα σε δεδομένα candlesticks.
    Περιλαμβάνει BOS, CHoCH, OB, FVG, Sweep, Liquidity Zones.
    """
    signals = {
        "BOS": [],
        "CHoCH": [],
        "OB": [],
        "FVG": [],
        "Sweep": [],
        "LiquidityZones": []
    }

    # Εξετάζουμε τα τελευταία 100 κεριά
    df = df.tail(100).copy()

    for i in range(2, len(df)):
        high = df.iloc[i]["high"]
        low = df.iloc[i]["low"]
        prev_high = df.iloc[i-1]["high"]
        prev_low = df.iloc[i-1]["low"]
        prev_prev_low = df.iloc[i-2]["low"]

        # BOS (Break of Structure)
        if low < prev_low and prev_low > prev_prev_low:
            signals["BOS"].append((i, low))

        # CHoCH
        if high > prev_high and prev_low < prev_prev_low:
            signals["CHoCH"].append((i, high))

        # Sweep
        if high > max(df.iloc[:i]["high"]) or low < min(df.iloc[:i]["low"]):
            signals["Sweep"].append((i, high if high > max(df.iloc[:i]["high"]) else low))

        # Fair Value Gap (FVG)
        if i >= 2:
            prev_close = df.iloc[i-1]["close"]
            prev_open = df.iloc[i-1]["open"]
            if abs(prev_close - prev_open) > 2 * (df.iloc[i]["high"] - df.iloc[i]["low"]) / 100:
                signals["FVG"].append((i, (high + low)/2))

        # Order Block (π.χ. bearish OB = ανοδικό κερί πριν BOS)
        if i >= 2 and df.iloc[i-2]["close"] > df.iloc[i-2]["open"] and low < prev_low:
            signals["OB"].append((i-2, df.iloc[i-2]["low"]))

        # Liquidity Zones (χοντρικά τοπικά highs/lows)
        if i > 5:
            recent_lows = df.iloc[i-5:i]["low"]
            if low == recent_lows.min():
                signals["LiquidityZones"].append((i, low))

    return signals

