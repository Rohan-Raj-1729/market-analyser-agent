# Market Analyser Agent

A multi-agent portfolio analysis system built with Google's Agent Development Kit (ADK) that performs comprehensive stock analysis by combining technical analysis, fundamental analysis, and market sentiment. The system validates stocks, analyzes them through multiple lenses, and provides portfolio allocation recommendations.

## Problem Statement

Analyzing stocks manually is laborious because it requires significant time investment in gathering market data, computing technical indicators, analyzing financial statements, researching market sentiment, and synthesizing all this information into actionable investment decisions. The repetitive nature of fetching data from multiple sources, calculating metrics, and maintaining consistency across different analysis methodologies can quickly become mentally exhausting and error-prone. Manual stock analysis also struggles to scale when evaluating multiple stocks simultaneously, forcing analysts to choose between depth and breadth or invest in hiring additional research staff. The complexity increases exponentially when trying to combine technical, fundamental, and sentiment analysis into a cohesive portfolio recommendation. Automation can streamline data gathering, compute complex metrics consistently, analyze financial statements systematically, monitor market sentiment in real-time, and synthesize multi-dimensional insights, allowing human analysts to focus their expertise on strategic interpretation, risk assessment, and making nuanced investment decisions that truly require human judgment.

## Solution Statement

Agents can automatically validate stock tickers by checking liquidity requirements and financial data availability, ensuring only suitable candidates proceed to analysis. They can gather historical price data from multiple sources, compute comprehensive technical indicators including risk metrics, momentum signals, and trend analysis, significantly reducing the time spent on manual calculations. Additionally, agents can retrieve and analyze financial statements systematically, calculating key ratios like ROIC, FCF yield, and debt-to-equity automatically. They can monitor market sentiment by searching latest news, performing sentiment analysis, and generating investment verdicts. Most importantly, agents can synthesize all these multi-dimensional analyses—technical, fundamental, and sentiment—into coherent portfolio allocation recommendations with percentage allocations and investment timelines, transforming stock analysis from a manual, fragmented process into a streamlined, data-driven workflow that scales effortlessly across multiple stocks.

## Architecture

Core to Market Analyser Agent is the `root_agent` -- a prime example of a multi-agent system. It's not a monolithic application but an ecosystem of specialized agents, each contributing to a different stage of the stock analysis and portfolio management process. This modular approach, facilitated by Google's Agent Development Kit, allows for a sophisticated and robust workflow. The central orchestrator of this system is the `root_agent`, constructed as a `SequentialAgent` that coordinates the entire analysis pipeline.

The `root_agent` is constructed using the `SequentialAgent` class from the Google ADK. Its definition highlights several key parameters: the name, the sub-agents it orchestrates in sequence, and the overall workflow it manages. Crucially, it coordinates three major stages: universe validation, parallel multi-dimensional analysis, and portfolio synthesis.

The real power of the Market Analyser Agent lies in its team of specialized sub-agents, each an expert in its domain. The system begins with the **Universe Definition Agent**, which validates and filters stock tickers. This is followed by a **Parallel Agent** that orchestrates three simultaneous analysis agents: the **Technical Analyst Agent**, **Fundamental Analyst Agent**, and **Market Sentiment Analyst Agent**. Finally, the **Portfolio Manager Agent** synthesizes all the gathered intelligence into actionable portfolio recommendations.

The system is built using Google ADK's agent framework with the following structure:

The system is built using Google ADK's agent framework with the following structure:

```
Sequential Agent (root_agent)
├── Universe Definition Agent (Sequential)
│   └── Validates tickers for liquidity and financial data availability
├── Parallel Agent (market_analyst)
│   ├── Technical Analyst Agent
│   ├── Fundamental Analyst Agent
│   └── Market Sentiment Analyst Agent
└── Portfolio Manager Agent
    └── Synthesizes all analyses and provides allocation recommendations
```

Each agent in this ecosystem is defined using the `LlmAgent` or `Agent` class from Google ADK, with specific instructions that govern its behavior, specialized tools for data retrieval and computation, and output keys that allow results to flow seamlessly through the system. The `agent_runner`, configured with session and memory services, manages the execution of this multi-agent workflow, maintaining state and context throughout the analysis process.

### Agent Flow

1. **Universe Definition Agent (UDA)**: Validates input tickers by checking:
   - Liquidity (minimum average volume: 200,000)
   - Financial statement coverage (minimum 5 years of data)
   - Returns validated tickers with market cap information

2. **Parallel Analysis Agents** (run simultaneously):
   - **Technical Analyst Agent (TA)**: Computes technical indicators including:
     - Annual return and volatility
     - Sharpe ratio
     - Maximum drawdown
     - Value at Risk (VaR) and Expected Shortfall (ES)
     - Momentum indicators (1m, 3m, 6m)
     - Moving average slopes
     - Liquidity metrics (dollar volume, Amihud illiquidity)
   
   - **Fundamental Analyst Agent (FAA)**: Analyzes financial statements:
     - Income statements, balance sheets, cash flow statements
     - ROIC (Return on Invested Capital)
     - FCF Yield (Free Cash Flow Yield)
     - Debt-to-Equity ratio
     - Financial health assessment
   
   - **Market Sentiment Analyst Agent (MSA)**: Performs sentiment analysis:
     - Searches latest news for each ticker
     - Provides investment verdicts: STRONG BUY, BUY, HOLD, SELL, STRONG SELL
     - Short-term and long-term outlook

3. **Portfolio Manager Agent (PM)**: Synthesizes all analyses to provide:
   - Percentage allocation recommendations for each validated ticker
   - Short-term and long-term investment plans

## Features

- **Multi-layered Analysis**: Combines technical, fundamental, and sentiment analysis
- **Data Validation**: Ensures only liquid stocks with sufficient historical data are analyzed
- **Comprehensive Metrics**: Calculates 15+ technical indicators and multiple financial ratios
- **Parallel Processing**: Runs three analysis agents simultaneously for efficiency
- **Portfolio Optimization**: Provides actionable allocation recommendations

## Requirements

### Dependencies

- `google-adk` - Google Agent Development Kit
- `yfinance` - Yahoo Finance data fetching
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `python-dotenv` - Environment variable management

### Environment Variables

Create a `.env` file in the project root with:

```
GOOGLE_API_KEY=your_google_api_key_here
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install google-adk yfinance pandas numpy python-dotenv
   ```
3. Set up your `.env` file with your Google API key
4. Run the main script

### Running the Example

```bash
python main.py
```

This will analyze the default tickers: `["CAT", "GS", "NEE", "BMY", "BKNG"]`

## Project Structure

```
market-analyser-agent/
├── main.py                          # Entry point and example usage
├── main_agent.py                    # Agent orchestration and runner setup
├── common/
│   └── google_adk_setup.py          # ADK configuration (retry, session, memory)
├── universe_definition_agent/
│   ├── agent.py                     # UDA agent definition
│   └── tools.py                     # Validation tools (liquidity, financials)
├── technical_analyst_agent/
│   ├── agent.py                     # TA agent definition
│   └── tools.py                     # Technical metrics computation
├── fundamentals_analyst_agent/
│   ├── agent.py                     # FAA agent definition
│   └── tools.py                     # Financial statement analysis
├── market_sentiment_analyst_agent/
│   └── agent.py                     # MSA agent definition
└── portfolio_manager_agent/
    └── agent.py                     # PM agent definition
```

## Agent Details

### Universe Definition Agent

**Purpose**: Clean and validate stock tickers before analysis

**Tools**:
- `validate_universe(tickers, min_avg_volume, min_financial_years)`: Validates tickers for liquidity and financial data availability
- `check_liquidity(ticker, min_avg_volume)`: Checks if stock meets minimum volume requirements
- `check_financial_statement_coverage(ticker, min_years)`: Verifies availability of historical financial statements
- `get_symbol_info(ticker)`: Retrieves basic market information (sector, industry, market cap, etc.)

**Output**: Validated tickers with market cap, average volume, and years of financial data available

### Technical Analyst Agent

**Purpose**: Analyze price patterns, momentum, and risk metrics

**Tools**:
- `compute_technical_metrics(ticker_list)`: Computes comprehensive technical indicators for multiple tickers
- `get_prices(ticker, period, interval)`: Fetches historical price data
- `compute_stock_metrics(df, market_returns)`: Calculates risk and return metrics

**Metrics Computed**:
- Return metrics: Annual return, volatility, Sharpe ratio
- Risk metrics: Max drawdown, VaR (95%), Expected Shortfall (95%)
- Momentum: 1-month, 3-month, 6-month momentum
- Trend: Moving average slope (MA50)
- Liquidity: Average dollar volume, Amihud illiquidity measure
- Market correlation: Beta, R-squared (if market returns provided)

### Fundamental Analyst Agent

**Purpose**: Evaluate company financial health and profitability

**Tools**:
- `run_fundamental_analysis(ticker, market_cap)`: Complete fundamental analysis workflow
- `get_income_statement(ticker)`: Retrieves income statement data
- `get_balance_sheet(ticker)`: Retrieves balance sheet data
- `get_cash_flow(ticker)`: Retrieves cash flow statement data
- `compute_roic(income_df, balance_df)`: Calculates Return on Invested Capital
- `compute_fcf_yield(cashflow_df, market_cap)`: Calculates Free Cash Flow Yield
- `compute_debt_to_equity(balance_df)`: Calculates Debt-to-Equity ratio

**Output**: Financial health summary, metrics table, and risk assessment

### Market Sentiment Analyst Agent

**Purpose**: Analyze market sentiment from news and market outlook

**Tools**:
- `google_search`: Searches for latest news and information about tickers

**Output**: Investment verdicts (STRONG BUY, BUY, HOLD, SELL, STRONG SELL) for both short-term and long-term horizons

### Portfolio Manager Agent

**Purpose**: Synthesize all analyses and provide portfolio recommendations

**Input**: Receives outputs from all previous agents via session state

**Output**:
- Percentage allocation recommendations for each validated ticker
- Short-term and long-term investment plans

## Configuration

### Retry Configuration

The system includes retry logic for API calls (configured in `common/google_adk_setup.py`):
- Maximum 5 retry attempts
- Exponential backoff with base 7
- Retries on HTTP errors: 429, 500, 503, 504

### Model Configuration

All agents use Google's Gemini 2.5 Flash Lite model for fast, cost-effective inference.

## Output Format

The system returns a comprehensive analysis including:

1. **Universe Definition**: List of validated and excluded tickers with reasons
2. **Technical Analysis**: Technical metrics and trend analysis for each ticker
3. **Fundamental Analysis**: Financial health assessment and key ratios
4. **Market Sentiment**: News-based sentiment and investment verdicts
5. **Portfolio Allocation**: Recommended capital allocation percentages and investment plans

## Limitations

- Requires valid stock tickers that are available on Yahoo Finance
- Minimum liquidity requirements (200k average volume) may exclude some stocks
- Requires at least 5 years of financial statement data
- Market sentiment analysis depends on available news sources
- Analysis is based on historical data and may not predict future performance

## License

See LICENSE file for details.

## Contributing

This is a capstone project for learning LangGraph and multi-agent systems. Contributions and improvements are welcome!
