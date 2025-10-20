"""
Risk Management team agents for risk debate
"""

from .aggressive_debator import aggressive_debator_agent
from .conservative_debator import conservative_debator_agent
from .neutral_debator import neutral_debator_agent

__all__ = ["aggressive_debator_agent", "conservative_debator_agent", "neutral_debator_agent"]