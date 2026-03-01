"""
Template Service
================

Loads HTML templates and metadata from the filesystem.
"""

import json
import logging
import re
from pathlib import Path
from typing import Optional

from app.services.agents.copy_injection.schemas import TemplateSummary, TemplateMetadata

logger = logging.getLogger(__name__)

# Path to templates directory
TEMPLATES_DIR = Path(__file__).parent.parent.parent.parent / "static" / "new_templates"
METADATA_FILE = TEMPLATES_DIR / "template_metadata.json"


class TemplateService:
    """Service for loading and managing HTML templates."""

    _metadata_cache: Optional[dict] = None

    @classmethod
    def _load_metadata(cls) -> dict:
        """Load and cache template metadata."""
        if cls._metadata_cache is None:
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                cls._metadata_cache = json.load(f)
            logger.info("Loaded template metadata from %s", METADATA_FILE)
        return cls._metadata_cache

    @classmethod
    def get_all(cls) -> list[TemplateSummary]:
        """Get summary of all available templates."""
        metadata = cls._load_metadata()
        templates = []
        for template_id, template_data in metadata.get("templates", {}).items():
            templates.append(
                TemplateSummary(
                    id=template_id,
                    name=template_data.get("name", template_id),
                )
            )
        return sorted(templates, key=lambda t: t.id)

    @classmethod
    def get_metadata(cls, template_id: str) -> TemplateMetadata:
        """Get metadata for a specific template."""
        metadata = cls._load_metadata()
        template_data = metadata.get("templates", {}).get(template_id)
        if not template_data:
            raise FileNotFoundError(f"Template not found: {template_id}")
        return TemplateMetadata(**template_data)

    @classmethod
    def get_html(cls, template_id: str) -> str:
        """Load the HTML content for a template."""
        metadata = cls.get_metadata(template_id)
        html_path = TEMPLATES_DIR / metadata.file
        if not html_path.exists():
            raise FileNotFoundError(f"Template HTML not found: {html_path}")
        return html_path.read_text(encoding="utf-8")

    @classmethod
    def get_css(cls, template_id: str) -> str:
        """Load the CSS content for a template (if exists)."""
        # CSS file has same name as HTML but with .css extension
        metadata = cls.get_metadata(template_id)
        css_filename = metadata.file.replace(".html", ".css")
        css_path = TEMPLATES_DIR / css_filename
        if not css_path.exists():
            logger.warning("No CSS file found for template %s", template_id)
            return ""
        return css_path.read_text(encoding="utf-8")

    @classmethod
    def get_image_context_rules(cls) -> dict:
        """Get image context rules from metadata."""
        metadata = cls._load_metadata()
        return metadata.get("image_context_rules", {})

    @classmethod
    def extract_placeholders(cls, html: str) -> list[str]:
        """
        Extract all placeholders from HTML content.
        Placeholders are in format: [Something goes here] or [SOMETHING GOES HERE]
        """
        pattern = r'\[([^\[\]]*(?:goes here|GOES HERE)[^\[\]]*)\]'
        matches = re.findall(pattern, html, re.IGNORECASE)
        # Return unique placeholders in order of first appearance
        seen = set()
        result = []
        for match in matches:
            placeholder = f"[{match}]"
            if placeholder not in seen:
                seen.add(placeholder)
                result.append(placeholder)
        return result

    @classmethod
    def extract_repeat_block(cls, html: str, section_name: str) -> Optional[tuple[str, str, int, int]]:
        """
        Extract a REPEAT block from HTML.

        Args:
            html: Full HTML content
            section_name: Name of the section (e.g., 'review', 'body', 'social_proof')

        Returns:
            Tuple of (full_match, inner_content, start_pos, end_pos) or None if not found
        """
        # Pattern matches both formats:
        # <!-- REPEAT:xxx:START --> and <!--REPEAT:xxx:START-->
        pattern = rf'<!--\s*REPEAT:{section_name}:START\s*-->(.*?)<!--\s*REPEAT:{section_name}:END\s*-->'
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if match:
            return (match.group(0), match.group(1), match.start(), match.end())
        return None

