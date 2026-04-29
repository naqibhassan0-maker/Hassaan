#!/usr/bin/env python3
"""
Diagnostic script to test yfinance data retrieval and structure.
Helps identify why price extraction is failing.
"""

import yfinance as yf
import pandas as pd

def test_yfinance_download():
    """Test yfinance download for different assets."""
    print("\n" + "="*70)
    print("YFINANCE DATA STRUCTURE DIAGNOSTIC")
    print("="*70)
    
    assets = {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Gold": "GC=F",
        "S&P 500": "^GSPC",
        "EUR/USD": "EURUSD=X",
    }
    
    for name, ticker in assets.items():
        print(f"\n{'='*70}")
        print(f"Testing: {name} ({ticker})")
        print("="*70)
        
        try:
            # Try downloading with different timeframes
            for timeframe in ["15m", "1h", "1d"]:
                print(f"\n  Timeframe: {timeframe}")
                
                period_map = {"15m": "5d", "1h": "30d", "1d": "1y"}
                
                try:
                    data = yf.download(
                        ticker, 
                        period=period_map.get(timeframe, "5d"), 
                        interval=timeframe,
                        progress=False
                    )
                    
                    if data is None:
                        print(f"    ❌ Data is None")
                        continue
                    
                    print(f"    ✅ Data retrieved")
                    print(f"       Type: {type(data)}")
                    print(f"       Shape: {data.shape}")
                    print(f"       Index type: {type(data.index)}")
                    print(f"       Columns: {list(data.columns)}")
                    print(f"       Empty: {data.empty}")
                    
                    if not data.empty and len(data) > 0:
                        print(f"\n       Last 3 rows:")
                        print(f"       {data.tail(3).to_string()}")
                        
                        # Try extracting prices
                        try:
                            close_series = data['Close']
                            print(f"\n       Close series type: {type(close_series)}")
                            print(f"       Close series length: {len(close_series)}")
                            print(f"       Last Close value: {close_series.iloc[-1]}")
                            print(f"       Last Close type: {type(close_series.iloc[-1])}")
                            
                            # Try with dropna
                            close_valid = close_series.dropna()
                            print(f"       Valid prices after dropna: {len(close_valid)}")
                            if len(close_valid) >= 2:
                                print(f"       ✅ Can extract price: {float(close_valid.iloc[-1])}")
                            else:
                                print(f"       ❌ Not enough valid prices")
                        except Exception as e:
                            print(f"       ❌ Price extraction error: {e}")
                    else:
                        print(f"    ❌ No data in returned DataFrame")
                    
                    break  # Only test first successful timeframe
                    
                except Exception as e:
                    print(f"    ❌ Error: {str(e)[:80]}")
        
        except Exception as e:
            print(f"  ❌ Asset error: {str(e)}")

def main():
    print("Testing yfinance data retrieval...")
    test_yfinance_download()
    print("\n" + "="*70)
    print("Diagnostic complete!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
