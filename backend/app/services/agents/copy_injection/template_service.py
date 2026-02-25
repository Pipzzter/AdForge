"""
Template Service
================

Reads pre-analyzed template JSON files and raw HTML files from
backend/app/static/templates/.

No LLM calls — pure file I/O.
"""

import json
import logging
from pathlib import Path

from app.services.agents.copy_injection.schemas import TemplateSummary, TemplateStructure

logger = logging.getLogger(__name__)

# Absolute path to the templates folder
TEMPLATES_DIR = Path(__file__).parent.parent.parent.parent / "static" / "templates"


class TemplateService:
    """Reads template JSON structures and HTML files from disk."""

    @staticmethod
    def get_all() -> list[TemplateSummary]:
        """Return a list of all available templates for the frontend dropdown."""
        summaries: list[TemplateSummary] = []
        for json_file in sorted(TEMPLATES_DIR.glob("*.json")):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                summaries.append(TemplateSummary(id=data["id"], name=data["name"]))
            except Exception as e:
                logger.warning("Failed to read template JSON %s: %s", json_file.name, e)
        return summaries

    @staticmethod
    def get_structure(template_id: str) -> TemplateStructure:
        """
        Read and return the full structure for one template.

        Raises FileNotFoundError if the JSON does not exist.
        """
        json_file = TEMPLATES_DIR / f"{template_id}.json"
        if not json_file.exists():
            raise FileNotFoundError(f"Template not found: {template_id}")
        data = json.loads(json_file.read_text(encoding="utf-8"))
        return TemplateStructure(**data)

    @staticmethod
    def get_html(template_id: str) -> str:
        """
        Read and return the raw HTML for one template.

        Raises FileNotFoundError if the HTML file does not exist.
        """
        structure = TemplateService.get_structure(template_id)
        html_file = TEMPLATES_DIR / structure.file
        if not html_file.exists():
            raise FileNotFoundError(f"HTML file not found: {structure.file}")
        return html_file.read_text(encoding="utf-8")

    @staticmethod
    def get_css(template_id: str) -> str:
        """
        Read and return the raw CSS for one template.

        The CSS file is expected to be named after the template_id,
        e.g. template_001.css.

        Returns an empty string if the CSS file does not exist.
        """
        css_file = TEMPLATES_DIR / f"{template_id}.css"
        if not css_file.exists():
            logger.warning("CSS file not found for template: %s", template_id)
            return ""
        return css_file.read_text(encoding="utf-8")

