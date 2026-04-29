import sys

# Verify all imports are available
try:
    import streamlit as st
    import streamlit.components.v1 as components
    import yfinance as yf
    import pandas as pd
    from datetime import datetime, timedelta
except ImportError as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    print("\n📦 Missing dependency detected. Please run:")
    print("   python3 start.py")
    print("\n   Or manually install:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

st.set_page_config(
    page_title="Smart Money Concepts Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📈 Smart Money Concepts Dashboard")
st.caption("Executive summary, signal framework, and live institutional signals overlay.")

page = st.sidebar.radio(
    "Navigation",
    [
        "Live Signals",
        "Executive Summary",
        "Top 20 Signals",
        "Signal Details",
        "Data Sources",
        "Risk & Execution",
        "Deployment Notes",
    ],
)

# ============================================================================
# SMC Analysis Functions
# ============================================================================

def analyze_smc(df):
    """
    Detect SMC signal patterns from OHLC data.
    Returns: (signal_text, signal_strength, score)
    """
    try:
        # Validate data
        if df is None or df.empty or len(df) < 3:
            return "INSUFFICIENT DATA", "Neutral", 0
        
        # Handle MultiIndex columns from yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df = df.copy()
            df.columns = df.columns.get_level_values(0)
        
        # Ensure we have the required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
            return "INVALID DATA FORMAT", "Neutral", 0
        
        score = 0
        signals = []
        bullish_fvg = False
        bearish_fvg = False
        
        # Get scalar values safely
        try:
            current_close = float(df['Close'].iloc[-1])
            current_volume = float(df['Volume'].iloc[-1])
        except (IndexError, TypeError, ValueError):
            return "DATA ERROR", "Neutral", 0
        
        # 1. Fair Value Gap (FVG) / Imbalance Detection
        if len(df) >= 2:
            try:
                curr_low = float(df['Low'].iloc[-1])
                curr_high = float(df['High'].iloc[-1])
                prev_high = float(df['High'].iloc[-2])
                prev_low = float(df['Low'].iloc[-2])
                
                # Bullish FVG: current Low > previous High (gap up)
                bullish_fvg = curr_low > prev_high
                # Bearish FVG: current High < previous Low (gap down)
                bearish_fvg = curr_high < prev_low
                
                if bullish_fvg:
                    signals.append("Bullish FVG")
                    score += 15
                elif bearish_fvg:
                    signals.append("Bearish FVG")
                    score += 15
            except (IndexError, TypeError, ValueError):
                pass
        
        # 2. Market Structure Shift (Break of Structure / BOS)
        try:
            lookback = min(20, len(df))
            last_high = float(df['High'].iloc[-lookback:-1].max())
            last_low = float(df['Low'].iloc[-lookback:-1].min())
            current_price = float(df['Close'].iloc[-1])
            
            if current_price > last_high:
                signals.append("Bullish BOS")
                score += 20
            elif current_price < last_low:
                signals.append("Bearish BOS")
                score += 20
        except (IndexError, TypeError, ValueError):
            current_price = current_close
            last_high = current_price
            last_low = current_price
        
        # 3. Volume Analysis (Simple: compare recent volume to average)
        if len(df) >= 5:
            try:
                avg_volume = float(df['Volume'].iloc[-5:-1].mean())
                if current_volume > avg_volume * 1.5:
                    signals.append("Volume Spike")
                    score += 10
            except (IndexError, TypeError, ValueError):
                pass
        
        # 4. Confluence Signal: Unicorn Setup (FVG + BOS Alignment)
        bullish_confluence = False
        bearish_confluence = False
        
        try:
            bullish_confluence = bullish_fvg and (current_price > last_low)
            bearish_confluence = bearish_fvg and (current_price < last_high)
            
            if bullish_confluence:
                signals.append("⭐ UNICORN (Bullish Setup)")
                score += 25
            elif bearish_confluence:
                signals.append("⭐ UNICORN (Bearish Setup)")
                score += 25
        except (TypeError, ValueError):
            pass
        
        # Determine overall signal
        if score >= 40:
            if bullish_confluence or (bullish_fvg and current_price > last_low):
                signal_text = "🟢 BUY (Unicorn Entry / OB Confluence)"
                strength = "Strong Bullish"
            elif bearish_confluence or (bearish_fvg and current_price < last_high):
                signal_text = "🔴 SELL (Institutional Supply)"
                strength = "Strong Bearish"
            else:
                signal_text = f"📊 MOMENTUM ({', '.join(signals)})"
                strength = "Bullish" if score > 0 else "Bearish"
        elif score >= 20:
            signal_text = f"⚠️  ACTIVE SETUP ({', '.join(signals[-2:] if len(signals) > 1 else signals)})"
            strength = "Moderate" + (" Bullish" if signals and "Bullish" in signals[0] else " Bearish")
        else:
            signal_text = "⏳ NEUTRAL / MONITORING"
            strength = "Neutral"
        
        return signal_text, strength, score
    
    except Exception as e:
        return f"ANALYSIS ERROR: {str(e)[:50]}", "Neutral", 0


if page == "Live Signals":
    st.header("📡 Live SMC Signals")
    st.markdown("Real-time Smart Money Concepts signal detection for major assets.")

    auto_refresh = st.checkbox(
        "Auto-refresh every 5 seconds",
        value=True,
        help="Automatically reload this live signal view every 5 seconds.",
    )

    if auto_refresh:
        components.html(
            """
            <script>
            setTimeout(function() {
                window.location.reload();
            }, 5000);
            </script>
            """,
            height=1,
        )
    
    # Asset selection
    col1, col2 = st.columns([2, 1])
    with col1:
        default_assets = {
            "Bitcoin": "BTC-USD",
            "Ethereum": "ETH-USD",
            "Gold": "GC=F",
            "S&P 500": "^GSPC",
            "EUR/USD": "EURUSD=X",
        }
    
    with col2:
        timeframe = st.selectbox("Timeframe", ["15m", "1h", "1d"], index=0)
    
    st.divider()
    
    # Display signals for each asset
    cols = st.columns(len(default_assets))
    
    for i, (name, ticker) in enumerate(default_assets.items()):
        with cols[i]:
            with st.spinner(f"Loading {name}..."):
                try:
                    # Download data
                    period_map = {"15m": "5d", "1h": "30d", "1d": "1y"}
                    data = yf.download(
                        ticker, 
                        period=period_map.get(timeframe, "5d"), 
                        interval=timeframe,
                        progress=False
                    )
                    
                    # Validate data structure
                    if data is None:
                        st.warning(f"No data returned for {name}")
                        continue
                    
                    # Handle MultiIndex columns from yfinance (when downloading multiple assets)
                    if isinstance(data.columns, pd.MultiIndex):
                        # Flatten MultiIndex columns
                        data.columns = data.columns.get_level_values(0)
                    
                    # Handle potential MultiIndex from yfinance
                    if isinstance(data.index, pd.MultiIndex):
                        st.warning(f"Invalid data format for {name}")
                        continue
                    
                    # Check if data is valid and has required columns
                    if not hasattr(data, 'empty') or data.empty:
                        st.warning(f"Insufficient data for {name}")
                        continue
                    
                    if len(data) < 2:
                        st.warning(f"Not enough data points for {name}")
                        continue
                    
                    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                    if not all(col in data.columns for col in required_cols):
                        st.warning(f"Missing OHLCV columns for {name}")
                        continue
                    
                    # Run SMC analysis
                    signal, strength, score = analyze_smc(data)
                    
                    # Extract price data safely with better error handling
                    try:
                        # Handle NaN values - find the last valid price
                        close_series = data['Close']
                        
                        # Drop NaN values to get valid prices
                        close_valid = close_series.dropna()
                        
                        if len(close_valid) < 2:
                            st.warning(f"Not enough valid price data for {name}")
                            continue
                        
                        # Get last two valid prices
                        price = float(close_valid.iloc[-1])
                        price_prev = float(close_valid.iloc[-2])
                        
                        # Make sure values are valid
                        if pd.isna(price) or pd.isna(price_prev):
                            st.warning(f"Invalid price data for {name}")
                            continue
                        
                        price_change = price - price_prev
                        price_change_pct = (price_change / price_prev) * 100 if price_prev != 0 else 0.0
                    except (IndexError, TypeError, ValueError, AttributeError) as e:
                        st.warning(f"Could not extract price for {name}: {str(e)[:50]}")
                        continue
                    
                    st.subheader(name)
                    
                    # Price display
                    st.metric(
                        label="Current Price",
                        value=f"${price:.2f}",
                        delta=f"{price_change_pct:+.2f}%"
                    )
                    
                    # Signal display
                    st.write(f"**Signal:** {signal}")
                    st.write(f"**Strength:** {strength}")
                    st.write(f"**Confidence Score:** {score}/100")
                    
                    # Color-coded recommendation
                    if "BUY" in signal or "UNICORN (Bullish" in signal:
                        st.success("✅ Recommendation: LONG Entry Zone")
                    elif "SELL" in signal or "UNICORN (Bearish" in signal:
                        st.error("❌ Recommendation: SHORT Entry Zone")
                    else:
                        st.info("🔍 Status: Monitoring for Setup")
                
                except Exception as e:
                    error_msg = str(e)
                    # Truncate long error messages
                    if len(error_msg) > 100:
                        error_msg = error_msg[:100] + "..."
                    st.error(f"Error loading {name}: {error_msg}")

    
    # Refresh info
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        if auto_refresh:
            st.caption("Auto-refresh is enabled and will reload the live signal view every 5 seconds.")
        else:
            st.caption("Signals update on manual refresh. Use F5 or the refresh button to pull latest data.")
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()

elif page == "Executive Summary":
    st.header("Executive Summary")

    st.markdown(
        "Institutional traders rely on footprints in price, volume, and time to execute high-probability trades. "
        "This dashboard framework prioritises the strongest Smart Money Concepts signals and overlays risk filters for cleaner entries."
    )
    st.markdown("### Core concept overview")
    st.markdown(
        """
- **Order Blocks (OBs)** and **Fair Value Gaps (FVGs)** mark where institutions build positions.
- **Liquidity Sweeps / Stop Hunts** identify where algorithms clear clustered retail stops.
- **Session Kill Zones** highlight fixed windows of extreme institutional activity.
- **Market Structure Shifts** (Breaks of Structure / Change of Character) signal trend continuation or reversal.
- Advanced order-flow tools like **Volume Profile / POC**, **Cumulative Volume Delta**, and **Order Book Depth** reveal where large participants are active.
- **Risk and execution filters** such as Multi-Timeframe Alignment, position sizing, drawdown controls, R:R tracking, economic calendars, DXY correlation, and sentiment analysis refine decision-making.
        """
    )
    st.markdown("### Dashboard purpose")
    st.markdown(
        "This app is designed as a translation layer from institutional trading concepts into a Streamlit-friendly report and signal reference. "
        "The next development stage is to wire these definitions into live data modules and chart overlays."
    )

elif page == "Top 20 Signals":
    st.header("Prioritised Top-20 Signals")
    st.markdown("The highest-edge features for a Smart Money Concepts dashboard are ranked below with recommended weights.")
    st.markdown(
        """
| Rank | Signal | Why it matters | Suggested weight |
|---|---|---|---|
| 1 | Order Blocks (OBs) | Institutional supply/demand zones | 15 |
| 2 | Fair Value Gaps (FVGs) | Inefficient price zones and re-entry magnets | 10 |
| 3 | Unicorn Setup (OB + FVG) | High-confluence institutional entry | 15 |
| 4 | Liquidity Sweeps / Stop Hunts | Captures retail liquidity and reversal timing | 15 |
| 5 | Session Kill Zones | High-volatility time windows | 10 |
| 6 | Market Structure Shifts | Trend continuation/reversal bias | 15 |
| 7 | Volume Profile / POC | Price levels with high traded volume | 10 |
| 8 | Cumulative Volume Delta (CVD) | Buying/selling pressure divergence | 10 |
| 9 | Order Book Depth | Live liquidity clusters and walls | 10 |
| 10 | VWAP / Anchored VWAP | Institutional execution price anchor | 8 |
| 11 | Optimal Trade Entry (OTE) | Deep retracement entry zone | 10 |
| 12 | SMT Divergence | Correlation divergence across assets | 8 |
| 13 | DXY / Intermarket Correlation | USD bias vs asset behavior | 7 |
| 14 | Economic Calendar Events | News-driven volatility filter | 0 |
| 15 | Real-Time Sentiment | Market mood context | 5 |
| 16 | Multi-Timeframe Alignment (MTFA) | Trend bias across timeframes | 8 |
| 17 | Confluence Scoring | Composite confirmation gauge | N/A |
| 18 | Position Sizing Calculator | Consistent risk sizing | N/A |
| 19 | Daily Drawdown Monitor | Hard loss limit enforcement | N/A |
| 20 | Risk:Reward Tracker | Minimum payoff verification | N/A |
        """
    )
    st.markdown(
        """
### Notes
- Signals with zero or N/A weight are risk controls and filters rather than direct edge signals.
- The system should prioritise confluence and require critical signals like OB or Unicorn before triggering trade alerts.
        """
    )

elif page == "Signal Details":
    st.header("Signal Details")
    st.markdown("### Order Blocks (OBs)")
    st.markdown(
        "Order Blocks are the last opposite-direction candles before a strong institutional move. They act as supply/demand zones where large players may re-enter. "
        "In a dashboard, OBs should be shaded as horizontal bands and updated on each closed candle."
    )
    st.markdown("### Fair Value Gaps (FVGs)")
    st.markdown(
        "FVGs are imbalance zones left by fast moves and often act as price magnets on retracements. "
        "They are detected from consecutive candles with a gap and are visualised as semi-transparent zones."
    )
    st.markdown("### Unicorn Setup")
    st.markdown(
        "A Unicorn forms when an OB overlaps with an unfilled FVG. This is a high-probability entry zone often called the ultimate institutional confluence."
    )
    st.markdown("### Liquidity Sweeps / Stop Hunts")
    st.markdown(
        "Sweeps occur when price moves beyond clustered highs or lows to capture stops. A sweep indicator should compare current price against recent swing levels and mark likely liquidity grabs."
    )
    st.markdown("### Session Kill Zones")
    st.markdown(
        "Fixed intraday windows such as London Open or NY Open are highlighted as temporal anchors. "
        "The dashboard should visibly shade these periods and use them to modulate signal strength."
    )
    st.markdown("### Market Structure Shifts (BOS / CHoCH)")
    st.markdown(
        "Breaks of Structure and Change of Character define trend continuation or early reversal. "
        "These should be derived from swing highs/lows and confirmed on candle closes."
    )
    st.markdown("### Volume Profile / POC")
    st.markdown(
        "Volume Profile maps traded volume by price. The POC is the heaviest volume node and is often defended by institutions. "
        "A sideways histogram with a POC line is recommended."
    )
    st.markdown("### Cumulative Volume Delta (CVD)")
    st.markdown(
        "CVD measures aggressive buy vs sell volume. Divergences between CVD and price highlight hidden order-flow weakness. "
        "Plot CVD under the price chart with divergence markers."
    )
    st.markdown("### Order Book Depth")
    st.markdown(
        "Live depth data reveals large resting bids and asks. Use a depth ladder heatmap or bar chart, with updates every few seconds where possible."
    )
    st.markdown("### VWAP & Anchored VWAP")
    st.markdown(
        "VWAP is the volume-weighted average price and acts as a dynamic institutional reference. "
        "Anchored VWAPs from session open or custom pivots can be added for better context."
    )
    st.markdown("### Optimal Trade Entry (OTE)")
    st.markdown(
        "OTE zones are 62–79% retracements of the last significant impulse. They are useful as premium entry zones when aligned with structure and OBs."
    )
    st.markdown("### SMT / DXY Divergence")
    st.markdown(
        "Correlation divergence across pairs or vs DXY can reveal institutional repositioning. "
        "Highlight divergence events when correlated assets fail to confirm new highs/lows."
    )

elif page == "Data Sources":
    st.header("Data Sources")
    st.markdown("### Recommended sources and practical notes")
    st.markdown(
        """
| Data Type | Free examples | Paid / official | Notes |
|---|---|---|---|
| Price & OHLCV | Yahoo Finance, AlphaVantage, CoinGecko | Bloomberg, Refinitiv, CME Direct | Free APIs have rate limits; use caching. |
| Volume | Included in OHLCV / exchange trade history | Proprietary exchange feeds | Tick/footprint volume may require paid vendor or direct connection. |
| Order Book | Binance/Bybit/Deribit public depth | NASDAQ TotalView, CME MDP | Free depth feeds are often limited to top levels. |
| Sentiment / News | MarketAux, NewsAPI, Google Trends | RavenPack, Thomson Reuters | Use sentiment as contextual filter, not primary trigger. |
| Economic Calendar | TradingEconomics, FXStreet | Econoday, Bloomberg | Schedule-based filters should suppress new entries around high-impact events. |
        """
    )
    st.markdown("### API key and rate-limit guidance")
    st.markdown(
        "- AlphaVantage: 5 calls/min, 25/day free.\n"
        "- NewsAPI: 100 requests/day free.\n"
        "- Binance public REST: no key for price and depth; use websockets for live updates.\n"
        "- TradingEconomics: free tier with limited daily requests.\n"
        "- Store API keys safely using Streamlit secrets in production."
    )

elif page == "Risk & Execution":
    st.header("Risk and Execution Filters")
    st.markdown("### Key overlays for consistency and capital protection")
    st.markdown(
        "- **Multi-Timeframe Alignment (MTFA)**: require trend direction agreement across Daily / 4H / 1H.\n"
        "- **Confluence scoring**: aggregate signal weights into a 0–100 score and trigger alerts only above a threshold.\n"
        "- **Position sizing calculator**: compute size from account equity, risk percentage, and stop distance.\n"
        "- **Daily drawdown monitor**: stop new trades if losses exceed the preset limit.\n"
        "- **Risk:Reward tracker**: require minimum payoff ratios, e.g. 1:2 or better.\n"
    )
    st.markdown("### Execution timeline")
    st.code(
        """
        timeline
            title Institutional Execution Flow (Intraday)
            section Pre-Session Setup
              00:00 : Daily pivot set
              00:00-04:00 : Asian session range (order accumulation)
            section Kill Zones
              07:00 : London Open
              13:30 : New York Open
            section Liquidity Hunts
              14:45 : Sweep of recent HH/LL
            section Structure Shift
              14:50 : Break of Structure
            section Entry Execution
              14:55 : Price returns to OB/FVG (Unicorn entry)
              15:00 : Verify multi-TF alignment and R:R
            section Trade Management
              15:05 : Set stop-loss (by OTE or ATR)
              15:30 : Check VWAP trend and DXY correlation
              23:59 : Daily drawdown reset / profit-taking
        """
    )
    st.markdown(
        "### Deployment suggestion"
        "\n- Host on Streamlit Community Cloud connected to GitHub.\n"
        "- Keep API keys private with Streamlit secrets.\n"
        "- Use SQLite or cached files for historical snapshots if needed.\n"
    )
