"""Email Assistant Agent for ADK Web UI.

This module provides the root_agent required by ADK's web interface.
It imports from the centralized AgentFactory to avoid code duplication.
"""
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.email_agent import AgentFactory

# Create the root agent using the factory (required by ADK web)
# This ensures consistent agent configuration across CLI and Web interfaces
root_agent = AgentFactory.create_agent()
