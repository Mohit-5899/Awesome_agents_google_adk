"""
Manager agents for orchestrating team decisions
"""

from .research_manager import research_manager_agent
from .risk_manager import risk_manager_agent

__all__ = ["research_manager_agent", "risk_manager_agent"]