import yfinance as yf
import pandas as pd

def get_income_statement(ticker: str):
    """
    Fetches the income statement (multi-year).
    Returns: DataFrame or {"error": "..."}
    """
    try:
        data = yf.Ticker(ticker).financials  # Income statement
        if data is None or data.empty:
            return {"error": "No income statement data available."}
        return data
    except Exception as e:
        return {"error": str(e)}
def get_balance_sheet(ticker: str):
    """
    Fetches multi-year balance sheet data.
    """
    try:
        data = yf.Ticker(ticker).balance_sheet
        if data is None or data.empty:
            return {"error": "No balance sheet data available."}
        return data
    except Exception as e:
        return {"error": str(e)}
def get_cash_flow(ticker: str):
    """
    Fetches multi-year cash flow statement data.
    """
    try:
        data = yf.Ticker(ticker).cashflow
        if data is None or data.empty:
            return {"error": "No cash flow data available."}
        return data
    except Exception as e:
        return {"error": str(e)}
def compute_roic(income_df, balance_df):
    """
    ROIC = EBIT / Invested Capital
    Invested Capital approx = Total Assets - Current Liabilities
    """
    try:
        ebit = income_df.loc["Ebit"].iloc[0]
        total_assets = balance_df.loc["Total Assets"].iloc[0]
        current_liabilities = balance_df.loc["Total Current Liabilities"].iloc[0]

        invested_capital = total_assets - current_liabilities
        roic = ebit / invested_capital if invested_capital != 0 else None

        return {"roic": roic, "invested_capital": invested_capital}
    except Exception as e:
        return {"error": f"ROIC calc error: {str(e)}"}
def compute_fcf_yield(cashflow_df, market_cap):
    """
    FCF Yield = Free Cash Flow / Market Cap
    FCF approx = Operating Cash Flow - CapEx
    """
    try:
        ocf = cashflow_df.loc["Total Cash From Operating Activities"].iloc[0]
        capex = cashflow_df.loc["Capital Expenditures"].iloc[0]

        fcf = ocf + capex  # capex is negative in yfinance
        if market_cap is None or market_cap <= 0:
            return {"error": "Invalid market cap for FCF yield."}

        fcf_yield = fcf / market_cap
        return {"fcf": fcf, "fcf_yield": fcf_yield}
    except Exception as e:
        return {"error": f"FCF Yield calc error: {str(e)}"}
def compute_debt_to_equity(balance_df):
    """
    Debt-to-Equity = Total Debt / Total Equity
    """
    try:
        total_debt = balance_df.loc["Total Debt"].iloc[0]
        total_equity = balance_df.loc["Total Stockholder Equity"].iloc[0]

        if total_equity == 0:
            return {"error": "Equity is zero — cannot compute D/E."}

        dte = total_debt / total_equity
        return {"debt_to_equity": dte}
    except Exception as e:
        return {"error": f"D/E calc error: {str(e)}"}

def run_fundamental_analysis(ticker: str, market_cap: float) -> dict:
    """
    Full FAA workflow using all tools.
    """
    results = {}

    # --- Retrieve statements ---
    income = get_income_statement(ticker)
    balance = get_balance_sheet(ticker)
    cashflow = get_cash_flow(ticker)

    # If any critical statement fails, return early
    if "error" in income or "error" in balance or "error" in cashflow:
        return {"error": "One or more statements unavailable.", "details": results}

    # --- Compute Ratios ---
    roic = compute_roic(income, balance)
    fcf_yield = compute_fcf_yield(cashflow, market_cap)
    dte = compute_debt_to_equity(balance)

    for df in (income, balance, cashflow):
       df.columns = [int(col.year) for col in df.columns]
       df.drop(columns=[2020,2021], inplace=True)
       df.dropna(inplace=True)

    # --- Assemble results ---
    results["ticker"] = ticker
    results["market_cap"] = market_cap
    results["income"] = income.to_dict()
    results["balance"] = balance.to_dict()
    results["cashflow"] = cashflow.to_dict()
    results["roic"] = roic
    results["fcf_yield"] = fcf_yield
    results["debt_to_equity"] = dte

    return results
