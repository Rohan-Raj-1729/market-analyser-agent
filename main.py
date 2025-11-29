from dotenv import load_dotenv
import os
import asyncio

from main_agent import agent_runner


async def main(tickers_list: list[str]):
    prompt = (
        f"Analyse the following stocks: {tickers_list}. "
        "Suggest which one to buy for the best returns for next 6 months "
        "by combining all scores"
    )
    response = await agent_runner.run_debug(prompt)
    return response

# --- Demonstration of the Agent ---
if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    random_5_tickers = ["CAT", "GS", "NEE", "BMY", "BKNG"]
    response = asyncio.run(main(random_5_tickers))
