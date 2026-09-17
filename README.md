# Finance Simulator

This Streamlit project turns the investment framework from the finance note into
a scenario simulator for the top-15 watchlist:

`GOOGL`, `MSFT`, `AMZN`, `AVGO`, `ANET`, `ETN`, `VRT`, `TTMI`, `STRL`,
`ORCL`, `CRDO`, `SNDK`, `LITE`, `ACN`, and `VICR`.

The app uses the same project pipeline pattern as the repression simulator:

- a standalone `app.py`
- sidebar scenario inputs
- synthetic simulation engine
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
http://localhost:8501
```

## Evaluate

```powershell
python eval_app.py
```

This is an educational simulator based on synthetic assumptions. It is not
financial advice and should not be treated as a price target, forecast, or buy
recommendation.
