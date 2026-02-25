"""
Agent 1: Copy & Image Injection Agent
======================================

Automatically generates complete landing pages by filling predefined
HTML templates with marketing copy and images.

Input:
    - Template ID (references a pre-analyzed HTML template)
    - Raw advertorial copy (unstructured text from copywriters)

Output:
    - Complete HTML page with all placeholders filled
    - Summary of what was placed where
"""

from app.services.agents.copy_injection.agent import CopyInjectionAgent
from app.services.agents.copy_injection.schemas import (
    CopyInjectionInput,
    CopyInjectionOutput,
    CopyStructureAnalysis,
    GroupCount,
    PlaceholderContent,
    PlaceholderMapping,
    PlacementSummary,
    TemplateStructure,
    TemplateSummary,
)
from app.services.agents.copy_injection.template_service import TemplateService

__all__ = [
    "CopyInjectionAgent",
    "CopyInjectionInput",
    "CopyInjectionOutput",
    "CopyStructureAnalysis",
    "GroupCount",
    "PlaceholderContent",
    "PlaceholderMapping",
    "PlacementSummary",
    "TemplateService",
    "TemplateStructure",
    "TemplateSummary",
]

