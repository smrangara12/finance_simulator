from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Finance Simulator",
    page_icon="FS",
    layout="wide",
)


PALETTE = {
    "ink": "#17212b",
    "muted": "#607080",
    "line": "#d7dee6",
    "blue": "#2f6f9f",
    "green": "#2f8f6f",
    "amber": "#bd7a1f",
    "red": "#bf4e45",
    "purple": "#725ba7",
    "teal": "#237b7b",
}


WATCHLIST = [
    {
        "Ticker": "GOOGL",
        "Company": "Alphabet",
        "Theme": "AI + Cloud",
        "Bucket": "Core",
        "View": "BUY",
        "Revenue growth": 14,
        "EPS/FCF growth": 17,
        "Valuation discipline": 76,
        "Gross margin trend": 74,
        "FCF quality": 92,
        "Debt quality": 92,
        "Customer concentration": 88,
        "Guidance trend": 78,
        "AI monetization": 82,
        "Insider signal": 56,
        "PEG score": 72,
        "Momentum": 68,
        "Starting valuation": 24,
        "Historical CAGR": 16,
        "Volatility": 24,
        "Rate sensitivity": 0.58,
        "AI capex sensitivity": 0.64,
        "Recession sensitivity": 0.34,
    },
    {
        "Ticker": "MSFT",
        "Company": "Microsoft",
        "Theme": "Cloud + AI",
        "Bucket": "Core",
        "View": "BUY",
        "Revenue growth": 15,
        "EPS/FCF growth": 18,
        "Valuation discipline": 66,
        "Gross margin trend": 86,
        "FCF quality": 95,
        "Debt quality": 91,
        "Customer concentration": 90,
        "Guidance trend": 82,
        "AI monetization": 88,
        "Insider signal": 55,
        "PEG score": 66,
        "Momentum": 72,
        "Starting valuation": 33,
        "Historical CAGR": 18,
        "Volatility": 22,
        "Rate sensitivity": 0.66,
        "AI capex sensitivity": 0.74,
        "Recession sensitivity": 0.30,
    },
    {
        "Ticker": "AMZN",
        "Company": "Amazon",
        "Theme": "AWS + AI",
        "Bucket": "Core",
        "View": "BUY",
        "Revenue growth": 12,
        "EPS/FCF growth": 22,
        "Valuation discipline": 70,
        "Gross margin trend": 72,
        "FCF quality": 78,
        "Debt quality": 80,
        "Customer concentration": 86,
        "Guidance trend": 76,
        "AI monetization": 78,
        "Insider signal": 54,
        "PEG score": 70,
        "Momentum": 70,
        "Starting valuation": 30,
        "Historical CAGR": 17,
        "Volatility": 30,
        "Rate sensitivity": 0.72,
        "AI capex sensitivity": 0.78,
        "Recession sensitivity": 0.46,
    },
    {
        "Ticker": "AVGO",
        "Company": "Broadcom",
        "Theme": "AI networking/custom silicon",
        "Bucket": "AI infrastructure",
        "View": "BUY",
        "Revenue growth": 18,
        "EPS/FCF growth": 21,
        "Valuation discipline": 68,
        "Gross margin trend": 82,
        "FCF quality": 90,
        "Debt quality": 73,
        "Customer concentration": 70,
        "Guidance trend": 84,
        "AI monetization": 90,
        "Insider signal": 58,
        "PEG score": 67,
        "Momentum": 82,
        "Starting valuation": 31,
        "Historical CAGR": 24,
        "Volatility": 34,
        "Rate sensitivity": 0.76,
        "AI capex sensitivity": 0.96,
        "Recession sensitivity": 0.42,
    },
    {
        "Ticker": "ANET",
        "Company": "Arista Networks",
        "Theme": "AI networking",
        "Bucket": "AI infrastructure",
        "View": "BUY",
        "Revenue growth": 19,
        "EPS/FCF growth": 20,
        "Valuation discipline": 61,
        "Gross margin trend": 80,
        "FCF quality": 86,
        "Debt quality": 95,
        "Customer concentration": 62,
        "Guidance trend": 82,
        "AI monetization": 85,
        "Insider signal": 52,
        "PEG score": 60,
        "Momentum": 80,
        "Starting valuation": 39,
        "Historical CAGR": 26,
        "Volatility": 36,
        "Rate sensitivity": 0.86,
        "AI capex sensitivity": 0.98,
        "Recession sensitivity": 0.45,
    },
    {
        "Ticker": "ETN",
        "Company": "Eaton",
        "Theme": "Power/electrical",
        "Bucket": "Power/grid",
        "View": "BUY",
        "Revenue growth": 11,
        "EPS/FCF growth": 14,
        "Valuation discipline": 72,
        "Gross margin trend": 78,
        "FCF quality": 84,
        "Debt quality": 82,
        "Customer concentration": 86,
        "Guidance trend": 80,
        "AI monetization": 72,
        "Insider signal": 55,
        "PEG score": 70,
        "Momentum": 76,
        "Starting valuation": 28,
        "Historical CAGR": 21,
        "Volatility": 26,
        "Rate sensitivity": 0.52,
        "AI capex sensitivity": 0.82,
        "Recession sensitivity": 0.38,
    },
    {
        "Ticker": "VRT",
        "Company": "Vertiv",
        "Theme": "Data-center power/cooling",
        "Bucket": "Power/grid",
        "View": "BUY",
        "Revenue growth": 20,
        "EPS/FCF growth": 25,
        "Valuation discipline": 58,
        "Gross margin trend": 72,
        "FCF quality": 76,
        "Debt quality": 70,
        "Customer concentration": 68,
        "Guidance trend": 86,
        "AI monetization": 88,
        "Insider signal": 54,
        "PEG score": 58,
        "Momentum": 88,
        "Starting valuation": 42,
        "Historical CAGR": 34,
        "Volatility": 48,
        "Rate sensitivity": 0.88,
        "AI capex sensitivity": 1.04,
        "Recession sensitivity": 0.50,
    },
    {
        "Ticker": "TTMI",
        "Company": "TTM Technologies",
        "Theme": "PCB/AI infrastructure",
        "Bucket": "Satellite",
        "View": "BUY on weakness",
        "Revenue growth": 13,
        "EPS/FCF growth": 17,
        "Valuation discipline": 78,
        "Gross margin trend": 64,
        "FCF quality": 66,
        "Debt quality": 66,
        "Customer concentration": 60,
        "Guidance trend": 72,
        "AI monetization": 62,
        "Insider signal": 56,
        "PEG score": 76,
        "Momentum": 72,
        "Starting valuation": 19,
        "Historical CAGR": 18,
        "Volatility": 38,
        "Rate sensitivity": 0.62,
        "AI capex sensitivity": 0.72,
        "Recession sensitivity": 0.58,
    },
    {
        "Ticker": "STRL",
        "Company": "Sterling Infrastructure",
        "Theme": "Data-center construction",
        "Bucket": "Satellite",
        "View": "BUY on weakness",
        "Revenue growth": 16,
        "EPS/FCF growth": 22,
        "Valuation discipline": 62,
        "Gross margin trend": 70,
        "FCF quality": 72,
        "Debt quality": 76,
        "Customer concentration": 70,
        "Guidance trend": 78,
        "AI monetization": 68,
        "Insider signal": 58,
        "PEG score": 61,
        "Momentum": 84,
        "Starting valuation": 33,
        "Historical CAGR": 32,
        "Volatility": 44,
        "Rate sensitivity": 0.72,
        "AI capex sensitivity": 0.84,
        "Recession sensitivity": 0.62,
    },
    {
        "Ticker": "ORCL",
        "Company": "Oracle",
        "Theme": "Cloud/AI",
        "Bucket": "Opportunistic",
        "View": "WATCH/BUY ON WEAKNESS",
        "Revenue growth": 18,
        "EPS/FCF growth": 10,
        "Valuation discipline": 55,
        "Gross margin trend": 68,
        "FCF quality": 42,
        "Debt quality": 48,
        "Customer concentration": 80,
        "Guidance trend": 86,
        "AI monetization": 84,
        "Insider signal": 54,
        "PEG score": 52,
        "Momentum": 82,
        "Starting valuation": 36,
        "Historical CAGR": 19,
        "Volatility": 34,
        "Rate sensitivity": 0.92,
        "AI capex sensitivity": 0.90,
        "Recession sensitivity": 0.42,
    },
    {
        "Ticker": "CRDO",
        "Company": "Credo Technology",
        "Theme": "AI connectivity",
        "Bucket": "Satellite",
        "View": "WATCH",
        "Revenue growth": 34,
        "EPS/FCF growth": 32,
        "Valuation discipline": 34,
        "Gross margin trend": 74,
        "FCF quality": 50,
        "Debt quality": 90,
        "Customer concentration": 35,
        "Guidance trend": 88,
        "AI monetization": 90,
        "Insider signal": 48,
        "PEG score": 36,
        "Momentum": 90,
        "Starting valuation": 72,
        "Historical CAGR": 38,
        "Volatility": 64,
        "Rate sensitivity": 1.22,
        "AI capex sensitivity": 1.15,
        "Recession sensitivity": 0.56,
    },
    {
        "Ticker": "SNDK",
        "Company": "SanDisk",
        "Theme": "AI storage",
        "Bucket": "Satellite",
        "View": "WATCH",
        "Revenue growth": 18,
        "EPS/FCF growth": 22,
        "Valuation discipline": 64,
        "Gross margin trend": 55,
        "FCF quality": 58,
        "Debt quality": 68,
        "Customer concentration": 65,
        "Guidance trend": 70,
        "AI monetization": 70,
        "Insider signal": 52,
        "PEG score": 64,
        "Momentum": 66,
        "Starting valuation": 22,
        "Historical CAGR": 16,
        "Volatility": 46,
        "Rate sensitivity": 0.74,
        "AI capex sensitivity": 0.82,
        "Recession sensitivity": 0.72,
    },
    {
        "Ticker": "LITE",
        "Company": "Lumentum",
        "Theme": "Optical AI infrastructure",
        "Bucket": "Satellite",
        "View": "WATCH",
        "Revenue growth": 22,
        "EPS/FCF growth": 24,
        "Valuation discipline": 42,
        "Gross margin trend": 60,
        "FCF quality": 52,
        "Debt quality": 58,
        "Customer concentration": 48,
        "Guidance trend": 76,
        "AI monetization": 78,
        "Insider signal": 50,
        "PEG score": 43,
        "Momentum": 78,
        "Starting valuation": 48,
        "Historical CAGR": 14,
        "Volatility": 58,
        "Rate sensitivity": 1.08,
        "AI capex sensitivity": 1.04,
        "Recession sensitivity": 0.70,
    },
    {
        "Ticker": "ACN",
        "Company": "Accenture",
        "Theme": "AI transformation",
        "Bucket": "Opportunistic",
        "View": "WATCH/ACCUMULATE",
        "Revenue growth": 6,
        "EPS/FCF growth": 8,
        "Valuation discipline": 70,
        "Gross margin trend": 70,
        "FCF quality": 86,
        "Debt quality": 94,
        "Customer concentration": 92,
        "Guidance trend": 58,
        "AI monetization": 62,
        "Insider signal": 54,
        "PEG score": 68,
        "Momentum": 44,
        "Starting valuation": 24,
        "Historical CAGR": 10,
        "Volatility": 23,
        "Rate sensitivity": 0.42,
        "AI capex sensitivity": 0.40,
        "Recession sensitivity": 0.46,
    },
    {
        "Ticker": "VICR",
        "Company": "Vicor",
        "Theme": "AI power",
        "Bucket": "Avoid for now",
        "View": "AVOID-FOR-NOW",
        "Revenue growth": 7,
        "EPS/FCF growth": 6,
        "Valuation discipline": 32,
        "Gross margin trend": 48,
        "FCF quality": 34,
        "Debt quality": 78,
        "Customer concentration": 40,
        "Guidance trend": 42,
        "AI monetization": 54,
        "Insider signal": 46,
        "PEG score": 30,
        "Momentum": 38,
        "Starting valuation": 50,
        "Historical CAGR": 2,
        "Volatility": 56,
        "Rate sensitivity": 1.04,
        "AI capex sensitivity": 0.68,
        "Recession sensitivity": 0.74,
    },
]


FACTOR_WEIGHTS = {
    "Revenue growth score": 0.14,
    "EPS/FCF growth score": 0.14,
    "Valuation discipline": 0.14,
    "Gross margin trend": 0.10,
    "FCF quality": 0.13,
    "Debt quality": 0.08,
    "Customer concentration": 0.07,
    "Guidance trend": 0.07,
    "AI monetization": 0.06,
    "Insider signal": 0.02,
    "PEG score": 0.03,
    "Momentum": 0.02,
}


@dataclass(frozen=True)
class MarketInputs:
    horizon_years: int
    starting_capital: float
    ten_year_yield: float
    inflation: float
    recession_probability: float
    ai_capex_growth: float
    power_demand_growth: float
    credit_spread: float
    dollar_strength: float
    oil_price: float
    liquidity_impulse: float
    valuation_reset: float
    seed: int


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #17212b;
            --muted: #607080;
            --line: #d7dee6;
            --blue: #2f6f9f;
            --green: #2f8f6f;
            --amber: #bd7a1f;
            --red: #bf4e45;
        }

        .stApp {
            color: var(--ink);
            background: linear-gradient(180deg, #f8fafb 0%, #eef3f1 48%, #f7f4ee 100%);
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--line);
        }

        [data-testid="stHeader"] {
            background: rgba(248, 250, 251, 0.94);
        }

        h1, h2, h3, p, div, span, label {
            letter-spacing: 0;
        }

        h1 {
            font-size: clamp(2rem, 3vw, 3.1rem);
            line-height: 1.05;
        }

        [data-testid="stMetric"],
        [data-testid="stDataFrame"],
        .stTabs [data-baseweb="tab-panel"] {
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.8rem;
        }

        .note {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .thesis {
            border-left: 5px solid var(--blue);
            background: rgba(255, 255, 255, 0.74);
            padding: 0.85rem 1rem;
            border-radius: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def clamp(value: np.ndarray | float, low: float, high: float) -> np.ndarray | float:
    return np.clip(value, low, high)


def score_growth(value: float, target: float) -> float:
    return float(clamp(value / target * 100, 0, 100))


def money(value: float) -> str:
    return f"${value:,.0f}"


def preset_values(name: str) -> Dict[str, float]:
    presets = {
        "Base AI buildout": {
            "ten_year_yield": 4.9,
            "inflation": 3.2,
            "recession_probability": 25,
            "ai_capex_growth": 24,
            "power_demand_growth": 12,
            "credit_spread": 1.3,
            "dollar_strength": 55,
            "oil_price": 82,
            "liquidity_impulse": 0.5,
            "valuation_reset": 0,
        },
        "Sticky inflation and 5% rates": {
            "ten_year_yield": 5.25,
            "inflation": 4.4,
            "recession_probability": 34,
            "ai_capex_growth": 18,
            "power_demand_growth": 10,
            "credit_spread": 1.8,
            "dollar_strength": 68,
            "oil_price": 96,
            "liquidity_impulse": -1.8,
            "valuation_reset": -8,
        },
        "Recession/liquidity squeeze": {
            "ten_year_yield": 3.9,
            "inflation": 2.7,
            "recession_probability": 68,
            "ai_capex_growth": 7,
            "power_demand_growth": 5,
            "credit_spread": 3.0,
            "dollar_strength": 72,
            "oil_price": 66,
            "liquidity_impulse": -4.0,
            "valuation_reset": -18,
        },
        "Rate cuts and growth rebound": {
            "ten_year_yield": 3.45,
            "inflation": 2.3,
            "recession_probability": 18,
            "ai_capex_growth": 28,
            "power_demand_growth": 13,
            "credit_spread": 1.0,
            "dollar_strength": 48,
            "oil_price": 74,
            "liquidity_impulse": 3.5,
            "valuation_reset": 8,
        },
        "AI capex digestion": {
            "ten_year_yield": 4.7,
            "inflation": 3.0,
            "recession_probability": 32,
            "ai_capex_growth": 2,
            "power_demand_growth": 8,
            "credit_spread": 1.7,
            "dollar_strength": 61,
            "oil_price": 80,
            "liquidity_impulse": -0.5,
            "valuation_reset": -12,
        },
        "Grid and defense rotation": {
            "ten_year_yield": 4.4,
            "inflation": 3.1,
            "recession_probability": 28,
            "ai_capex_growth": 16,
            "power_demand_growth": 17,
            "credit_spread": 1.4,
            "dollar_strength": 58,
            "oil_price": 88,
            "liquidity_impulse": 0.2,
            "valuation_reset": -2,
        },
    }
    return presets[name]


def get_inputs() -> MarketInputs:
    st.sidebar.header("Market Inputs")
    preset = st.sidebar.selectbox(
        "Scenario preset",
        [
            "Base AI buildout",
            "Sticky inflation and 5% rates",
            "Recession/liquidity squeeze",
            "Rate cuts and growth rebound",
            "AI capex digestion",
            "Grid and defense rotation",
        ],
    )
    values = preset_values(preset)
    starting_capital = st.sidebar.number_input("Starting capital", 10_000, 10_000_000, 100_000, 10_000)
    horizon_years = st.sidebar.slider("Forward horizon", 1, 10, 3, 1)

    with st.sidebar.expander("Rates and macro", expanded=True):
        ten_year_yield = st.slider("10-year Treasury yield (%)", 2.0, 7.0, values["ten_year_yield"], 0.05)
        inflation = st.slider("Inflation (%)", 0.0, 8.0, values["inflation"], 0.1)
        recession_probability = st.slider("Recession probability (%)", 0.0, 90.0, float(values["recession_probability"]), 1.0)
        credit_spread = st.slider("Credit spread (%)", 0.5, 5.0, float(values["credit_spread"]), 0.1)
        liquidity_impulse = st.slider("Liquidity impulse (%)", -6.0, 6.0, float(values["liquidity_impulse"]), 0.1)

    with st.sidebar.expander("AI and physical infrastructure", expanded=True):
        ai_capex_growth = st.slider("AI capex growth (%)", -10.0, 45.0, float(values["ai_capex_growth"]), 1.0)
        power_demand_growth = st.slider("Data-center power demand growth (%)", -5.0, 30.0, float(values["power_demand_growth"]), 1.0)
        valuation_reset = st.slider("Market valuation reset (%)", -35.0, 25.0, float(values["valuation_reset"]), 1.0)

    with st.sidebar.expander("External market inputs", expanded=False):
        dollar_strength = st.slider("Dollar strength index", 20.0, 100.0, float(values["dollar_strength"]), 1.0)
        oil_price = st.slider("Oil price ($/barrel)", 35.0, 160.0, float(values["oil_price"]), 1.0)
        seed = st.number_input("Random seed", 1, 9999, 77, 1)

    return MarketInputs(
        horizon_years=int(horizon_years),
        starting_capital=float(starting_capital),
        ten_year_yield=float(ten_year_yield),
        inflation=float(inflation),
        recession_probability=float(recession_probability),
        ai_capex_growth=float(ai_capex_growth),
        power_demand_growth=float(power_demand_growth),
        credit_spread=float(credit_spread),
        dollar_strength=float(dollar_strength),
        oil_price=float(oil_price),
        liquidity_impulse=float(liquidity_impulse),
        valuation_reset=float(valuation_reset),
        seed=int(seed),
    )


def watchlist_frame() -> pd.DataFrame:
    df = pd.DataFrame(WATCHLIST)
    df["Revenue growth score"] = df["Revenue growth"].map(lambda value: score_growth(value, 15))
    df["EPS/FCF growth score"] = df["EPS/FCF growth"].map(lambda value: score_growth(value, 15))
    df["Factor score"] = sum(df[column] * weight for column, weight in FACTOR_WEIGHTS.items())
    return df


def macro_adjusted_frame(inputs: MarketInputs) -> pd.DataFrame:
    df = watchlist_frame()
    rate_penalty = np.maximum(inputs.ten_year_yield - 4.0, 0) * 3.4 * df["Rate sensitivity"]
    inflation_penalty = np.maximum(inputs.inflation - 2.5, 0) * 1.8
    recession_penalty = inputs.recession_probability / 100 * 18 * df["Recession sensitivity"]
    credit_penalty = np.maximum(inputs.credit_spread - 1.2, 0) * 3.0 * (100 - df["Debt quality"]) / 100
    ai_boost = (inputs.ai_capex_growth - 10) * 0.42 * df["AI capex sensitivity"]
    power_boost = (inputs.power_demand_growth - 7) * 0.38 * df["Theme"].str.contains("Power|power|electrical|construction").astype(float)
    liquidity_boost = inputs.liquidity_impulse * 1.2
    valuation_boost = inputs.valuation_reset * (100 - df["Valuation discipline"]) / 100
    oil_penalty = np.maximum(inputs.oil_price - 85, 0) * 0.05 * df["Recession sensitivity"]
    dollar_penalty = np.maximum(inputs.dollar_strength - 60, 0) * 0.08 * df["Rate sensitivity"]

    df["Macro adjustment"] = (
        ai_boost
        + power_boost
        + liquidity_boost
        + valuation_boost
        - rate_penalty
        - inflation_penalty
        - recession_penalty
        - credit_penalty
        - oil_penalty
        - dollar_penalty
    )
    df["Scenario score"] = clamp(df["Factor score"] + df["Macro adjustment"], 0, 100)
    df["Risk score"] = clamp(
        df["Volatility"] * 0.55
        + df["Starting valuation"] * 0.45
        + df["Rate sensitivity"] * 12
        + (100 - df["FCF quality"]) * 0.20
        + (100 - df["Customer concentration"]) * 0.12,
        0,
        100,
    )
    df["Expected return (%)"] = (
        -2
        + df["Scenario score"] * 0.23
        + df["Revenue growth"] * 0.25
        + df["EPS/FCF growth"] * 0.18
        - df["Risk score"] * 0.12
        - np.maximum(inputs.ten_year_yield - 4.5, 0) * df["Rate sensitivity"] * 2.4
    )
    df["Recommendation"] = np.select(
        [
            (df["Scenario score"] >= 76) & (df["Risk score"] <= 48),
            (df["Scenario score"] >= 68) & (df["Risk score"] <= 62),
            (df["Scenario score"] >= 56),
        ],
        ["Buy/Accumulate", "Watch for entry", "Hold/Research"],
        default="Avoid for now",
    )
    return df.sort_values("Scenario score", ascending=False)


@st.cache_data(show_spinner=False)
def simulate_paths(inputs: MarketInputs) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(inputs.seed)
    df = macro_adjusted_frame(inputs)
    historical_months = 60
    forward_months = inputs.horizon_years * 12
    months = np.arange(-historical_months, forward_months + 1)
    rows = []

    for row in df.to_dict("records"):
        base_price = 100 * np.exp(rng.normal(0, 0.15))
        history_drift = (row["Historical CAGR"] / 100 - 0.5 * (row["Volatility"] / 100) ** 2) / 12
        forward_drift = (row["Expected return (%)"] / 100 - 0.5 * (row["Volatility"] / 100) ** 2) / 12
        monthly_vol = row["Volatility"] / 100 / np.sqrt(12)
        price = base_price
        prices = []
        for month in months:
            drift = history_drift if month <= 0 else forward_drift
            cycle = 0.006 * np.sin((month + len(row["Ticker"])) / 7)
            shock = rng.normal(drift + cycle, monthly_vol)
            price *= np.exp(shock)
            prices.append(price)
        anchor = prices[historical_months]
        normalized_prices = np.array(prices) / anchor * 100
        for month, value in zip(months, normalized_prices):
            rows.append(
                {
                    "Ticker": row["Ticker"],
                    "Company": row["Company"],
                    "Bucket": row["Bucket"],
                    "Theme": row["Theme"],
                    "Month": int(month),
                    "Year": month / 12,
                    "Index value": value,
                    "Period": "Historical simulation" if month <= 0 else "Forward simulation",
                }
            )

    paths = pd.DataFrame(rows)
    portfolio = build_portfolio_path(inputs, paths, df)
    return paths, portfolio


def build_portfolio_path(inputs: MarketInputs, paths: pd.DataFrame, scored: pd.DataFrame) -> pd.DataFrame:
    base_weights = {
        "Core": 0.55,
        "AI infrastructure": 0.22,
        "Power/grid": 0.13,
        "Satellite": 0.08,
        "Opportunistic": 0.02,
        "Avoid for now": 0.00,
    }
    scored = scored.copy()
    scored["Bucket base"] = scored["Bucket"].map(base_weights).fillna(0)
    scored["Weight raw"] = scored["Bucket base"] * scored["Scenario score"] / 100
    scored["Weight"] = scored["Weight raw"] / scored["Weight raw"].sum()
    weighted = paths.merge(scored[["Ticker", "Weight"]], on="Ticker", how="left")
    portfolio = (
        weighted.assign(Contribution=lambda frame: frame["Index value"] * frame["Weight"])
        .groupby(["Month", "Year", "Period"], as_index=False)
        .agg(Portfolio=("Contribution", "sum"))
    )
    portfolio["Portfolio value"] = portfolio["Portfolio"] / 100 * inputs.starting_capital
    return portfolio


def build_evaluation(inputs: MarketInputs, scored: pd.DataFrame, portfolio: pd.DataFrame) -> pd.DataFrame:
    final_value = portfolio.iloc[-1]["Portfolio value"]
    expected_gain = (final_value / inputs.starting_capital - 1) * 100
    avg_score = scored["Scenario score"].mean()
    high_risk_weight = scored.loc[scored["Risk score"] > 65, "Scenario score"].sum() / scored["Scenario score"].sum() * 100
    ai_concentration = scored.loc[scored["Bucket"].isin(["AI infrastructure", "Satellite"]), "Scenario score"].sum() / scored["Scenario score"].sum() * 100
    fcf_floor = scored["FCF quality"].mean()
    rate_risk = inputs.ten_year_yield + inputs.credit_spread

    checks = pd.DataFrame(
        [
            ["Portfolio forward return", expected_gain, ">= 8%", "Pass" if expected_gain >= 8 else "Warn" if expected_gain >= 0 else "Fail"],
            ["Average scenario score", avg_score, ">= 65", "Pass" if avg_score >= 65 else "Warn" if avg_score >= 55 else "Fail"],
            ["High-risk exposure", high_risk_weight, "<= 35%", "Pass" if high_risk_weight <= 35 else "Warn" if high_risk_weight <= 50 else "Fail"],
            ["AI infrastructure concentration", ai_concentration, "<= 45%", "Pass" if ai_concentration <= 45 else "Warn" if ai_concentration <= 58 else "Fail"],
            ["FCF discipline", fcf_floor, ">= 65", "Pass" if fcf_floor >= 65 else "Warn" if fcf_floor >= 55 else "Fail"],
            ["Rate/credit stress", rate_risk, "<= 6.5", "Pass" if rate_risk <= 6.5 else "Warn" if rate_risk <= 8 else "Fail"],
        ],
        columns=["Evaluation", "Value", "Target", "Result"],
    )
    checks["Value"] = checks["Value"].round(2)
    return checks


def plot_scorecard(scored: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        scored.sort_values("Scenario score"),
        x="Scenario score",
        y="Ticker",
        orientation="h",
        color="Recommendation",
        color_discrete_map={
            "Buy/Accumulate": PALETTE["green"],
            "Watch for entry": PALETTE["blue"],
            "Hold/Research": PALETTE["amber"],
            "Avoid for now": PALETTE["red"],
        },
        hover_data=["Theme", "Expected return (%)", "Risk score", "View"],
        title="12-factor score adjusted by market conditions",
    )
    fig.update_layout(xaxis_title="Scenario score", yaxis_title="", margin=dict(l=20, r=20, t=60, b=20))
    return fig


def plot_paths(paths: pd.DataFrame, tickers: Iterable[str]) -> go.Figure:
    frame = paths[paths["Ticker"].isin(tickers)]
    fig = px.line(
        frame,
        x="Year",
        y="Index value",
        color="Ticker",
        line_dash="Period",
        title="Synthetic history and forward scenario paths, today = 100",
    )
    fig.add_vline(x=0, line_dash="dot", line_color="#17212b")
    fig.update_layout(hovermode="x unified", yaxis_title="Index", margin=dict(l=20, r=20, t=60, b=20))
    return fig


def plot_portfolio(portfolio: pd.DataFrame) -> go.Figure:
    fig = px.area(
        portfolio,
        x="Year",
        y="Portfolio value",
        color="Period",
        title="Model portfolio path from framework weights",
        color_discrete_sequence=[PALETTE["blue"], PALETTE["green"]],
    )
    fig.add_vline(x=0, line_dash="dot", line_color="#17212b")
    fig.update_layout(hovermode="x unified", yaxis_title="Portfolio value", margin=dict(l=20, r=20, t=60, b=20))
    return fig


def plot_factor_heatmap(scored: pd.DataFrame) -> go.Figure:
    columns = [
        "Revenue growth score",
        "EPS/FCF growth score",
        "Valuation discipline",
        "Gross margin trend",
        "FCF quality",
        "Debt quality",
        "Customer concentration",
        "Guidance trend",
        "AI monetization",
        "PEG score",
        "Momentum",
    ]
    heat = scored.set_index("Ticker")[columns]
    fig = px.imshow(
        heat,
        color_continuous_scale=[[0, PALETTE["red"]], [0.5, PALETTE["amber"]], [1, PALETTE["green"]]],
        aspect="auto",
        title="Factor heatmap",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20), height=620)
    return fig


def plot_3d_surface(inputs: MarketInputs) -> go.Figure:
    rates = np.linspace(2.5, 6.5, 36)
    ai_growth = np.linspace(-5, 40, 40)
    x, y = np.meshgrid(rates, ai_growth)
    z = (
        8
        + (y - 10) * 0.34
        - np.maximum(x - 4, 0) * 3.8
        - inputs.recession_probability * 0.045
        + inputs.liquidity_impulse * 0.8
        + inputs.valuation_reset * 0.12
    )
    fig = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                colorscale=[[0, PALETTE["red"]], [0.45, PALETTE["amber"]], [0.75, PALETTE["green"]], [1, PALETTE["blue"]]],
                colorbar=dict(title="Return %"),
            )
        ]
    )
    fig.update_layout(
        title="3D sensitivity: rates vs AI capex growth",
        scene=dict(
            xaxis_title="10-year yield (%)",
            yaxis_title="AI capex growth (%)",
            zaxis_title="Portfolio expected return (%)",
            camera=dict(eye=dict(x=1.5, y=-1.55, z=1.1)),
        ),
        height=650,
        margin=dict(l=0, r=0, t=60, b=0),
    )
    return fig


def plot_eval(eval_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        eval_df,
        x="Value",
        y="Evaluation",
        orientation="h",
        color="Result",
        color_discrete_map={"Pass": PALETTE["green"], "Warn": PALETTE["amber"], "Fail": PALETTE["red"]},
        title="Scenario evaluation",
    )
    fig.update_layout(xaxis_title="Value", yaxis_title="", margin=dict(l=20, r=20, t=60, b=20))
    return fig


def verdict(eval_df: pd.DataFrame) -> str:
    counts = eval_df["Result"].value_counts().to_dict()
    if counts.get("Fail", 0):
        return "Fail: scenario quality is constrained by valuation, macro stress, concentration, or weak FCF discipline."
    if counts.get("Warn", 0):
        return "Warn: the setup is investable but entry price, rate sensitivity, or concentration should be watched."
    return "Pass: the scenario aligns with the framework's growth, FCF, valuation, and macro filters."


def main() -> None:
    inject_theme()
    inputs = get_inputs()
    scored = macro_adjusted_frame(inputs)
    paths, portfolio = simulate_paths(inputs)
    eval_df = build_evaluation(inputs, scored, portfolio)

    final_value = portfolio.iloc[-1]["Portfolio value"]
    top = scored.iloc[0]

    st.title("Finance Simulator: AI, Rates, FCF, and Market Conditions")
    st.markdown(
        """
        This simulator turns the investment framework into a scenario model: the 12-factor stock screen
        is combined with external market inputs such as rates, inflation, AI capex, power demand,
        credit spreads, dollar strength, oil, and liquidity.
        """
    )
    st.markdown(
        f"<div class='thesis'>Top simulated setup: <b>{top['Ticker']}</b> ({top['Theme']}) with a "
        f"scenario score of <b>{top['Scenario score']:.1f}</b>. The model portfolio ends at "
        f"<b>{money(final_value)}</b> from {money(inputs.starting_capital)} over {inputs.horizon_years} years.</div>",
        unsafe_allow_html=True,
    )
    st.write("")

    metric_cols = st.columns(5)
    metric_cols[0].metric("Portfolio final value", money(final_value))
    metric_cols[1].metric("Forward return", f"{(final_value / inputs.starting_capital - 1) * 100:.1f}%")
    metric_cols[2].metric("Average score", f"{scored['Scenario score'].mean():.1f}")
    metric_cols[3].metric("10Y yield", f"{inputs.ten_year_yield:.2f}%")
    metric_cols[4].metric("AI capex growth", f"{inputs.ai_capex_growth:.0f}%")

    tabs = st.tabs(["Scorecard", "Simulation", "Factors", "Market Surface", "Evaluation", "Data"])

    with tabs[0]:
        left, right = st.columns([1.25, 1])
        with left:
            st.plotly_chart(plot_scorecard(scored), width="stretch")
        with right:
            st.dataframe(
                scored[
                    [
                        "Ticker",
                        "Theme",
                        "Bucket",
                        "View",
                        "Scenario score",
                        "Risk score",
                        "Expected return (%)",
                        "Recommendation",
                    ]
                ].round(2),
                width="stretch",
                hide_index=True,
            )

    with tabs[1]:
        selected = st.multiselect(
            "Stocks to plot",
            options=scored["Ticker"].tolist(),
            default=scored["Ticker"].head(7).tolist(),
        )
        st.plotly_chart(plot_paths(paths, selected), width="stretch")
        st.plotly_chart(plot_portfolio(portfolio), width="stretch")

    with tabs[2]:
        st.plotly_chart(plot_factor_heatmap(scored), width="stretch")
        st.markdown(
            """
            <p class='note'>
            Tier 1 factors carry the most weight: forward revenue growth, EPS/FCF growth, valuation
            relative to growth, margin trajectory, and FCF quality. Tier 2 and Tier 3 factors refine
            the ranking but do not override weak FCF or excessive valuation.
            </p>
            """,
            unsafe_allow_html=True,
        )

    with tabs[3]:
        st.plotly_chart(plot_3d_surface(inputs), width="stretch")

    with tabs[4]:
        result = verdict(eval_df)
        if result.startswith("Fail"):
            st.error(result)
        elif result.startswith("Warn"):
            st.warning(result)
        else:
            st.success(result)
        left, right = st.columns([1.1, 1])
        with left:
            st.plotly_chart(plot_eval(eval_df), width="stretch")
        with right:
            st.dataframe(eval_df, width="stretch", hide_index=True)

    with tabs[5]:
        st.subheader("Scenario-adjusted watchlist")
        st.dataframe(scored.round(2), width="stretch", hide_index=True)
        st.subheader("Portfolio path")
        st.dataframe(portfolio.round(2), width="stretch", hide_index=True)
        st.download_button(
            "Download scenario scores",
            data=scored.to_csv(index=False),
            file_name="finance_simulator_scores.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
