"""
Copy Injection Agent Router
============================

API endpoints for Agent 1 - Copy & Image Injection.
"""

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.agents.copy_injection import (
    CopyInjectionAgent,
    CopyInjectionInput,
    CopyInjectionOutput,
    TemplateService,
    TemplateSummary,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/copyinjection", tags=["agents"])


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

@router.get("/templates", response_model=list[TemplateSummary])
async def get_templates() -> list[TemplateSummary]:
    """Return all available templates for the frontend dropdown."""
    logger.info("GET /copyinjection/templates")
    return TemplateService.get_all()




# ---------------------------------------------------------------------------
# Legacy placeholder extraction (kept for debugging)
# ---------------------------------------------------------------------------

class ExtractPlaceholdersInput(BaseModel):
    """Input for placeholder extraction."""

    html_template: str = Field(..., description="HTML template to extract placeholders from")


class ExtractPlaceholdersOutput(BaseModel):
    """Output from placeholder extraction."""

    placeholders: list[str] = Field(default_factory=list)
    count: int = Field(default=0)


@router.post("/extract-placeholders", response_model=ExtractPlaceholdersOutput)
async def extract_placeholders(payload: ExtractPlaceholdersInput) -> ExtractPlaceholdersOutput:
    """Extract all placeholders from an HTML template (debug utility)."""
    logger.info(
        "POST /copyinjection/extract-placeholders: template_length=%d",
        len(payload.html_template),
    )
    agent = CopyInjectionAgent()
    placeholders = agent.extract_placeholders(payload.html_template)
    return ExtractPlaceholdersOutput(placeholders=placeholders, count=len(placeholders))


# ---------------------------------------------------------------------------
# Main injection endpoint
# ---------------------------------------------------------------------------

@router.post("", response_model=CopyInjectionOutput)
async def inject_copy(payload: CopyInjectionInput) -> CopyInjectionOutput:
    """
    Fill a template with marketing copy and return the generated HTML + metadata.
    Preview and ZIP packaging are handled entirely client-side.
    """
    logger.info(
        "POST /copyinjection: template_id=%s, copy_length=%d",
        payload.template_id,
        len(payload.raw_copy),
    )
    agent = CopyInjectionAgent()
    return await agent.process(payload)

