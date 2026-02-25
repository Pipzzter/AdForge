"""
Base Agent Class
================

Abstract base class that all agents inherit from.
Provides common functionality for LLM interaction and HTML processing.
"""

import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

logger = logging.getLogger(__name__)

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class BaseAgent(ABC, Generic[InputT, OutputT]):
    """
    Abstract base class for all AI agents.

    Each agent processes input through an LLM and returns structured output.
    Subclasses must implement the `process` method.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        logger.info("Initialized agent: %s", name)

    @abstractmethod
    async def process(self, input_data: InputT) -> OutputT:
        """
        Process input data and return structured output.

        Args:
            input_data: Agent-specific input model

        Returns:
            Agent-specific output model
        """
        pass

    @abstractmethod
    def build_prompt(self, input_data: InputT) -> str:
        """
        Build the prompt to send to the LLM.

        Args:
            input_data: Agent-specific input model

        Returns:
            Formatted prompt string
        """
        pass

