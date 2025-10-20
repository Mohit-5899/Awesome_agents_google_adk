"""
Fundamental data tools for ADK agents
"""

from typing import Annotated
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tradingagents.dataflows.interface import route_to_vendor


def get_fundamentals(
    ticker: Annotated[str, "ticker symbol"],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
) -> str:
    """
    Retrieve comprehensive fundamental data for a given ticker symbol.
    Uses the configured fundamental_data vendor.
    
    Args:
        ticker: Ticker symbol of the company
        curr_date: Current date you are trading at, yyyy-mm-dd
    
    Returns:
        A formatted report containing comprehensive fundamental data
    """
    return route_to_vendor("get_fundamentals", ticker, curr_date)


def get_balance_sheet(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[str, "reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"] = None,
) -> str:
    """
    Retrieve balance sheet data for a given ticker symbol.
    Uses the configured fundamental_data vendor.
    
    Args:
        ticker: Ticker symbol of the company
        freq: Reporting frequency: annual/quarterly (default quarterly)
        curr_date: Current date you are trading at, yyyy-mm-dd
    
    Returns:
        A formatted report containing balance sheet data
    """
    return route_to_vendor("get_balance_sheet", ticker, freq, curr_date)


def get_cashflow(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[str, "reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"] = None,
) -> str:
    """
    Retrieve cash flow statement data for a given ticker symbol.
    Uses the configured fundamental_data vendor.
    
    Args:
        ticker: Ticker symbol of the company
        freq: Reporting frequency: annual/quarterly (default quarterly)
        curr_date: Current date you are trading at, yyyy-mm-dd
    
    Returns:
        A formatted report containing cash flow statement data
    """
    return route_to_vendor("get_cashflow", ticker, freq, curr_date)


def get_income_statement(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[str, "reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"] = None,
) -> str:
    """
    Retrieve income statement data for a given ticker symbol.
    Uses the configured fundamental_data vendor.
    
    Args:
        ticker: Ticker symbol of the company
        freq: Reporting frequency: annual/quarterly (default quarterly)
        curr_date: Current date you are trading at, yyyy-mm-dd
    
    Returns:
        A formatted report containing income statement data
    """
    return route_to_vendor("get_income_statement", ticker, freq, curr_date)
