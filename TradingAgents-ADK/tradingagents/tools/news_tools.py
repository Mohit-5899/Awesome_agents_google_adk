"""
News and sentiment data tools for ADK agents
"""

from typing import Annotated
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tradingagents.dataflows.interface import route_to_vendor


def get_news(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve news data for a given ticker symbol.
    Uses the configured news_data vendor.
    
    Args:
        ticker: Ticker symbol
        start_date: Start date in yyyy-mm-dd format
        end_date: End date in yyyy-mm-dd format
    
    Returns:
        A formatted string containing news data
    """
    return route_to_vendor("get_news", ticker, start_date, end_date)


def get_global_news(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "Number of days to look back"] = 7,
    limit: Annotated[int, "Maximum number of articles to return"] = 5,
) -> str:
    """
    Retrieve global news data.
    Uses the configured news_data vendor.
    
    Args:
        curr_date: Current date in yyyy-mm-dd format
        look_back_days: Number of days to look back (default 7)
        limit: Maximum number of articles to return (default 5)
    
    Returns:
        A formatted string containing global news data
    """
    return route_to_vendor("get_global_news", curr_date, look_back_days, limit)


def get_insider_sentiment(
    ticker: Annotated[str, "ticker symbol for the company"],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
) -> str:
    """
    Retrieve insider sentiment information about a company.
    Uses the configured news_data vendor.
    
    Args:
        ticker: Ticker symbol of the company
        curr_date: Current date you are trading at, yyyy-mm-dd
    
    Returns:
        A report of insider sentiment data
    """
    return route_to_vendor("get_insider_sentiment", ticker, curr_date)


def get_insider_transactions(
    ticker: Annotated[str, "ticker symbol"],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
) -> str:
    """
    Retrieve insider transaction information about a company.
    Uses the configured news_data vendor.
    
    Args:
        ticker: Ticker symbol of the company
        curr_date: Current date you are trading at, yyyy-mm-dd
    
    Returns:
        A report of insider transaction data
    """
    return route_to_vendor("get_insider_transactions", ticker, curr_date)
