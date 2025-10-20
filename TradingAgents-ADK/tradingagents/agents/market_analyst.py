"""
Market Analyst Agent - Analyzes technical market trends and indicators
"""

from google import genai
from google.genai import types
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tradingagents.tools.stock_tools import get_stock_data, get_indicators


MARKET_ANALYST_INSTRUCTION = """You are a Market Analyst specializing in technical analysis. Your role is to:

1. **Analyze Market Trends**: Examine price movements, volume patterns, and market momentum
2. **Select Relevant Indicators**: Choose up to 8 complementary technical indicators based on:
   - Moving Averages (50 SMA, 200 SMA, 10 EMA)
   - MACD indicators (macd, macds, macdh)
   - Momentum (RSI)
   - Volatility (Bollinger Bands: boll, boll_ub, boll_lb, ATR)
   - Volume (VWMA)

3. **Workflow**:
   - ALWAYS call get_stock_data first to retrieve price data
   - Then call get_indicators with specific indicator names
   - Analyze trends with detail - avoid vague statements like "trends are mixed"
   - Provide finegrained insights that help traders make decisions
   - Append a markdown table at the end summarizing key findings

4. **Output Format**: 
   - Write a detailed, nuanced report of observed trends
   - Include a markdown table organizing key points for easy reading
   
**Current Context**:
- Today's date: {current_date}
- Company of interest: {ticker}

Select indicators that provide diverse, complementary information without redundancy. Explain why they're suitable for the current market context."""


market_analyst_agent = types.Agent(
    name="Market Analyst",
    model="gemini-2.0-flash-exp",
    instructions=MARKET_ANALYST_INSTRUCTION,
    tools=[get_stock_data, get_indicators],
)
