"""
Schemas for Copy & Image Injection Agent
=========================================

Pydantic models for input/output of Agent 1.
"""

from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Template structure schemas (read from JSON files)
# ---------------------------------------------------------------------------

class TemplateGroup(BaseModel):
    """A repeatable group of placeholders in a template."""

    label: str = Field(..., description="Group name, e.g. 'reviews'")
    count: int = Field(..., description="Number of slots in the template")
    placeholders: list[str] = Field(..., description="Exact placeholder strings in order")
    container_class: Optional[str] = Field(
        None, description="CSS class of the card wrapper div used for cloning"
    )


class TemplateStructure(BaseModel):
    """Full pre-analyzed structure of one HTML template."""

    id: str
    name: str
    file: str
    groups: list[TemplateGroup]
    singletons: list[str]


class TemplateSummary(BaseModel):
    """Lightweight summary returned to the frontend dropdown."""

    id: str
    name: str


# ---------------------------------------------------------------------------
# LLM Call 1 — count how many of each group the copy contains
# ---------------------------------------------------------------------------

class GroupCount(BaseModel):
    """How many items of one group the copy actually contains."""

    label: str = Field(..., description="Group label matching TemplateGroup.label")
    count: int = Field(..., description="Number of items found in the raw copy")


class CopyStructureAnalysis(BaseModel):
    """Result of LLM Call 1 — counts per group from the raw copy."""

    groups: list[GroupCount] = Field(
        default_factory=list,
        description="Count for each repeatable group",
    )


# ---------------------------------------------------------------------------


class PlaceholderContent(BaseModel):
    """Content generated for a single placeholder."""

    placeholder: str = Field(
        ...,
        description="The original placeholder text (e.g., '[Headline goes here]')",
    )
    content: str = Field(
        ...,
        description="The generated content to replace the placeholder",
    )


class PlaceholderMapping(BaseModel):
    """Mapping of all placeholders to their generated content."""

    placeholders: list[PlaceholderContent] = Field(
        default_factory=list,
        description="List of placeholder-to-content mappings",
    )


# ---------------------------------------------------------------------------
# Agent input / output
# ---------------------------------------------------------------------------

class CopyInjectionInput(BaseModel):
    """Input for Copy & Image Injection Agent."""

    template_id: str = Field(
        ...,
        description="ID of the pre-analyzed template, e.g. 'template_001'",
        min_length=1,
    )
    raw_copy: str = Field(
        ...,
        description="Raw advertorial copy from copywriters (unstructured text)",
        min_length=1,
    )
    product_name: Optional[str] = Field(
        None,
        description="Product name for context (optional)",
    )
    product_category: Optional[str] = Field(
        None,
        description="Product category for context (optional)",
    )


class PlacementSummary(BaseModel):
    """Summary of a single placeholder that was filled."""

    placeholder: str = Field(..., description="The placeholder that was filled")
    content_preview: str = Field(
        ..., description="Preview of the content that was placed (truncated)"
    )
    filled: bool = Field(
        default=True, description="Whether the placeholder was successfully filled"
    )


class CopyInjectionOutput(BaseModel):
    """Output from Copy & Image Injection Agent."""

    html: str = Field(..., description="Complete HTML with all placeholders filled")
    placeholders_found: list[str] = Field(
        default_factory=list,
        description="List of all placeholders found in the template",
    )
    placements: list[PlacementSummary] = Field(
        default_factory=list,
        description="Summary of what was placed where",
    )
    success: bool = Field(default=True, description="Whether processing succeeded")
    error_message: Optional[str] = Field(
        None, description="Error message if processing failed"
    )

