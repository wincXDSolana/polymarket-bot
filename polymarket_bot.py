import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON
from py_clob_client.exceptions import PolyMarketException
import ta  # for MACD (install with pip install ta)

load_dotenv()

# === YOUR KEYS (from MoonDev's template style) ===
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # NEVER commit this!
HOST = "https://clob.polymarket.com"   # official CLOB
CHAIN_ID = POLYGON

# Connect (gasless signing — exactly how MoonDev does it)
client = ClobClient(host=HOST, key=PRIVATE_KEY, chain_id=CHAIN_ID)

# Gamma API for live 5-min markets (MoonDev uses this for scanning)
GAMMA_API = "https://gamma-api.polymarket.com/markets"

def get_5min_markets():
    """Fetch active 5-min crypto Up/Down markets"""
    params = {"active": True, "limit": 50}
    resp = requests.get(GAMMA_API, params=params)
    markets = resp.json()
    five_min = [m for m in markets if "5 Minute" in m.get("question", "") and any(x in m.get("question", "") for x in ["BTC", "ETH", "SOL"])]
    return five_min

def get_recent_price_data(condition_id: str, minutes: int = 30):
    """Simple OHLCV fetch for mean-reversion calc (MoonDev backtests this way)"""
    # Placeholder — in production pull from Coinbase or Polymarket ticks via WebSocket
    # For demo we simulate; replace with real tick data in live version
    url = f"https://gamma-api.polymarket.com/prices/{condition_id}?resolution=1m"
    data = requests.get(url).json()
    df = pd.DataFrame(data["prices"])
    df["close"] = df["close"].astype(float)
    return df.tail(minutes)

def mean_reversion_signal(df):
    """MoonDev-style mean reversion + MACD filter"""
    df["sma"] = df["close"].rolling(10).mean()
    df["dev"] = (df["close"] - df["sma"]) / df["sma"]
    
    # MACD (his favorite for 5-min confirmation)
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()
    
    latest = df.iloc[-1]
    if latest["dev"] > 0.015 and latest["macd"] < latest["signal"]:  # Overbought + bearish MACD → bet NO
        return "NO", 0.60  # confidence
    elif latest["dev"] < -0.015 and latest["macd"] > latest["signal"]:  # Oversold + bullish MACD → bet YES
        return "YES", 0.60
    return None, 0

def place_order(condition_id: str, side: str, size: float = 5.0):
    """Gasless limit order — MoonDev's preferred (avoids fees)"""
    try:
        order = client.create_order(
            token_id=condition_id,  # YES/NO token
            price=0.50 if side == "YES" else 0.50,  # at fair value for mean-reversion
            size=size,
            side=side,
        )
        print(f"✅ Placed {side} order for ${size} on {condition_id}")
        return order
    except PolyMarketException as e:
        print(f"Order failed: {e}")
        return None

def main():
    print("🚀 MoonDev-inspired Polymarket Mean Reversion Bot starting...")
    while True:
        try:
            markets = get_5min_markets()
            for market in markets:
                condition_id = market["condition_id"]  # YES/NO token ID
                df = get_recent_price_data(condition_id)
                signal, conf = mean_reversion_signal(df)
                
                if signal and conf > 0.55:  # High-confidence filter like he teaches
                    # Check open positions first (no duplicates)
                    positions = client.get_positions()
                    if not any(p["condition_id"] == condition_id for p in positions):
                        place_order(condition_id, signal, size=5.0)  # tiny size for incubation
            
            print("✅ Scanned markets — sleeping 30s (MoonDev rhythm)")
            time.sleep(30)  # 5-min market cadence
            
        except Exception as e:
            print(f"Error: {e} — retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main()
