# Finance Simulator

This Streamlit project turns the investment framework from the finance note into
a scenario simulator for the top-15 watchlist:

`GOOGL`, `MSFT`, `AMZN`, `AVGO`, `ANET`, `ETN`, `VRT`, `TTMI`, `STRL`,
`ORCL`, `CRDO`, `SNDK`, `LITE`, `ACN`, and `VICR`.

The app uses the same project pipeline pattern as the repression simulator:

- a standalone `app.py`
- sidebar scenario inputs
- synthetic simulation engine
- 2001-2025 historical backtest comparison
- 2D and 3D Plotly visualizations
- evaluation scorecard
- `eval_app.py` verification harness

## What It Simulates

The model combines a 12-factor stock screen with market-condition inputs:

- Forward revenue growth
- Forward EPS/FCF growth
- Valuation discipline relative to growth
- Gross-margin trajectory
- Free cash flow quality
- Debt/capital requirements
- Customer concentration
- Management guidance trend
- AI revenue monetization
- Insider signal
- PEG score
- Momentum

External market inputs include 10-year Treasury yields, inflation, recession
probability, AI capex growth, data-center power demand, credit spreads, dollar
strength, oil prices, liquidity impulse, and valuation reset pressure.

## Historical Backtest

The `2001-2025 Backtest` tab lets you choose any 5 stocks from the watchlist and
compare a $10,000 equal-weight portfolio against:

- S&P 500 (`^GSPC`)
- Vanguard Total Stock Market ETF (`VTI`)
- Russell 1000 Growth proxy (`IWF`)
- Large-cap growth proxy (`VUG`)
- Vanguard Balanced Index proxy (`VBIAX`)
- Russell 1000 Value proxy (`IWD`)

The app also maps the requested J.P. Morgan strategy references to public,
observable proxies:

- JPMCAP / Core Advisory Portfolio -> `VTI`
- J.P. Morgan U.S. Large Cap Growth Strategy -> `IWF` or `VUG`
- J.P. Morgan Dynamic Multi-Asset Strategy -> `VBIAX`
- J.P. Morgan Focused Equity Income -> `IWD`

The tab shows:

- $10,000 growth chart
- Return difference versus the selected 5-stock portfolio
- Drawdown chart showing persistent value-fall periods
- Performance and risk profile table
- Greatest fall, recovery, gain-streak, and losing-streak table

When `yfinance` is installed and network access is available, the app uses
adjusted monthly close data. If live data is unavailable, it falls back to
deterministic synthetic monthly data so the app and eval harness still work.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m streamlit run app.py
```

The app usually opens at:

```text
http://localhost:8503
```

## Evaluate

```powershell
python eval_app.py
```

This is an educational simulator based on synthetic assumptions. It is not
financial advice and should not be treated as a price target, forecast, or buy
recommendation.
