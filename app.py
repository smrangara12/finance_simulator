from __future__ import annotations

from dataclasses import dataclass
from datetime import date
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

BACKTEST_START = "2001-01-01"
BACKTEST_END = date.today().isoformat()
BACKTEST_INITIAL_VALUE = 10_000

BENCHMARKS = {
    "S&P 500": "^GSPC",
    "VTI - Total Stock Market": "VTI",
    "IWF - Russell 1000 Growth": "IWF",
    "VUG - Large Cap Growth": "VUG",
    "VBIAX - Balanced Index": "VBIAX",
    "IWD - Russell 1000 Value": "IWD",
}

JPM_PROXY_MAP = {
    "JPMCAP / Core Advisory proxy": "VTI - Total Stock Market",
    "JPM U.S. Large Cap Growth proxy": "IWF - Russell 1000 Growth",
    "JPM U.S. Large Cap Growth proxy / VUG alternate": "VUG - Large Cap Growth",
    "JPM Dynamic Multi-Asset proxy": "VBIAX - Balanced Index",
    "JPM Focused Equity Income proxy": "IWD - Russell 1000 Value",
}

JPM_PROXY_TICKERS = {
    "JPMCAP - Core Advisory proxy (VTI)": "VTI",
    "JPM U.S. Large Cap Growth proxy (IWF)": "IWF",
    "JPM U.S. Large Cap Growth alternate (VUG)": "VUG",
    "JPMPI - Dynamic Multi-Asset proxy (VBIAX)": "VBIAX",
    "JPM Focused Equity Income proxy (IWD)": "IWD",
}

INNOVATOR_UNIVERSE = [
    {"Ticker": "MSFT", "Company": "Microsoft", "Sector": "Technology", "Industry": "Cloud software", "Revenue growth": 15, "EPS/FCF growth": 18, "FCF quality": 95, "Balance sheet": 91, "Moat": 94, "Downside resilience": 88, "Innovation intensity": 90, "Valuation discipline": 66, "Cyclicality risk": 28, "Regulatory risk": 45},
    {"Ticker": "GOOGL", "Company": "Alphabet", "Sector": "Communication Services", "Industry": "AI, search, cloud", "Revenue growth": 14, "EPS/FCF growth": 17, "FCF quality": 92, "Balance sheet": 92, "Moat": 92, "Downside resilience": 86, "Innovation intensity": 88, "Valuation discipline": 76, "Cyclicality risk": 32, "Regulatory risk": 58},
    {"Ticker": "AMZN", "Company": "Amazon", "Sector": "Consumer/Technology", "Industry": "Cloud, ecommerce, ads", "Revenue growth": 12, "EPS/FCF growth": 22, "FCF quality": 78, "Balance sheet": 80, "Moat": 88, "Downside resilience": 78, "Innovation intensity": 86, "Valuation discipline": 70, "Cyclicality risk": 46, "Regulatory risk": 46},
    {"Ticker": "AVGO", "Company": "Broadcom", "Sector": "Technology", "Industry": "AI silicon/networking", "Revenue growth": 18, "EPS/FCF growth": 21, "FCF quality": 90, "Balance sheet": 73, "Moat": 88, "Downside resilience": 76, "Innovation intensity": 85, "Valuation discipline": 68, "Cyclicality risk": 42, "Regulatory risk": 28},
    {"Ticker": "ANET", "Company": "Arista Networks", "Sector": "Technology", "Industry": "Data-center networking", "Revenue growth": 19, "EPS/FCF growth": 20, "FCF quality": 86, "Balance sheet": 95, "Moat": 82, "Downside resilience": 78, "Innovation intensity": 86, "Valuation discipline": 61, "Cyclicality risk": 45, "Regulatory risk": 22},
    {"Ticker": "NVDA", "Company": "NVIDIA", "Sector": "Technology", "Industry": "AI accelerators", "Revenue growth": 28, "EPS/FCF growth": 30, "FCF quality": 92, "Balance sheet": 92, "Moat": 94, "Downside resilience": 72, "Innovation intensity": 98, "Valuation discipline": 46, "Cyclicality risk": 62, "Regulatory risk": 38},
    {"Ticker": "AMD", "Company": "Advanced Micro Devices", "Sector": "Technology", "Industry": "AI compute / CPUs", "Revenue growth": 18, "EPS/FCF growth": 24, "FCF quality": 72, "Balance sheet": 82, "Moat": 72, "Downside resilience": 66, "Innovation intensity": 88, "Valuation discipline": 56, "Cyclicality risk": 64, "Regulatory risk": 26},
    {"Ticker": "TSM", "Company": "Taiwan Semiconductor", "Sector": "Technology", "Industry": "Semiconductor foundry", "Revenue growth": 16, "EPS/FCF growth": 18, "FCF quality": 82, "Balance sheet": 86, "Moat": 96, "Downside resilience": 74, "Innovation intensity": 92, "Valuation discipline": 70, "Cyclicality risk": 55, "Regulatory risk": 64},
    {"Ticker": "ASML", "Company": "ASML", "Sector": "Technology", "Industry": "Semiconductor equipment", "Revenue growth": 13, "EPS/FCF growth": 16, "FCF quality": 86, "Balance sheet": 88, "Moat": 98, "Downside resilience": 78, "Innovation intensity": 94, "Valuation discipline": 66, "Cyclicality risk": 50, "Regulatory risk": 42},
    {"Ticker": "SNOW", "Company": "Snowflake", "Sector": "Technology", "Industry": "Data cloud", "Revenue growth": 24, "EPS/FCF growth": 22, "FCF quality": 62, "Balance sheet": 90, "Moat": 70, "Downside resilience": 54, "Innovation intensity": 86, "Valuation discipline": 38, "Cyclicality risk": 58, "Regulatory risk": 20},
    {"Ticker": "NOW", "Company": "ServiceNow", "Sector": "Technology", "Industry": "Enterprise workflow AI", "Revenue growth": 19, "EPS/FCF growth": 22, "FCF quality": 84, "Balance sheet": 82, "Moat": 84, "Downside resilience": 78, "Innovation intensity": 86, "Valuation discipline": 56, "Cyclicality risk": 38, "Regulatory risk": 18},
    {"Ticker": "CRM", "Company": "Salesforce", "Sector": "Technology", "Industry": "Enterprise software / AI CRM", "Revenue growth": 10, "EPS/FCF growth": 16, "FCF quality": 88, "Balance sheet": 80, "Moat": 82, "Downside resilience": 80, "Innovation intensity": 76, "Valuation discipline": 72, "Cyclicality risk": 35, "Regulatory risk": 20},
    {"Ticker": "PANW", "Company": "Palo Alto Networks", "Sector": "Technology", "Industry": "Cybersecurity", "Revenue growth": 16, "EPS/FCF growth": 20, "FCF quality": 82, "Balance sheet": 76, "Moat": 80, "Downside resilience": 76, "Innovation intensity": 84, "Valuation discipline": 58, "Cyclicality risk": 34, "Regulatory risk": 18},
    {"Ticker": "CRWD", "Company": "CrowdStrike", "Sector": "Technology", "Industry": "Cloud security", "Revenue growth": 22, "EPS/FCF growth": 24, "FCF quality": 76, "Balance sheet": 86, "Moat": 78, "Downside resilience": 68, "Innovation intensity": 86, "Valuation discipline": 44, "Cyclicality risk": 42, "Regulatory risk": 16},
    {"Ticker": "ETN", "Company": "Eaton", "Sector": "Industrials", "Industry": "Power management", "Revenue growth": 11, "EPS/FCF growth": 14, "FCF quality": 84, "Balance sheet": 82, "Moat": 78, "Downside resilience": 82, "Innovation intensity": 72, "Valuation discipline": 72, "Cyclicality risk": 38, "Regulatory risk": 22},
    {"Ticker": "VRT", "Company": "Vertiv", "Sector": "Industrials", "Industry": "Data-center power/cooling", "Revenue growth": 20, "EPS/FCF growth": 25, "FCF quality": 76, "Balance sheet": 70, "Moat": 76, "Downside resilience": 66, "Innovation intensity": 82, "Valuation discipline": 58, "Cyclicality risk": 50, "Regulatory risk": 22},
    {"Ticker": "GEV", "Company": "GE Vernova", "Sector": "Industrials/Energy", "Industry": "Grid and power equipment", "Revenue growth": 10, "EPS/FCF growth": 18, "FCF quality": 66, "Balance sheet": 72, "Moat": 74, "Downside resilience": 68, "Innovation intensity": 76, "Valuation discipline": 62, "Cyclicality risk": 46, "Regulatory risk": 35},
    {"Ticker": "PWR", "Company": "Quanta Services", "Sector": "Industrials", "Industry": "Grid infrastructure", "Revenue growth": 12, "EPS/FCF growth": 15, "FCF quality": 72, "Balance sheet": 76, "Moat": 76, "Downside resilience": 74, "Innovation intensity": 70, "Valuation discipline": 68, "Cyclicality risk": 42, "Regulatory risk": 30},
    {"Ticker": "LLY", "Company": "Eli Lilly", "Sector": "Healthcare", "Industry": "Biopharma innovation", "Revenue growth": 18, "EPS/FCF growth": 24, "FCF quality": 78, "Balance sheet": 76, "Moat": 90, "Downside resilience": 80, "Innovation intensity": 92, "Valuation discipline": 44, "Cyclicality risk": 20, "Regulatory risk": 48},
    {"Ticker": "ISRG", "Company": "Intuitive Surgical", "Sector": "Healthcare", "Industry": "Robotic surgery", "Revenue growth": 14, "EPS/FCF growth": 17, "FCF quality": 88, "Balance sheet": 94, "Moat": 88, "Downside resilience": 82, "Innovation intensity": 86, "Valuation discipline": 58, "Cyclicality risk": 24, "Regulatory risk": 34},
    {"Ticker": "TMO", "Company": "Thermo Fisher Scientific", "Sector": "Healthcare", "Industry": "Life-science tools", "Revenue growth": 8, "EPS/FCF growth": 12, "FCF quality": 84, "Balance sheet": 76, "Moat": 82, "Downside resilience": 78, "Innovation intensity": 72, "Valuation discipline": 70, "Cyclicality risk": 34, "Regulatory risk": 24},
    {"Ticker": "DDOG", "Company": "Datadog", "Sector": "Technology", "Industry": "Observability / cloud monitoring", "Cap tier": "Mid/Large growth", "Revenue growth": 21, "EPS/FCF growth": 24, "FCF quality": 78, "Balance sheet": 86, "Moat": 76, "Downside resilience": 66, "Innovation intensity": 86, "Valuation discipline": 48, "Cyclicality risk": 46, "Regulatory risk": 16},
    {"Ticker": "NET", "Company": "Cloudflare", "Sector": "Technology", "Industry": "Edge cloud / security", "Cap tier": "Mid/Large growth", "Revenue growth": 24, "EPS/FCF growth": 22, "FCF quality": 62, "Balance sheet": 82, "Moat": 72, "Downside resilience": 58, "Innovation intensity": 88, "Valuation discipline": 36, "Cyclicality risk": 50, "Regulatory risk": 18},
    {"Ticker": "GTLB", "Company": "GitLab", "Sector": "Technology", "Industry": "DevSecOps platform", "Cap tier": "Mid cap", "Revenue growth": 22, "EPS/FCF growth": 20, "FCF quality": 58, "Balance sheet": 88, "Moat": 66, "Downside resilience": 56, "Innovation intensity": 84, "Valuation discipline": 42, "Cyclicality risk": 52, "Regulatory risk": 14},
    {"Ticker": "IOT", "Company": "Samsara", "Sector": "Technology", "Industry": "Industrial IoT / fleet software", "Cap tier": "Mid cap", "Revenue growth": 24, "EPS/FCF growth": 22, "FCF quality": 60, "Balance sheet": 86, "Moat": 68, "Downside resilience": 58, "Innovation intensity": 82, "Valuation discipline": 40, "Cyclicality risk": 56, "Regulatory risk": 16},
    {"Ticker": "DUOL", "Company": "Duolingo", "Sector": "Communication Services", "Industry": "AI-enabled education software", "Cap tier": "Mid cap", "Revenue growth": 25, "EPS/FCF growth": 26, "FCF quality": 76, "Balance sheet": 92, "Moat": 74, "Downside resilience": 68, "Innovation intensity": 86, "Valuation discipline": 44, "Cyclicality risk": 42, "Regulatory risk": 18},
    {"Ticker": "APPF", "Company": "AppFolio", "Sector": "Technology", "Industry": "Vertical SaaS / property software", "Cap tier": "Mid cap", "Revenue growth": 17, "EPS/FCF growth": 22, "FCF quality": 74, "Balance sheet": 90, "Moat": 70, "Downside resilience": 70, "Innovation intensity": 76, "Valuation discipline": 58, "Cyclicality risk": 44, "Regulatory risk": 16},
    {"Ticker": "FOUR", "Company": "Shift4 Payments", "Sector": "Financial Technology", "Industry": "Payments infrastructure", "Cap tier": "Mid cap", "Revenue growth": 18, "EPS/FCF growth": 21, "FCF quality": 68, "Balance sheet": 66, "Moat": 66, "Downside resilience": 58, "Innovation intensity": 70, "Valuation discipline": 60, "Cyclicality risk": 58, "Regulatory risk": 26},
    {"Ticker": "BILL", "Company": "BILL Holdings", "Sector": "Financial Technology", "Industry": "SMB payments automation", "Cap tier": "Mid cap", "Revenue growth": 12, "EPS/FCF growth": 18, "FCF quality": 62, "Balance sheet": 78, "Moat": 58, "Downside resilience": 52, "Innovation intensity": 70, "Valuation discipline": 54, "Cyclicality risk": 64, "Regulatory risk": 24},
    {"Ticker": "ALAB", "Company": "Astera Labs", "Sector": "Technology", "Industry": "AI connectivity semiconductors", "Cap tier": "Mid cap", "Revenue growth": 32, "EPS/FCF growth": 34, "FCF quality": 58, "Balance sheet": 82, "Moat": 62, "Downside resilience": 48, "Innovation intensity": 88, "Valuation discipline": 28, "Cyclicality risk": 72, "Regulatory risk": 24},
    {"Ticker": "LSCC", "Company": "Lattice Semiconductor", "Sector": "Technology", "Industry": "Low-power programmable chips", "Cap tier": "Mid cap", "Revenue growth": 12, "EPS/FCF growth": 16, "FCF quality": 78, "Balance sheet": 86, "Moat": 70, "Downside resilience": 66, "Innovation intensity": 76, "Valuation discipline": 58, "Cyclicality risk": 62, "Regulatory risk": 24},
    {"Ticker": "ONTO", "Company": "Onto Innovation", "Sector": "Technology", "Industry": "Semiconductor process control", "Cap tier": "Mid cap", "Revenue growth": 13, "EPS/FCF growth": 17, "FCF quality": 76, "Balance sheet": 90, "Moat": 70, "Downside resilience": 68, "Innovation intensity": 74, "Valuation discipline": 62, "Cyclicality risk": 58, "Regulatory risk": 20},
    {"Ticker": "TMDX", "Company": "TransMedics", "Sector": "Healthcare", "Industry": "Organ transplant technology", "Cap tier": "Small/Mid cap", "Revenue growth": 28, "EPS/FCF growth": 30, "FCF quality": 42, "Balance sheet": 62, "Moat": 64, "Downside resilience": 44, "Innovation intensity": 88, "Valuation discipline": 30, "Cyclicality risk": 46, "Regulatory risk": 56},
    {"Ticker": "INSP", "Company": "Inspire Medical Systems", "Sector": "Healthcare", "Industry": "Sleep apnea medical devices", "Cap tier": "Small/Mid cap", "Revenue growth": 18, "EPS/FCF growth": 20, "FCF quality": 46, "Balance sheet": 80, "Moat": 60, "Downside resilience": 48, "Innovation intensity": 76, "Valuation discipline": 44, "Cyclicality risk": 44, "Regulatory risk": 48},
    {"Ticker": "AXON", "Company": "Axon Enterprise", "Sector": "Industrials/Technology", "Industry": "Public safety software and devices", "Cap tier": "Mid/Large growth", "Revenue growth": 22, "EPS/FCF growth": 24, "FCF quality": 72, "Balance sheet": 84, "Moat": 78, "Downside resilience": 74, "Innovation intensity": 84, "Valuation discipline": 48, "Cyclicality risk": 34, "Regulatory risk": 34},
    {"Ticker": "FSLR", "Company": "First Solar", "Sector": "Energy Technology", "Industry": "Solar manufacturing", "Cap tier": "Mid cap", "Revenue growth": 15, "EPS/FCF growth": 22, "FCF quality": 64, "Balance sheet": 84, "Moat": 68, "Downside resilience": 58, "Innovation intensity": 72, "Valuation discipline": 66, "Cyclicality risk": 62, "Regulatory risk": 46},
    {"Ticker": "FLNC", "Company": "Fluence Energy", "Sector": "Energy Technology", "Industry": "Grid-scale energy storage", "Cap tier": "Small cap", "Revenue growth": 20, "EPS/FCF growth": 24, "FCF quality": 38, "Balance sheet": 62, "Moat": 52, "Downside resilience": 38, "Innovation intensity": 78, "Valuation discipline": 44, "Cyclicality risk": 70, "Regulatory risk": 42},
    {"Ticker": "STEM", "Company": "Stem", "Sector": "Energy Technology", "Industry": "AI energy storage software", "Cap tier": "Small cap", "Revenue growth": 10, "EPS/FCF growth": 16, "FCF quality": 24, "Balance sheet": 40, "Moat": 42, "Downside resilience": 24, "Innovation intensity": 68, "Valuation discipline": 32, "Cyclicality risk": 78, "Regulatory risk": 38},
    {"Ticker": "ENVX", "Company": "Enovix", "Sector": "Industrials/Technology", "Industry": "Advanced batteries", "Cap tier": "Small cap", "Revenue growth": 30, "EPS/FCF growth": 28, "FCF quality": 18, "Balance sheet": 54, "Moat": 48, "Downside resilience": 22, "Innovation intensity": 82, "Valuation discipline": 24, "Cyclicality risk": 80, "Regulatory risk": 28},
    {"Ticker": "ELF", "Company": "e.l.f. Beauty", "Sector": "Consumer", "Industry": "Digitally native beauty brand", "Cap tier": "Mid cap", "Revenue growth": 18, "EPS/FCF growth": 22, "FCF quality": 72, "Balance sheet": 78, "Moat": 66, "Downside resilience": 66, "Innovation intensity": 72, "Valuation discipline": 52, "Cyclicality risk": 48, "Regulatory risk": 14},
    {"Ticker": "ONON", "Company": "On Holding", "Sector": "Consumer", "Industry": "Premium athletic footwear", "Cap tier": "Mid cap", "Revenue growth": 20, "EPS/FCF growth": 23, "FCF quality": 58, "Balance sheet": 82, "Moat": 62, "Downside resilience": 58, "Innovation intensity": 70, "Valuation discipline": 46, "Cyclicality risk": 56, "Regulatory risk": 14},
]


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
    fed_policy_path: float
    yield_curve_slope: float
    eps_revision: float
    equity_risk_premium: float
    labor_market_stress: float
    consumer_health: float
    housing_cycle: float
    treasury_issuance_pressure: float
    volatility_regime: float
    ai_revenue_conversion: float
    semiconductor_cycle: float
    tariff_pressure: float
    tax_policy_pressure: float
    regulatory_pressure: float
    geopolitical_risk: float
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
    extra_defaults = {
        "fed_policy_path": -0.5,
        "yield_curve_slope": 0.2,
        "eps_revision": 3.0,
        "equity_risk_premium": 3.5,
        "labor_market_stress": 25.0,
        "consumer_health": 65.0,
        "housing_cycle": 50.0,
        "treasury_issuance_pressure": 55.0,
        "volatility_regime": 18.0,
        "ai_revenue_conversion": 65.0,
        "semiconductor_cycle": 55.0,
        "tariff_pressure": 20.0,
        "tax_policy_pressure": 25.0,
        "regulatory_pressure": 30.0,
        "geopolitical_risk": 35.0,
    }
    scenario_overrides = {
        "Sticky inflation and 5% rates": {
            "fed_policy_path": 0.3,
            "yield_curve_slope": -0.4,
            "eps_revision": -2.0,
            "equity_risk_premium": 4.4,
            "consumer_health": 48.0,
            "treasury_issuance_pressure": 72.0,
            "volatility_regime": 24.0,
            "tariff_pressure": 35.0,
        },
        "Recession/liquidity squeeze": {
            "fed_policy_path": -1.2,
            "yield_curve_slope": -0.8,
            "eps_revision": -8.0,
            "equity_risk_premium": 5.0,
            "labor_market_stress": 68.0,
            "consumer_health": 32.0,
            "housing_cycle": 25.0,
            "volatility_regime": 34.0,
            "geopolitical_risk": 50.0,
        },
        "Rate cuts and growth rebound": {
            "fed_policy_path": -1.5,
            "yield_curve_slope": 0.9,
            "eps_revision": 7.0,
            "equity_risk_premium": 3.0,
            "labor_market_stress": 18.0,
            "consumer_health": 76.0,
            "housing_cycle": 68.0,
            "volatility_regime": 14.0,
            "ai_revenue_conversion": 74.0,
        },
        "AI capex digestion": {
            "eps_revision": -3.0,
            "ai_revenue_conversion": 38.0,
            "semiconductor_cycle": 35.0,
            "regulatory_pressure": 40.0,
            "volatility_regime": 24.0,
        },
        "Grid and defense rotation": {
            "power_demand_growth": 17,
            "eps_revision": 4.0,
            "housing_cycle": 56.0,
            "treasury_issuance_pressure": 58.0,
            "regulatory_pressure": 38.0,
            "geopolitical_risk": 62.0,
        },
    }
    values = {**extra_defaults, **presets[name]}
    values.update(scenario_overrides.get(name, {}))
    return values


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
        fed_policy_path = st.slider("Fed policy path: cuts/hikes next 12m (%)", -3.0, 3.0, float(values["fed_policy_path"]), 0.1)
        yield_curve_slope = st.slider("Yield curve slope, 10Y-2Y (%)", -2.0, 3.0, float(values["yield_curve_slope"]), 0.1)
        inflation = st.slider("Inflation (%)", 0.0, 8.0, values["inflation"], 0.1)
        recession_probability = st.slider("Recession probability (%)", 0.0, 90.0, float(values["recession_probability"]), 1.0)
        credit_spread = st.slider("Credit spread (%)", 0.5, 5.0, float(values["credit_spread"]), 0.1)
        liquidity_impulse = st.slider("Liquidity impulse (%)", -6.0, 6.0, float(values["liquidity_impulse"]), 0.1)
        equity_risk_premium = st.slider("Equity risk premium (%)", 2.0, 7.0, float(values["equity_risk_premium"]), 0.1)
        treasury_issuance_pressure = st.slider("Treasury issuance / deficit pressure", 0.0, 100.0, float(values["treasury_issuance_pressure"]), 1.0)
        volatility_regime = st.slider("Volatility regime / VIX proxy", 8.0, 50.0, float(values["volatility_regime"]), 1.0)

    with st.sidebar.expander("AI and physical infrastructure", expanded=True):
        ai_capex_growth = st.slider("AI capex growth (%)", -10.0, 45.0, float(values["ai_capex_growth"]), 1.0)
        ai_revenue_conversion = st.slider("AI revenue conversion quality", 0.0, 100.0, float(values["ai_revenue_conversion"]), 1.0)
        power_demand_growth = st.slider("Data-center power demand growth (%)", -5.0, 30.0, float(values["power_demand_growth"]), 1.0)
        semiconductor_cycle = st.slider("Semiconductor cycle strength", 0.0, 100.0, float(values["semiconductor_cycle"]), 1.0)
        valuation_reset = st.slider("Market valuation reset (%)", -35.0, 25.0, float(values["valuation_reset"]), 1.0)

    with st.sidebar.expander("Economy and earnings", expanded=False):
        eps_revision = st.slider("Forward EPS revision (%)", -20.0, 20.0, float(values["eps_revision"]), 0.5)
        labor_market_stress = st.slider("Labor market stress", 0.0, 100.0, float(values["labor_market_stress"]), 1.0)
        consumer_health = st.slider("Consumer health", 0.0, 100.0, float(values["consumer_health"]), 1.0)
        housing_cycle = st.slider("Housing cycle strength", 0.0, 100.0, float(values["housing_cycle"]), 1.0)

    with st.sidebar.expander("Policy and geopolitical risk", expanded=False):
        tariff_pressure = st.slider("Tariff / trade pressure", 0.0, 100.0, float(values["tariff_pressure"]), 1.0)
        tax_policy_pressure = st.slider("Tax policy pressure", 0.0, 100.0, float(values["tax_policy_pressure"]), 1.0)
        regulatory_pressure = st.slider("Regulatory / antitrust pressure", 0.0, 100.0, float(values["regulatory_pressure"]), 1.0)
        geopolitical_risk = st.slider("Geopolitical risk", 0.0, 100.0, float(values["geopolitical_risk"]), 1.0)

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
        fed_policy_path=float(fed_policy_path),
        yield_curve_slope=float(yield_curve_slope),
        eps_revision=float(eps_revision),
        equity_risk_premium=float(equity_risk_premium),
        labor_market_stress=float(labor_market_stress),
        consumer_health=float(consumer_health),
        housing_cycle=float(housing_cycle),
        treasury_issuance_pressure=float(treasury_issuance_pressure),
        volatility_regime=float(volatility_regime),
        ai_revenue_conversion=float(ai_revenue_conversion),
        semiconductor_cycle=float(semiconductor_cycle),
        tariff_pressure=float(tariff_pressure),
        tax_policy_pressure=float(tax_policy_pressure),
        regulatory_pressure=float(regulatory_pressure),
        geopolitical_risk=float(geopolitical_risk),
        seed=int(seed),
    )


def watchlist_frame() -> pd.DataFrame:
    df = pd.DataFrame(WATCHLIST)
    df["Revenue growth score"] = df["Revenue growth"].map(lambda value: score_growth(value, 15))
    df["EPS/FCF growth score"] = df["EPS/FCF growth"].map(lambda value: score_growth(value, 15))
    df["Factor score"] = sum(df[column] * weight for column, weight in FACTOR_WEIGHTS.items())
    return df


def innovator_frame(inputs: MarketInputs) -> pd.DataFrame:
    df = pd.DataFrame(INNOVATOR_UNIVERSE)
    df["Cap tier"] = df["Cap tier"].fillna("Large/Mega cap")
    msft = df[df["Ticker"] == "MSFT"].iloc[0]
    msft_growth = (msft["Revenue growth"] + msft["EPS/FCF growth"]) / 2
    df["Growth vs MSFT %"] = ((df["Revenue growth"] + df["EPS/FCF growth"]) / 2 / msft_growth - 1) * 100
    df["Quality compounder score"] = (
        df["FCF quality"] * 0.20
        + df["Balance sheet"] * 0.14
        + df["Moat"] * 0.17
        + df["Innovation intensity"] * 0.17
        + df["Downside resilience"] * 0.16
        + df["Valuation discipline"] * 0.10
        + np.clip(df["Growth vs MSFT %"] + 50, 0, 100) * 0.06
    )
    df["Long-term downside risk"] = np.clip(
        df["Cyclicality risk"] * 0.26
        + df["Regulatory risk"] * 0.18
        + (100 - df["FCF quality"]) * 0.18
        + (100 - df["Balance sheet"]) * 0.14
        + (100 - df["Valuation discipline"]) * 0.14
        + max(inputs.ten_year_yield - 4, 0) * 3.0
        + max(inputs.equity_risk_premium - 3.5, 0) * 2.5
        + inputs.regulatory_pressure * 0.08
        + inputs.geopolitical_risk * 0.04,
        0,
        100,
    )
    df["Macro-adjusted innovator score"] = np.clip(
        df["Quality compounder score"]
        + (inputs.ai_revenue_conversion - 50) * 0.04
        + inputs.eps_revision * 0.22
        + inputs.liquidity_impulse * 0.45
        - df["Long-term downside risk"] * 0.22,
        0,
        100,
    )
    df["Innovator class"] = np.select(
        [
            (df["Growth vs MSFT %"] >= -10) & (df["Long-term downside risk"] <= 38) & (df["Macro-adjusted innovator score"] >= 68),
            (df["Growth vs MSFT %"] >= 0) & (df["Macro-adjusted innovator score"] >= 64),
            (df["Macro-adjusted innovator score"] >= 58),
        ],
        ["MSFT-like compounder", "Higher-growth innovator", "Watchlist innovator"],
        default="Higher-risk innovator",
    )
    return df.sort_values(["Macro-adjusted innovator score", "Growth vs MSFT %"], ascending=False)


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
    fed_boost = -inputs.fed_policy_path * 1.15 * df["Rate sensitivity"]
    curve_boost = inputs.yield_curve_slope * 0.85
    eps_boost = inputs.eps_revision * 0.55
    erp_penalty = np.maximum(inputs.equity_risk_premium - 3.5, 0) * 2.2 * df["Rate sensitivity"]
    labor_penalty = np.maximum(inputs.labor_market_stress - 35, 0) * 0.07 * df["Recession sensitivity"]
    consumer_boost = (inputs.consumer_health - 50) * 0.045 * (1 - df["Recession sensitivity"] / 2)
    housing_boost = (inputs.housing_cycle - 50) * 0.03
    treasury_penalty = np.maximum(inputs.treasury_issuance_pressure - 55, 0) * 0.035 * df["Rate sensitivity"]
    volatility_penalty = np.maximum(inputs.volatility_regime - 18, 0) * 0.11
    ai_conversion_boost = (inputs.ai_revenue_conversion - 50) * 0.075 * df["AI capex sensitivity"]
    semi_boost = (inputs.semiconductor_cycle - 50) * 0.055 * df["Theme"].str.contains("networking|Optical|storage|PCB|connectivity", case=False).astype(float)
    tariff_penalty = inputs.tariff_pressure * 0.025 * df["Recession sensitivity"]
    tax_penalty = inputs.tax_policy_pressure * 0.025 * (df["FCF quality"] / 100)
    regulatory_penalty = inputs.regulatory_pressure * 0.035 * df["Theme"].str.contains("AI|Cloud|cloud", case=False).astype(float)
    geopolitical_boost = inputs.geopolitical_risk * 0.02 * df["Theme"].str.contains("defense|aerospace|PCB", case=False).astype(float)

    df["Macro adjustment"] = (
        ai_boost
        + power_boost
        + liquidity_boost
        + valuation_boost
        + fed_boost
        + curve_boost
        + eps_boost
        + consumer_boost
        + housing_boost
        + ai_conversion_boost
        + semi_boost
        + geopolitical_boost
        - rate_penalty
        - inflation_penalty
        - recession_penalty
        - credit_penalty
        - oil_penalty
        - dollar_penalty
        - erp_penalty
        - labor_penalty
        - treasury_penalty
        - volatility_penalty
        - tariff_penalty
        - tax_penalty
        - regulatory_penalty
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


def available_watchlist_tickers() -> list[str]:
    return [item["Ticker"] for item in WATCHLIST]


def synthetic_monthly_prices(tickers: list[str], start: str = BACKTEST_START, end: str = BACKTEST_END) -> pd.DataFrame:
    dates = pd.date_range(start=start, end=end, freq="ME")
    rows = []
    watch = watchlist_frame().set_index("Ticker")
    benchmark_profiles = {
        "^GSPC": (7.6, 15.0),
        "VTI": (7.8, 15.5),
        "IWF": (8.6, 18.0),
        "VUG": (8.8, 18.5),
        "VBIAX": (6.1, 9.5),
        "IWD": (7.0, 16.0),
    }
    crisis_shocks = {
        2001: -0.025,
        2002: -0.030,
        2008: -0.060,
        2020: -0.045,
        2022: -0.035,
    }

    for ticker in tickers:
        if ticker in watch.index:
            cagr = float(watch.loc[ticker, "Historical CAGR"])
            volatility = float(watch.loc[ticker, "Volatility"])
        else:
            cagr, volatility = benchmark_profiles.get(ticker, (7.0, 16.0))
        rng = np.random.default_rng(sum(ord(char) for char in ticker) + 2001)
        price = 100.0
        for date in dates:
            drift = (cagr / 100 - 0.5 * (volatility / 100) ** 2) / 12
            shock = crisis_shocks.get(date.year, 0.0) if date.month in {2, 3, 9, 10} else 0.0
            cycle = 0.004 * np.sin((date.year - 2001) / 1.8 + len(ticker))
            monthly_return = rng.normal(drift + cycle + shock, volatility / 100 / np.sqrt(12))
            price *= np.exp(monthly_return)
            rows.append({"Date": date, "Ticker": ticker, "Adj Close": price, "Source": "synthetic fallback"})
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def load_monthly_prices(tickers: tuple[str, ...], start: str = BACKTEST_START, end: str = BACKTEST_END) -> tuple[pd.DataFrame, str]:
    ticker_list = list(dict.fromkeys(tickers))
    try:
        import yfinance as yf

        raw = yf.download(
            ticker_list,
            start=start,
            end=end,
            auto_adjust=True,
            progress=False,
            group_by="ticker",
            threads=True,
        )
        if raw.empty:
            raise RuntimeError("yfinance returned no rows")

        if len(ticker_list) == 1:
            prices = raw[["Close"]].rename(columns={"Close": ticker_list[0]})
        else:
            prices = pd.DataFrame({ticker: raw[ticker]["Close"] for ticker in ticker_list if ticker in raw.columns.get_level_values(0)})
        monthly = prices.resample("ME").last().dropna(how="all")
        frame = monthly.reset_index().melt(id_vars="Date", var_name="Ticker", value_name="Adj Close")
        frame = frame.dropna(subset=["Adj Close"])
        frame["Source"] = "yfinance adjusted close"
        missing = set(ticker_list) - set(frame["Ticker"].unique())
        if missing:
            fallback = synthetic_monthly_prices(sorted(missing), start, end)
            frame = pd.concat([frame, fallback], ignore_index=True)
            return frame, "mixed: yfinance plus synthetic fallback for missing tickers"
        return frame, "yfinance adjusted close"
    except Exception:
        return synthetic_monthly_prices(ticker_list, start, end), "synthetic fallback"


def build_historical_backtest(selected_stocks: list[str], initial_value: float = BACKTEST_INITIAL_VALUE) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    selected = selected_stocks[:5]
    benchmark_tickers = list(BENCHMARKS.values())
    tickers = tuple(selected + benchmark_tickers)
    prices_long, source = load_monthly_prices(tickers)
    prices = prices_long.pivot_table(index="Date", columns="Ticker", values="Adj Close", aggfunc="last").sort_index()
    returns = prices.pct_change()

    series = {}
    for ticker in selected + benchmark_tickers:
        if ticker in prices:
            normalized = prices[ticker].dropna()
            if not normalized.empty:
                series[ticker] = normalized / normalized.iloc[0] * initial_value

    selected_returns = returns[selected].dropna(how="all")
    selected_returns = selected_returns.mean(axis=1, skipna=True).dropna()
    selected_portfolio = (1 + selected_returns).cumprod() * initial_value
    if not selected_portfolio.empty:
        first_date = selected_portfolio.index.min()
        selected_portfolio.loc[first_date] = initial_value
        selected_portfolio = selected_portfolio.sort_index()
        series["Selected 5 equal-weight"] = selected_portfolio

    value_frame = pd.DataFrame(series).sort_index()
    for jpm_label, proxy_ticker in JPM_PROXY_TICKERS.items():
        if proxy_ticker in value_frame:
            value_frame[jpm_label] = value_frame[proxy_ticker]
    value_frame = value_frame.dropna(how="all")
    value_long = value_frame.reset_index().melt(id_vars="Date", var_name="Asset", value_name="Value").dropna()
    metrics = performance_metrics(value_frame)
    periods = drawdown_and_gain_periods(value_frame)
    return value_long, metrics, periods, source


def performance_metrics(value_frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    selected_final = value_frame.get("Selected 5 equal-weight", pd.Series(dtype=float)).dropna()
    selected_terminal = float(selected_final.iloc[-1]) if not selected_final.empty else np.nan
    sp_final = value_frame.get("^GSPC", pd.Series(dtype=float)).dropna()
    sp_terminal = float(sp_final.iloc[-1]) if not sp_final.empty else np.nan

    for asset in value_frame.columns:
        values = value_frame[asset].dropna()
        if len(values) < 2:
            continue
        monthly_returns = values.pct_change().dropna()
        years = max((values.index[-1] - values.index[0]).days / 365.25, 1 / 12)
        terminal = float(values.iloc[-1])
        total_return = terminal / values.iloc[0] - 1
        cagr = (terminal / values.iloc[0]) ** (1 / years) - 1
        volatility = monthly_returns.std() * np.sqrt(12)
        running_max = values.cummax()
        drawdown = values / running_max - 1
        max_drawdown = drawdown.min()
        best_month = monthly_returns.max()
        worst_month = monthly_returns.min()
        positive_months = (monthly_returns > 0).mean()
        rows.append(
            {
                "Asset": asset_label(asset),
                "Ticker": asset,
                "Final value": terminal,
                "Total return %": total_return * 100,
                "Return difference vs Selected 5 %": (
                    (terminal / selected_terminal - 1) * 100
                    if np.isfinite(selected_terminal) and asset != "Selected 5 equal-weight"
                    else 0
                ),
                "Return difference vs S&P 500 %": (
                    (terminal / sp_terminal - 1) * 100
                    if np.isfinite(sp_terminal) and asset != "^GSPC"
                    else 0
                ),
                "CAGR %": cagr * 100,
                "Annual volatility %": volatility * 100,
                "Max drawdown %": max_drawdown * 100,
                "Best month %": best_month * 100,
                "Worst month %": worst_month * 100,
                "Positive months %": positive_months * 100,
                "Risk profile": risk_profile(volatility, max_drawdown),
                "Greatest risk": greatest_risk(asset, volatility, max_drawdown),
            }
        )
    return pd.DataFrame(rows).sort_values("Final value", ascending=False)


def asset_label(asset: str) -> str:
    labels = {value: key for key, value in BENCHMARKS.items()}
    labels["Selected 5 equal-weight"] = "Selected 5 equal-weight"
    return labels.get(asset, asset)


def risk_profile(volatility: float, max_drawdown: float) -> str:
    if volatility > 0.32 or max_drawdown < -0.55:
        return "Aggressive / high drawdown risk"
    if volatility > 0.20 or max_drawdown < -0.35:
        return "Growth / moderate-high risk"
    if volatility > 0.12 or max_drawdown < -0.22:
        return "Balanced / moderate risk"
    return "Defensive / lower volatility"


def greatest_risk(asset: str, volatility: float, max_drawdown: float) -> str:
    if asset in {"IWF", "VUG"}:
        return "Growth valuation compression during high-rate periods"
    if asset == "VBIAX":
        return "Balanced fund still exposed to simultaneous stock/bond drawdowns"
    if asset == "IWD":
        return "Value traps, financial cyclicality, and slower earnings growth"
    if asset == "VTI":
        return "Broad equity beta and recession drawdowns"
    if asset == "^GSPC":
        return "Large-cap concentration and market-cycle drawdowns"
    if max_drawdown < -0.5:
        return "Persistent value fall after valuation reset or business-cycle shock"
    if volatility > 0.3:
        return "High volatility and timing risk"
    return "Business execution, valuation, and macro sensitivity"


def drawdown_and_gain_periods(value_frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for asset in value_frame.columns:
        values = value_frame[asset].dropna()
        if len(values) < 3:
            continue
        running_max = values.cummax()
        drawdown = values / running_max - 1
        trough_date = drawdown.idxmin()
        peak_date = values.loc[:trough_date].idxmax()
        recovery_candidates = values.loc[trough_date:][values.loc[trough_date:] >= values.loc[peak_date]]
        recovery_date = recovery_candidates.index[0] if not recovery_candidates.empty else pd.NaT
        fall_months = max((trough_date.year - peak_date.year) * 12 + trough_date.month - peak_date.month, 0)
        recovery_months = (
            (recovery_date.year - trough_date.year) * 12 + recovery_date.month - trough_date.month
            if pd.notna(recovery_date)
            else np.nan
        )

        returns = values.pct_change().dropna()
        gain_streak, fall_streak = longest_streaks(returns)
        rows.append(
            {
                "Asset": asset_label(asset),
                "Ticker": asset,
                "Greatest fall start": peak_date.strftime("%Y-%m-%d"),
                "Greatest fall trough": trough_date.strftime("%Y-%m-%d"),
                "Recovered by": recovery_date.strftime("%Y-%m-%d") if pd.notna(recovery_date) else "Not recovered by latest data",
                "Max drawdown %": drawdown.min() * 100,
                "Persistent value fall months": fall_months,
                "Recovery months": recovery_months,
                "Longest gain period months": gain_streak,
                "Longest losing period months": fall_streak,
            }
        )
    return pd.DataFrame(rows).sort_values("Max drawdown %")


def longest_streaks(returns: pd.Series) -> tuple[int, int]:
    gain_best = gain_current = 0
    loss_best = loss_current = 0
    for value in returns:
        if value > 0:
            gain_current += 1
            loss_current = 0
        elif value < 0:
            loss_current += 1
            gain_current = 0
        else:
            gain_current = 0
            loss_current = 0
        gain_best = max(gain_best, gain_current)
        loss_best = max(loss_best, loss_current)
    return gain_best, loss_best


def what_if_adjustment(asset: str, inputs: MarketInputs) -> tuple[float, float, str]:
    watch = watchlist_frame().set_index("Ticker")
    base_return = 7.0
    base_volatility = 15.0
    rate_sensitivity = 0.55
    recession_sensitivity = 0.45
    ai_sensitivity = 0.25
    power_sensitivity = 0.15
    semi_sensitivity = 0.10
    regulatory_sensitivity = 0.25
    risk_note = "Broad market beta and macro-cycle risk"

    if asset in watch.index:
        row = watch.loc[asset]
        base_return = float(row["Historical CAGR"])
        base_volatility = float(row["Volatility"])
        rate_sensitivity = float(row["Rate sensitivity"])
        recession_sensitivity = float(row["Recession sensitivity"])
        ai_sensitivity = float(row["AI capex sensitivity"])
        power_sensitivity = 0.55 if "power" in str(row["Theme"]).lower() or "construction" in str(row["Theme"]).lower() else 0.20
        semi_sensitivity = 0.65 if any(term in str(row["Theme"]).lower() for term in ["networking", "optical", "storage", "pcb", "connectivity"]) else 0.10
        regulatory_sensitivity = 0.55 if any(term in str(row["Theme"]).lower() for term in ["ai", "cloud"]) else 0.20
        risk_note = greatest_risk(asset, base_volatility / 100, -0.35)
    elif asset in {"IWF", "VUG"}:
        base_return, base_volatility, rate_sensitivity, ai_sensitivity = 8.5, 18.0, 0.85, 0.45
        risk_note = "Growth multiple compression if rates stay high"
    elif asset == "VBIAX":
        base_return, base_volatility, rate_sensitivity, recession_sensitivity = 6.0, 9.5, 0.35, 0.25
        risk_note = "Stock/bond correlation shock and lower upside capture"
    elif asset == "IWD":
        base_return, base_volatility, rate_sensitivity, recession_sensitivity = 7.0, 16.0, 0.48, 0.55
        risk_note = "Value cyclicality, financial exposure, and slower growth"
    elif asset in {"^GSPC", "VTI"}:
        base_return, base_volatility, rate_sensitivity, recession_sensitivity = 7.6, 15.5, 0.55, 0.45

    adjusted_return = (
        base_return
        + (inputs.ai_capex_growth - 10) * 0.18 * ai_sensitivity
        + (inputs.power_demand_growth - 7) * 0.14 * power_sensitivity
        + inputs.liquidity_impulse * 0.55
        + inputs.valuation_reset * 0.22 * rate_sensitivity
        - inputs.fed_policy_path * 0.85 * rate_sensitivity
        + inputs.yield_curve_slope * 0.45
        + inputs.eps_revision * 0.35
        + (inputs.consumer_health - 50) * 0.055 * (1 - recession_sensitivity / 2)
        + (inputs.housing_cycle - 50) * 0.025
        + (inputs.ai_revenue_conversion - 50) * 0.055 * ai_sensitivity
        + (inputs.semiconductor_cycle - 50) * 0.045 * semi_sensitivity
        + inputs.geopolitical_risk * 0.018 * semi_sensitivity
        - max(inputs.ten_year_yield - 4.0, 0) * 1.75 * rate_sensitivity
        - max(inputs.inflation - 2.5, 0) * 0.65
        - inputs.recession_probability * 0.075 * recession_sensitivity
        - max(inputs.credit_spread - 1.2, 0) * 0.75
        - max(inputs.oil_price - 85, 0) * 0.025 * recession_sensitivity
        - max(inputs.dollar_strength - 60, 0) * 0.035 * rate_sensitivity
        - max(inputs.equity_risk_premium - 3.5, 0) * 1.15 * rate_sensitivity
        - max(inputs.labor_market_stress - 35, 0) * 0.045 * recession_sensitivity
        - max(inputs.treasury_issuance_pressure - 55, 0) * 0.035 * rate_sensitivity
        - inputs.tariff_pressure * 0.018 * recession_sensitivity
        - inputs.tax_policy_pressure * 0.018
        - inputs.regulatory_pressure * 0.026 * regulatory_sensitivity
    )
    adjusted_volatility = base_volatility * (
        1
        + inputs.recession_probability / 250
        + max(inputs.credit_spread - 1.2, 0) / 10
        + abs(inputs.valuation_reset) / 180
        + max(inputs.volatility_regime - 18, 0) / 90
        + max(inputs.geopolitical_risk - 40, 0) / 280
    )
    return float(adjusted_return), float(adjusted_volatility), risk_note


def build_forward_what_if(
    value_long: pd.DataFrame,
    selected_stocks: list[str],
    inputs: MarketInputs,
    horizon_years: int,
    paths: int = 120,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    base = value_long.pivot_table(index="Date", columns="Asset", values="Value", aggfunc="last").sort_index()
    if base.empty:
        return pd.DataFrame(), pd.DataFrame()
    start_date = pd.Timestamp(base.index.max())
    future_dates = pd.date_range(start=start_date + pd.offsets.MonthEnd(1), periods=horizon_years * 12, freq="ME")
    assets = list(base.columns)
    rng = np.random.default_rng(inputs.seed + horizon_years + len(selected_stocks))
    rows = []
    summary_rows = []

    for asset_label_value in assets:
        current_value = float(base[asset_label_value].dropna().iloc[-1])
        ticker = reverse_asset_label(asset_label_value)
        expected_return, volatility, risk_note = what_if_adjustment(ticker, inputs)
        monthly_drift = (expected_return / 100 - 0.5 * (volatility / 100) ** 2) / 12
        monthly_vol = volatility / 100 / np.sqrt(12)
        terminal_values = []

        for path_id in range(paths):
            value = current_value
            for date_value in future_dates:
                shock = rng.normal(monthly_drift, monthly_vol)
                value *= np.exp(shock)
                rows.append(
                    {
                        "Date": date_value,
                        "Asset": asset_label_value,
                        "Path": path_id,
                        "Value": value,
                        "Expected annual return %": expected_return,
                        "Expected annual volatility %": volatility,
                    }
                )
            terminal_values.append(value)

        terminal = np.array(terminal_values)
        summary_rows.append(
            {
                "Asset": asset_label_value,
                "Current value": current_value,
                "Median terminal value": np.percentile(terminal, 50),
                "Bear case p10": np.percentile(terminal, 10),
                "Bull case p90": np.percentile(terminal, 90),
                "Median forward return %": (np.percentile(terminal, 50) / current_value - 1) * 100,
                "Probability of loss %": (terminal < current_value).mean() * 100,
                "Expected annual return %": expected_return,
                "Expected annual volatility %": volatility,
                "Greatest forward risk": risk_note,
            }
        )

    forward_paths = pd.DataFrame(rows)
    percentiles = (
        forward_paths.groupby(["Date", "Asset"])["Value"]
        .quantile([0.1, 0.5, 0.9])
        .unstack()
        .rename(columns={0.1: "Bear case p10", 0.5: "Median", 0.9: "Bull case p90"})
        .reset_index()
    )
    return percentiles, pd.DataFrame(summary_rows).sort_values("Median terminal value", ascending=False)


def reverse_asset_label(label: str) -> str:
    labels = {value: key for key, value in BENCHMARKS.items()}
    reverse = {friendly: ticker for ticker, friendly in labels.items()}
    reverse.update(JPM_PROXY_TICKERS)
    reverse["Selected 5 equal-weight"] = "Selected 5 equal-weight"
    return reverse.get(label, label)


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


def plot_backtest_values(value_long: pd.DataFrame) -> go.Figure:
    fig = px.line(
        value_long,
        x="Date",
        y="Value",
        color="Asset",
        title=f"$10,000 growth comparison, {BACKTEST_START[:4]}-{BACKTEST_END[:4]}",
    )
    fig.update_traces(line=dict(width=2.4))
    fig.update_layout(hovermode="x unified", yaxis_title="Portfolio value", margin=dict(l=20, r=20, t=60, b=20))
    return fig


def plot_return_difference(metrics: pd.DataFrame) -> go.Figure:
    frame = metrics.copy().sort_values("Return difference vs Selected 5 %")
    fig = px.bar(
        frame,
        x="Return difference vs Selected 5 %",
        y="Asset",
        orientation="h",
        color="Return difference vs Selected 5 %",
        color_continuous_scale=[[0, PALETTE["red"]], [0.5, PALETTE["amber"]], [1, PALETTE["green"]]],
        title="Return difference versus selected 5-stock portfolio",
    )
    fig.add_vline(x=0, line_dash="dot", line_color="#17212b")
    fig.update_layout(yaxis_title="", coloraxis_showscale=False, margin=dict(l=20, r=20, t=60, b=20))
    return fig


def plot_drawdowns(value_long: pd.DataFrame) -> go.Figure:
    value_frame = value_long.pivot_table(index="Date", columns="Asset", values="Value", aggfunc="last").sort_index()
    drawdown = value_frame / value_frame.cummax() - 1
    drawdown_long = drawdown.reset_index().melt(id_vars="Date", var_name="Asset", value_name="Drawdown")
    fig = px.area(
        drawdown_long.dropna(),
        x="Date",
        y="Drawdown",
        color="Asset",
        title="Persistent value fall periods: drawdown from prior high",
    )
    fig.update_layout(hovermode="x unified", yaxis_tickformat=".0%", yaxis_title="Drawdown", margin=dict(l=20, r=20, t=60, b=20))
    return fig


def plot_forward_what_if(forward_percentiles: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for asset in forward_percentiles["Asset"].unique():
        frame = forward_percentiles[forward_percentiles["Asset"] == asset].sort_values("Date")
        fig.add_trace(
            go.Scatter(
                x=frame["Date"],
                y=frame["Bull case p90"],
                mode="lines",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=frame["Date"],
                y=frame["Bear case p10"],
                mode="lines",
                fill="tonexty",
                name=f"{asset} p10-p90",
                line=dict(width=0),
                opacity=0.18,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=frame["Date"],
                y=frame["Median"],
                mode="lines",
                name=f"{asset} median",
                line=dict(width=2.2),
            )
        )
    fig.update_layout(
        title="Forward what-if simulation: median and p10/p90 range",
        xaxis_title="Date",
        yaxis_title="Projected value",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def plot_innovator_scatter(innovators: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        innovators,
        x="Long-term downside risk",
        y="Growth vs MSFT %",
        size="Macro-adjusted innovator score",
        color="Cap tier",
        hover_name="Ticker",
        hover_data=["Company", "Sector", "Industry", "FCF quality", "Balance sheet", "Moat", "Innovator class"],
        title="Innovators: Microsoft-like or higher growth versus long-term downside risk",
    )
    fig.add_hline(y=0, line_dash="dot", line_color="#17212b", annotation_text="MSFT growth baseline")
    fig.update_layout(xaxis_title="Lower is better: long-term downside risk", yaxis_title="Growth vs MSFT", margin=dict(l=20, r=20, t=60, b=20))
    return fig


def plot_sector_innovators(innovators: pd.DataFrame) -> go.Figure:
    sector_frame = (
        innovators.groupby("Sector", as_index=False)
        .agg(
            Avg_score=("Macro-adjusted innovator score", "mean"),
            Avg_growth_vs_msft=("Growth vs MSFT %", "mean"),
            Avg_downside_risk=("Long-term downside risk", "mean"),
            Count=("Ticker", "count"),
        )
        .sort_values("Avg_score", ascending=False)
    )
    fig = px.bar(
        sector_frame,
        x="Avg_score",
        y="Sector",
        orientation="h",
        color="Avg_downside_risk",
        color_continuous_scale=[[0, PALETTE["green"]], [0.55, PALETTE["amber"]], [1, PALETTE["red"]]],
        title="Sectorwise innovator potential and downside risk",
        hover_data=["Avg_growth_vs_msft", "Count"],
    )
    fig.update_layout(xaxis_title="Average innovator score", yaxis_title="", margin=dict(l=20, r=20, t=60, b=20))
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
    innovators = innovator_frame(inputs)
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

    tabs = st.tabs(["Scorecard", "Simulation", "2001-Today + What If", "Innovators", "Factors", "Market Surface", "Evaluation", "Data"])

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
        st.subheader("Compare Any 5 Stocks Against Market And JPM Proxy Benchmarks")
        st.caption("Historical comparison runs from January 2001 through the latest available month, then extends with a forward what-if simulator.")
        default_backtest = ["GOOGL", "MSFT", "AMZN", "AVGO", "ETN"]
        selected_backtest = st.multiselect(
            "Choose up to 5 watchlist stocks",
            options=available_watchlist_tickers(),
            default=default_backtest,
            max_selections=5,
        )
        forward_horizon = st.slider("Forward what-if horizon after latest data", 1, 15, 5, 1)
        if len(selected_backtest) != 5:
            st.warning("Select exactly 5 stocks to make the equal-weight comparison meaningful.")
        else:
            value_long, metrics, periods, data_source = build_historical_backtest(selected_backtest)
            forward_percentiles, forward_summary = build_forward_what_if(value_long, selected_backtest, inputs, forward_horizon)
            selected_final = metrics.loc[metrics["Ticker"] == "Selected 5 equal-weight", "Final value"]
            sp_final = metrics.loc[metrics["Ticker"] == "^GSPC", "Final value"]
            selected_value = float(selected_final.iloc[0]) if not selected_final.empty else np.nan
            sp_value = float(sp_final.iloc[0]) if not sp_final.empty else np.nan

            st.caption(
                f"Data source: {data_source}. The JPM strategies are represented by public proxies: "
                f"JPMCAP -> VTI, U.S. Large Cap Growth -> IWF/VUG, Dynamic Multi-Asset -> VBIAX, "
                f"Focused Equity Income -> IWD. JPM proxy labels are included as separate comparison lines."
            )
            metric_cols = st.columns(4)
            metric_cols[0].metric("Initial investment", money(BACKTEST_INITIAL_VALUE))
            metric_cols[1].metric("Selected 5 final", money(selected_value) if np.isfinite(selected_value) else "n/a")
            metric_cols[2].metric("S&P 500 final", money(sp_value) if np.isfinite(sp_value) else "n/a")
            metric_cols[3].metric(
                "Difference vs S&P",
                f"{(selected_value / sp_value - 1) * 100:.1f}%" if np.isfinite(selected_value) and np.isfinite(sp_value) else "n/a",
            )

            st.plotly_chart(plot_backtest_values(value_long), width="stretch")
            left, right = st.columns(2)
            with left:
                st.plotly_chart(plot_return_difference(metrics), width="stretch")
            with right:
                st.plotly_chart(plot_drawdowns(value_long), width="stretch")

            st.subheader("Performance And Risk Profile")
            st.dataframe(metrics.round(2), width="stretch", hide_index=True)
            st.subheader("Greatest Value Fall And Persistent Gain/Loss Periods")
            st.dataframe(periods.round(2), width="stretch", hide_index=True)
            st.subheader("Forward What-If Simulation")
            st.markdown(
                """
                <p class='note'>
                Forward projections use the current sidebar macro parameters. Higher yields, inflation,
                recession probability, credit spreads, equity risk premium, Treasury issuance pressure,
                volatility, oil prices, dollar strength, labor stress, tariffs, tax pressure, regulatory
                pressure, and valuation-reset pressure reduce expected returns; stronger EPS revisions,
                AI revenue conversion, AI capex, power demand, consumer health, housing, semiconductor
                cycle, yield-curve normalization, and liquidity improve expected returns based on each
                asset's sensitivity profile.
                </p>
                """,
                unsafe_allow_html=True,
            )
            if not forward_percentiles.empty:
                st.plotly_chart(plot_forward_what_if(forward_percentiles), width="stretch")
                st.dataframe(forward_summary.round(2), width="stretch", hide_index=True)
            st.subheader("Benchmark And JPM Strategy Proxy Map")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"JPM strategy": strategy, "Public proxy": proxy}
                        for strategy, proxy in JPM_PROXY_MAP.items()
                    ]
                ),
                width="stretch",
                hide_index=True,
            )

            st.download_button(
                "Download backtest metrics",
                data=metrics.to_csv(index=False),
                file_name="finance_backtest_metrics.csv",
                mime="text/csv",
            )
            st.download_button(
                "Download drawdown periods",
                data=periods.to_csv(index=False),
                file_name="finance_backtest_periods.csv",
                mime="text/csv",
            )
            st.download_button(
                "Download forward what-if summary",
                data=forward_summary.to_csv(index=False),
                file_name="finance_forward_what_if_summary.csv",
                mime="text/csv",
            )

    with tabs[3]:
        st.subheader("Sectorwise Innovators With Microsoft-Like Growth And Lower Downside Risk")
        st.markdown(
            """
            <p class='note'>
            This model ranks potential innovators by growth relative to Microsoft, FCF quality, balance-sheet
            strength, moat, innovation intensity, valuation discipline, and long-term downside risk. It is a
            screening model, not a buy list.
            </p>
            """,
            unsafe_allow_html=True,
        )
        selected_cap_tiers = st.multiselect(
            "Cap tiers",
            options=sorted(innovators["Cap tier"].unique()),
            default=[tier for tier in sorted(innovators["Cap tier"].unique()) if "Mid" in tier or "Small" in tier],
        )
        filtered_innovators = innovators[innovators["Cap tier"].isin(selected_cap_tiers)] if selected_cap_tiers else innovators
        left, right = st.columns([1.2, 1])
        with left:
            st.plotly_chart(plot_innovator_scatter(filtered_innovators), width="stretch")
        with right:
            st.plotly_chart(plot_sector_innovators(filtered_innovators), width="stretch")
        st.subheader("Top Innovator Candidates")
        st.dataframe(
            filtered_innovators[
                [
                    "Ticker",
                    "Company",
                    "Cap tier",
                    "Sector",
                    "Industry",
                    "Growth vs MSFT %",
                    "Macro-adjusted innovator score",
                    "Long-term downside risk",
                    "FCF quality",
                    "Balance sheet",
                    "Moat",
                    "Innovator class",
                ]
            ].round(2),
            width="stretch",
            hide_index=True,
        )
        st.subheader("Sector And Industry Breakdown")
        st.dataframe(
            filtered_innovators.groupby(["Cap tier", "Sector", "Industry"], as_index=False)
            .agg(
                Candidates=("Ticker", "count"),
                Avg_growth_vs_msft=("Growth vs MSFT %", "mean"),
                Avg_score=("Macro-adjusted innovator score", "mean"),
                Avg_downside_risk=("Long-term downside risk", "mean"),
            )
            .sort_values("Avg_score", ascending=False)
            .round(2),
            width="stretch",
            hide_index=True,
        )

    with tabs[4]:
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

    with tabs[5]:
        st.plotly_chart(plot_3d_surface(inputs), width="stretch")

    with tabs[6]:
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

    with tabs[7]:
        st.subheader("Scenario-adjusted watchlist")
        st.dataframe(scored.round(2), width="stretch", hide_index=True)
        st.subheader("Innovator screen")
        st.dataframe(innovators.round(2), width="stretch", hide_index=True)
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
