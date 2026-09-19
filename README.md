# Finance Simulator

This Streamlit project turns the investment framework from the finance note into
a scenario simulator for the top-15 watchlist:

`GOOGL`, `MSFT`, `AMZN`, `AVGO`, `ANET`, `ETN`, `VRT`, `TTMI`, `STRL`,
`ORCL`, `CRDO`, `SNDK`, `LITE`, `ACN`, and `VICR`.

The app uses the same project pipeline pattern as the repression simulator:

- a standalone `app.py`
- sidebar scenario inputs
- synthetic simulation engine
- 2001-to-today historical backtest comparison
- forward what-if simulator driven by market-condition parameters
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

## Historical Backtest And Forward What-If

The `2001-Today + What If` tab lets you choose any 5 stocks from the watchlist
and compare a $10,000 equal-weight portfolio from January 2001 through the
latest available month against:

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
- Forward what-if projection chart with median, p10 bear case, and p90 bull case
- Forward risk summary with probability of loss and expected volatility

When `yfinance` is installed and network access is available, the app uses
adjusted monthly close data. If live data is unavailable, it falls back to
deterministic synthetic monthly data so the app and eval harness still work.

The forward what-if simulator extends the latest historical value using the
sidebar macro parameters:

- 10-year Treasury yield
- Fed policy path for cuts or hikes
- Yield curve slope
- inflation
- recession probability
- forward EPS revision
- equity risk premium
- labor market stress
- consumer health
- housing cycle strength
- AI capex growth
- AI revenue conversion quality
- data-center power demand growth
- semiconductor cycle strength
- credit spread
- Treasury issuance / deficit pressure
- volatility regime
- dollar strength
- oil price
- liquidity impulse
- market valuation reset
- tariff / trade pressure
- tax policy pressure
- regulatory / antitrust pressure
- geopolitical risk

Higher rates, inflation, recession probability, credit spreads, equity risk
premium, Treasury issuance pressure, volatility, oil prices, dollar strength,
labor stress, tariffs, tax pressure, regulatory pressure, geopolitical risk,
and valuation-reset pressure reduce projected returns based on each asset's
sensitivity profile. Stronger EPS revisions, AI capex, AI revenue conversion,
power demand, consumer health, housing, semiconductor cycle, yield-curve
normalization, and liquidity can improve projected returns. The projections are
scenario analysis, not forecasts.

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
