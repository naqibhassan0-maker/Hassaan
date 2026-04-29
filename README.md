# Smart Money Concepts Dashboard

A Streamlit dashboard for institutional-style trading signals, signal detection algorithms, and risk management overlays. Includes live real-time SMC signal analysis powered by yfinance.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

## Features

- **Live Signals Tab** — Real-time SMC detection for BTC, ETH, Gold, S&P 500, EUR/USD, and other assets with 15-min/1H/Daily timeframes.
- **Executive Summary** — High-level overview of Smart Money Concepts and institutional trading footprints.
- **Top 20 Signals** — Prioritised signal list with edge impact ratings and suggested weights.
- **Signal Details** — Detailed breakdowns of OB, FVG, Unicorn Setup, Liquidity Sweeps, Kill Zones, Market Structure Shifts, Volume Profile/POC, CVD, Order Book Depth, VWAP, OTE, SMT Divergence, and intermarket correlation.
- **Data Sources** — Recommended APIs (free and paid) for price, volume, order flow, sentiment, and economic calendar data.
- **Risk & Execution** — Risk management filters, position sizing logic, drawdown monitors, R:R tracking, and institutional execution timeline.
- **Deployment Notes** — Guidance for hosting on Streamlit Community Cloud and GitHub.

## SMC Signal Detection Algorithms

The dashboard includes built-in signal detection for:

- **Fair Value Gap (FVG)** — Imbalance zones detected from candle gaps.
- **Market Structure Shifts (BOS)** — Break of Structure from recent swing highs/lows.
- **Volume Spikes** — Price moves with abnormally high volume.
- **Unicorn Confluence** — High-probability setups where FVG and BOS align.

All signals are scored (0–100) with colour-coded recommendations for LONG/SHORT entry zones.

## Run locally

### Option 1: Quick Start (Recommended)
```bash
python3 start.py
```
This automatically installs dependencies and launches the dashboard.

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
python3 test_imports.py

# Launch dashboard
streamlit run streamlit_app.py
```

### Option 3: Using Bash Script (Linux/Mac)
```bash
chmod +x run.sh
./run.sh
```

The dashboard will open at `http://localhost:8501`

### Troubleshooting
If you encounter import errors, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions.


## App structure

- `streamlit_app.py` — Main multi-page dashboard with live signals and educational reference sections.
- `requirements.txt` — Dependencies: Streamlit, yfinance, pandas.

## Data Sources

- **Price & OHLCV:** Yahoo Finance (yfinance library) — free, no key required.
- **Real-time signals:** 15-min, 1H, and daily timeframes via yfinance.
- **Assets tracked:** BTC, ETH, Gold, S&P 500, EUR/USD (expandable).

## Next Steps & Roadmap

- Add order-flow data (CVD) from exchange APIs (Binance, CoinGecko).
- Integrate Volume Profile and Point of Control (POC) visualization.
- Add Order Book Depth heatmaps.
- Risk controls: drawdown monitor, position sizing calculator, R:R validation.
- Economic calendar integration for news filters.
- Multi-asset correlation divergence detection (SMT signals).
- Backtesting module for signal validation.

## Disclaimer

This is a reference and educational dashboard. All signals are informational and not financial advice. Always validate signals with your own analysis and risk management before trading.

