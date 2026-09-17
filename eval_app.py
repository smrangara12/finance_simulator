from __future__ import annotations

from streamlit.testing.v1 import AppTest

from app import MarketInputs, build_evaluation, macro_adjusted_frame, preset_values, simulate_paths


def inputs_from_preset(name: str) -> MarketInputs:
    values = preset_values(name)
    return MarketInputs(
        horizon_years=3,
        starting_capital=100_000,
        ten_year_yield=values["ten_year_yield"],
        inflation=values["inflation"],
        recession_probability=values["recession_probability"],
        ai_capex_growth=values["ai_capex_growth"],
        power_demand_growth=values["power_demand_growth"],
        credit_spread=values["credit_spread"],
        dollar_strength=values["dollar_strength"],
        oil_price=values["oil_price"],
        liquidity_impulse=values["liquidity_impulse"],
        valuation_reset=values["valuation_reset"],
        seed=77,
    )


def run_model_evals() -> None:
    presets = [
        "Base AI buildout",
        "Sticky inflation and 5% rates",
        "Recession/liquidity squeeze",
        "Rate cuts and growth rebound",
        "AI capex digestion",
        "Grid and defense rotation",
    ]
    for preset in presets:
        inputs = inputs_from_preset(preset)
        scored = macro_adjusted_frame(inputs)
        paths, portfolio = simulate_paths(inputs)
        eval_df = build_evaluation(inputs, scored, portfolio)

        assert not scored.empty, f"{preset}: scored frame is empty"
        assert not paths.empty, f"{preset}: paths frame is empty"
        assert not portfolio.empty, f"{preset}: portfolio frame is empty"
        assert not eval_df.empty, f"{preset}: eval frame is empty"
        assert scored["Scenario score"].between(0, 100).all(), f"{preset}: scenario scores out of range"
        assert portfolio["Portfolio value"].iloc[-1] > 0, f"{preset}: portfolio value must stay positive"
        assert set(eval_df["Result"]).issubset({"Pass", "Warn", "Fail"}), f"{preset}: invalid eval result"

        top = scored.iloc[0]["Ticker"]
        final_value = portfolio.iloc[-1]["Portfolio value"]
        print(f"{preset}: top={top}; final=${final_value:,.0f}; eval={eval_df['Result'].value_counts().to_dict()}")


def run_streamlit_eval() -> None:
    app_test = AppTest.from_file("app.py")
    app_test.run(timeout=20)
    assert not app_test.exception, [exception.value for exception in app_test.exception]
    print("Streamlit execution: no exceptions")


if __name__ == "__main__":
    run_model_evals()
    run_streamlit_eval()
