# TOOLS #
import yfinance as yf


def get_symbol_info(ticker: str):
    """
    Fetches market info such as sector, industry, market cap, average volume, etc.
    """
    try:
        data = yf.Ticker(ticker).info
        return {
            "ticker": ticker,
            "sector": data.get("sector"),
            "industry": data.get("industry"),
            "market_cap": data.get("marketCap"),
            "avg_volume": data.get("averageVolume"),
            "exchange": data.get("exchange"),
            "short_name": data.get("shortName"),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def check_liquidity(ticker: str, min_avg_volume: int = 200000):
    """
    Basic liquidity test: flags stocks that are too illiquid to include.
    """
    info = get_symbol_info(ticker)
    vol = info.get("avg_volume")

    if vol is None:
        return {"ticker": ticker, "liquid": False, "reason": "Missing volume data"}

    return {
        "ticker": ticker,
        "liquid": vol >= min_avg_volume,
        "avg_volume": vol,
        "reason": "OK" if vol >= min_avg_volume else f"Avg volume too low: {vol}"
    }


def check_financial_statement_coverage(ticker: str, min_years: int = 5):
    """
    Ensures the company has multi-year financial statements.
    """
    stock = yf.Ticker(ticker)

    try:
        bs = stock.balance_sheet   # columns are years
        is_ = stock.financials
        cf = stock.cashflow
    except Exception as e:
        return {"ticker": ticker, "ok": False, "reason": f"API error: {str(e)}"}

    years_bs = bs.shape[1] if bs is not None else 0
    years_is = is_.shape[1] if is_ is not None else 0
    years_cf = cf.shape[1] if cf is not None else 0

    # Check consistency
    min_available_years = min(years_bs, years_is, years_cf)

    return {
        "ticker": ticker,
        "ok": min_available_years >= min_years,
        "years_available": min_available_years,
        "reason": "OK" if min_available_years >= min_years else f"Only {min_available_years} years of data."
    }


def validate_universe(tickers, min_avg_volume=200000, min_financial_years=5):
    """
    Runs liquidity + financial coverage validation.
    """
    validated = []
    excluded = []

    for t in tickers:
        liq = check_liquidity(t, min_avg_volume)
        fin = check_financial_statement_coverage(t, min_financial_years)

        if liq["liquid"] and fin["ok"]:
            validated.append({
                "ticker": t,
                "market_cap": get_symbol_info(t).get("market_cap"),
                "avg_volume": liq["avg_volume"],
                "years_financials": fin["years_available"]
            })
        else:
            excluded.append({
                "ticker": t,
                "liquidity_check": liq,
                "financials_check": fin
            })

    return {"validated": validated, "excluded": excluded}
