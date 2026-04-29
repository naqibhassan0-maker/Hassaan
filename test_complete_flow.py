#!/usr/bin/env python3
"""
Integration test to verify the complete price extraction flow works.
Tests with real yfinance data.
"""

import pandas as pd
import yfinance as yf

def test_complete_flow():
    """Test the complete flow with real yfinance data."""
    print("\n" + "="*70)
    print("COMPLETE FLOW TEST - Price Extraction")
    print("="*70)
    
    assets = {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
    }
    
    for name, ticker in assets.items():
        print(f"\nTesting: {name} ({ticker})")
        print("-"*70)
        
        try:
            # Step 1: Download
            print("  1️⃣  Downloading data...")
            data = yf.download(
                ticker, 
                period="5d", 
                interval="15m",
                progress=False
            )
            
            if data is None:
                print("     ❌ Data is None")
                continue
            
            print(f"     ✅ Downloaded {len(data)} candles")
            
            # Step 2: Handle MultiIndex columns
            print("  2️⃣  Handling column structure...")
            if isinstance(data.columns, pd.MultiIndex):
                print(f"     📋 MultiIndex detected: {list(data.columns)[:2]}...")
                data.columns = data.columns.get_level_values(0)
                print(f"     ✅ Flattened to: {list(data.columns)}")
            else:
                print(f"     ℹ️  Regular columns: {list(data.columns)}")
            
            # Step 3: Validate structure
            print("  3️⃣  Validating structure...")
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            has_cols = all(col in data.columns for col in required_cols)
            print(f"     {'✅' if has_cols else '❌'} Has OHLCV: {has_cols}")
            
            if not has_cols:
                print(f"     Available: {list(data.columns)}")
                continue
            
            # Step 4: Extract prices
            print("  4️⃣  Extracting prices...")
            close_series = data['Close']
            print(f"     Type: {type(close_series)}")
            
            close_valid = close_series.dropna()
            print(f"     Valid prices: {len(close_valid)}/{len(close_series)}")
            
            if len(close_valid) < 2:
                print(f"     ❌ Not enough valid prices")
                continue
            
            price = float(close_valid.iloc[-1])
            price_prev = float(close_valid.iloc[-2])
            
            print(f"     ✅ Current price: ${price:.2f}")
            print(f"     ✅ Previous price: ${price_prev:.2f}")
            
            # Step 5: Calculate change
            print("  5️⃣  Calculating change...")
            price_change = price - price_prev
            price_change_pct = (price_change / price_prev) * 100 if price_prev != 0 else 0.0
            
            print(f"     ✅ Change: ${price_change:+.2f} ({price_change_pct:+.2f}%)")
            
            print(f"\n✅ {name} COMPLETE SUCCESS!")
            
        except Exception as e:
            print(f"     ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_complete_flow()
    print("\n" + "="*70 + "\n")
