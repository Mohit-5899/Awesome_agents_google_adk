"""
ADK Configuration for TradingAgents
"""

import os

ADK_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results_adk"),
    
    "model": "gemini-2.0-flash-exp",
    
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "alpha_vantage",
        "news_data": "alpha_vantage",
    },
}
