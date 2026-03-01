"""
Copy Injection Agent
====================

Agent 1: Fills HTML templates with advertorial copy and generated images.
"""

from app.services.agents.copy_injection.agent import CopyInjectionAgent
from app.services.agents.copy_injection.schemas import (
    CopyInjectionInput,
    CopyInjectionOutput,
    TemplateSummary,
    PlacementSummary,
    ParsedCopy,
)
from app.services.agents.copy_injection.template_service import TemplateService

__all__ = [
    "CopyInjectionAgent",
    "CopyInjectionInput",
    "CopyInjectionOutput",
    "TemplateSummary",
    "PlacementSummary",
    "ParsedCopy",
    "TemplateService",
]

