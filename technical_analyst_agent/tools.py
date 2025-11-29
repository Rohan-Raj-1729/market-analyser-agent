import yfinance as yf
import numpy as np
import pandas as pd


def get_prices(ticker: str, period: str = "1y", interval: str = "1d") -> dict:
    """
    Fetch historical price data for multiple tickers.
    Returns dict: {ticker: DataFrame}
    """
    data = yf.download(ticker, period=period, interval=interval)
    data.columns = [col[0].lower() for col in data.columns]
    data.index.name = 'date'
    return data


def compute_stock_metrics(df, market_returns=None):
    """
    df: DataFrame with columns ['open','high','low','close','volume']
    market_returns: optional Series aligned to df.index for beta / R²
    """

    out = {}

    # --- BASIC RETURNS ---
    returns = df['close'].pct_change().dropna()
    out['annual_return'] = (df['close'].iloc[-1] / df['close'].iloc[0]) - 1
    out['annual_volatility'] = returns.std() * np.sqrt(252)
    out['sharpe_ratio'] = out['annual_return'] / out['annual_volatility'] if out['annual_volatility'] != 0 else np.nan

    # --- MAX DRAWDOWN ---
    roll_max = df['close'].cummax()
    drawdown = df['close'] / roll_max - 1
    out['max_drawdown'] = drawdown.min()

    # --- HISTORICAL VaR & ES ---
    out['VaR_95'] = returns.quantile(0.05)
    out['ES_95'] = returns[returns <= returns.quantile(0.05)].mean()

    # --- MOMENTUM ---
    out['momentum_6m'] = df['close'].pct_change(126).iloc[-1]  # ~6 months
    out['momentum_3m'] = df['close'].pct_change(63).iloc[-1]   # ~3 months
    out['momentum_1m'] = df['close'].pct_change(21).iloc[-1]

    # --- MOVING AVERAGE SLOPE ---
    ma50 = df['close'].rolling(50).mean()
    # slope = last MA - MA 10 days ago (simple numerical slope)
    out['slope_ma50'] = ma50.iloc[-1] - ma50.iloc[-11]

    # --- LIQUIDITY ---
    df['dollar_volume'] = df['close'] * df['volume']
    out['avg_dollar_volume'] = df['dollar_volume'].mean()

    # Amihud Illiquidity: |r| / $vol
    amihud = (returns.abs() / df['dollar_volume'].reindex(returns.index))
    out['amihud_illiquidity'] = amihud.mean()

    # --- BETA / R² (if market provided) ---
    if market_returns is not None:
        aligned = pd.concat([returns, market_returns], axis=1).dropna()
        if len(aligned) > 10:
            r = aligned.iloc[:, 0]
            m = aligned.iloc[:, 1]
            cov = np.cov(r, m)[0, 1]
            var = np.var(m)
            beta = cov / var if var != 0 else np.nan

            # R² of simple linear regression
            corr = np.corrcoef(r, m)[0, 1]
            r2 = corr**2

            out['beta'] = beta
            out['r_squared'] = r2
        else:
            out['beta'] = np.nan
            out['r_squared'] = np.nan
    else:
        out['beta'] = None
        out['r_squared'] = None

    for key, val in out.items():
        if isinstance(val, np.float64):
            out[key] = round(float(val), 4)
    return out


def compute_technical_metrics(ticker_list: list[str]):
    """
    Computes a comprehensive set of technical and statistical metrics for a given list of stock tickers.

    This tool fetches 1 year of historical data for the provided tickers and calculates
    key indicators including Sharpe Ratio, Sortino Ratio, Volatility, RSI, and Moving Averages.
    It is useful for screening assets or analyzing portfolio components.

    Args:
        ticker_list (list[str]): A list of stock ticker symbols (e.g., ['AAPL', 'MSFT', 'GOOG']).

    Returns:
        pd.DataFrame: A DataFrame containing the calculated metrics for each ticker.
                      Columns include: 'ticker', 'annual_return', 'annual_volatility',
                      'sharpe_ratio', 'max_drawdown', 'VaR_95', 'ES_95', 'momentum_6m',
                      'momentum_3m', 'momentum_1m', 'slope_ma50', 'avg_dollar_volume',
    """
    try:
        techincal_metrics: list = []
        for ticker in ticker_list:
            metrics_for_ticker: dict = compute_stock_metrics(get_prices(ticker, '1y'))
            metrics_for_ticker['ticker'] = ticker
            techincal_metrics.append(metrics_for_ticker)
        technical_metrics_df: pd.Dataframe = pd.DataFrame(techincal_metrics)
        return technical_metrics_df[['ticker', 'annual_return', 'annual_volatility',
                            'sharpe_ratio', 'max_drawdown', 'VaR_95', 'ES_95', 'momentum_6m',
                            'momentum_3m', 'momentum_1m', 'slope_ma50', 'avg_dollar_volume']].to_dict('records')
    except:
        return {"status": "error"}
