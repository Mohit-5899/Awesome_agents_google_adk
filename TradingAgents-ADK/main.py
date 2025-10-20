"""
TradingAgents ADK - Main entry point
Run multi-agent trading analysis using Google ADK
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from google import genai
from google.genai import types
from tradingagents.agent import root_agent
from tradingagents.config.default_config import ADK_CONFIG
from tradingagents.dataflows.config import set_config
from tradingagents.default_config import DEFAULT_CONFIG

load_dotenv()


def run_trading_analysis(ticker: str, trade_date: str = None):
    """
    Run trading analysis for a given ticker using ADK agents
    
    Args:
        ticker: Stock ticker symbol (e.g., 'NVDA', 'AAPL')
        trade_date: Trading date in YYYY-MM-DD format (defaults to today)
    
    Returns:
        Trading decision and analysis
    """
    if trade_date is None:
        trade_date = datetime.now().strftime("%Y-%m-%d")
    
    set_config(DEFAULT_CONFIG)
    
    print(f"\n{'='*80}")
    print(f"TradingAgents ADK - Multi-Agent Trading Analysis")
    print(f"{'='*80}")
    print(f"Ticker: {ticker}")
    print(f"Date: {trade_date}")
    print(f"{'='*80}\n")
    
    client = genai.Client(
        vertexai=False,
        api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    )
    
    query = f"""Analyze {ticker} for trading on {trade_date}. 
    
Please coordinate with all analyst agents to:
1. Gather technical market analysis
2. Review recent news and macroeconomic trends
3. Assess social sentiment
4. Evaluate company fundamentals

Then provide your final trading recommendation."""
    
    print("Starting multi-agent analysis...")
    print(f"Query: {query}\n")
    
    response = client.agentic.generate_content(
        model=root_agent.model,
        contents=query,
        config=types.GenerateContentConfig(
            agent=root_agent,
            temperature=0.7,
        )
    )
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80 + "\n")
    
    for part in response.candidates[0].content.parts:
        print(part.text)
    
    return response


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="TradingAgents ADK - Multi-Agent Trading Analysis"
    )
    parser.add_argument(
        "ticker",
        type=str,
        help="Stock ticker symbol (e.g., NVDA, AAPL, TSLA)"
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Trading date in YYYY-MM-DD format (defaults to today)"
    )
    
    args = parser.parse_args()
    
    run_trading_analysis(args.ticker, args.date)


if __name__ == "__main__":
    main()
