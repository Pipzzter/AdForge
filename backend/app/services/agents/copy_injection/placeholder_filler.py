"""
Placeholder Filler
==================

Fills placeholders in HTML templates with content.
Handles both simple replacement and repeatable section cloning.
"""

import logging
import re
import uuid
from collections.abc import Callable

from app.services.agents.copy_injection.schemas import (
    PlacementSummary,
    BodySection,
    Review,
    SocialProof,
)
from app.services.agents.copy_injection.template_service import TemplateService

logger = logging.getLogger(__name__)


def regenerate_ids(html_block: str, prefix: str) -> str:
    """
    Regenerate all cc-id-xxx attributes to avoid duplicate IDs.

    Args:
        html_block: HTML content with cc-id attributes
        prefix: Prefix for new IDs (e.g., 'rev1', 'body2')

    Returns:
        HTML with regenerated IDs
    """
    def replace_id(match: re.Match) -> str:
        return f'id="cc-id-{prefix}-{uuid.uuid4().hex[:8]}"'

    return re.sub(r'id="cc-id-[^"]*"', replace_id, html_block)


class PlaceholderFiller:
    """Fills placeholders in HTML templates."""

    def __init__(self, html: str, template_id: str) -> None:
        self.html = html
        self.template_id = template_id
        self.placements: list[PlacementSummary] = []
        self.image_placeholders: dict[str, str] = {}  # placeholder -> image_context

    def fill_simple(self, placeholder: str, content: str) -> bool:
        """
        Fill a simple (non-repeatable) placeholder.

        Args:
            placeholder: The placeholder text including brackets
            content: The content to replace it with

        Returns:
            True if placeholder was found and filled
        """
        if placeholder not in self.html:
            self.placements.append(
                PlacementSummary(
                    placeholder=placeholder,
                    content_preview="[NOT FOUND IN TEMPLATE]",
                    filled=False,
                )
            )
            return False

        self.html = self.html.replace(placeholder, content)
        self.placements.append(
            PlacementSummary(
                placeholder=placeholder,
                content_preview=content[:100] + "..." if len(content) > 100 else content,
                filled=True,
            )
        )
        logger.debug("Filled placeholder: %s", placeholder)
        return True

    def fill_image_placeholder(self, placeholder: str, image_context: str) -> None:
        """
        Mark an image placeholder for later generation.

        Args:
            placeholder: The image placeholder text
            image_context: Description for image generation
        """
        if placeholder in self.html:
            self.image_placeholders[placeholder] = image_context
            logger.debug("Marked image placeholder: %s -> %s", placeholder, image_context[:50])

    def fill_repeat_section(
        self,
        section_name: str,
        items: list,
        fill_item_func: Callable,
    ) -> bool:
        """
        Fill a repeatable section by cloning the block for each item.

        Args:
            section_name: Name of the section (e.g., 'review', 'body', 'social_proof')
            items: List of items to fill (e.g., list of Review objects)
            fill_item_func: Function that takes (block_html, item, index) and returns filled html

        Returns:
            True if section was found and processed
        """
        block_info = TemplateService.extract_repeat_block(self.html, section_name)
        if not block_info:
            logger.warning("REPEAT block not found: %s", section_name)
            return False

        full_match, inner_content, start_pos, end_pos = block_info

        if not items:
            # No items - remove the entire block
            self.html = self.html[:start_pos] + self.html[end_pos:]
            logger.info("Removed empty REPEAT block: %s", section_name)
            return True

        # Clone and fill for each item
        filled_blocks = []
        for idx, item in enumerate(items):
            # Clone the inner content
            block_html = inner_content
            # Regenerate IDs
            block_html = regenerate_ids(block_html, f"{section_name}{idx + 1}")
            # Fill item-specific content
            block_html, item_placements = fill_item_func(block_html, item, idx)
            self.placements.extend(item_placements)
            filled_blocks.append(block_html)

        # Join all filled blocks
        combined = "\n".join(filled_blocks)

        # Replace the original block (including markers) with combined blocks
        self.html = self.html[:start_pos] + combined + self.html[end_pos:]

        logger.info(
            "Filled REPEAT block: %s with %d items",
            section_name,
            len(items),
        )
        return True

    def get_result(self) -> tuple[str, list[PlacementSummary], dict[str, str]]:
        """
        Get the final result.

        Returns:
            Tuple of (filled_html, placements, image_placeholders)
        """
        return self.html, self.placements, self.image_placeholders


# ---------------------------------------------------------------------------
# Item filling functions for repeatable sections
# ---------------------------------------------------------------------------


def fill_body_item(
    block_html: str,
    item: BodySection,
    idx: int,
) -> tuple[str, list[PlacementSummary]]:
    """
    Fill a body section block.

    The REPEAT block is cloned as-is with all its styling intact.
    We just do simple text replacement for the placeholders.
    """
    placements = []

    # Body section title - simple text replacement
    title_ph = "[Body section title goes here]"
    if title_ph in block_html and item.title:
        block_html = block_html.replace(title_ph, item.title)
        placements.append(PlacementSummary(
            placeholder=f"{title_ph} (body #{idx + 1})",
            content_preview=item.title[:100],
            filled=True,
        ))
    elif title_ph in block_html:
        block_html = block_html.replace(title_ph, "")
        placements.append(PlacementSummary(
            placeholder=f"{title_ph} (body #{idx + 1})",
            content_preview="[No title provided]",
            filled=False,
        ))

    # Body section content - simple text replacement
    content_ph = "[Body section goes here]"
    if content_ph in block_html:
        block_html = block_html.replace(content_ph, item.content)
        placements.append(PlacementSummary(
            placeholder=f"{content_ph} (body #{idx + 1})",
            content_preview=item.content[:100] + "..." if len(item.content) > 100 else item.content,
            filled=True,
        ))

    # Listicle item variants (for template_004)
    listicle_title_ph = "[Listicle item title goes here (1., 2., 3.,)]"
    if listicle_title_ph in block_html:
        title_text = item.title or f"{idx + 1}."
        block_html = block_html.replace(listicle_title_ph, title_text)
        placements.append(PlacementSummary(
            placeholder=f"{listicle_title_ph} (body #{idx + 1})",
            content_preview=title_text,
            filled=True,
        ))

    listicle_content_ph = "[Listicle item goes here]"
    if listicle_content_ph in block_html:
        block_html = block_html.replace(listicle_content_ph, item.content)
        placements.append(PlacementSummary(
            placeholder=f"{listicle_content_ph} (body #{idx + 1})",
            content_preview=item.content[:100] + "..." if len(item.content) > 100 else item.content,
            filled=True,
        ))

    # Image placeholder - mark for later generation
    for img_ph in ["[Body section image goes here]", "[Listicle item image goes here]"]:
        if img_ph in block_html:
            # We'll replace with a marker that includes the context
            context = item.image_context or f"Image relevant to: {item.content[:100]}"
            marker = f"__IMG_PLACEHOLDER_{idx}_{img_ph}__"
            block_html = block_html.replace(img_ph, marker)
            placements.append(PlacementSummary(
                placeholder=f"{img_ph} (body #{idx + 1})",
                content_preview=f"[IMAGE: {context[:80]}]",
                filled=True,  # Will be filled with actual URL later
            ))

    return block_html, placements


def fill_review_item(
    block_html: str,
    item: Review,
    idx: int,
) -> tuple[str, list[PlacementSummary]]:
    """Fill a review block."""
    placements = []

    # Review person name
    name_ph = "[Review person name goes here]"
    if name_ph in block_html:
        block_html = block_html.replace(name_ph, item.person_name)
        placements.append(PlacementSummary(
            placeholder=f"{name_ph} (review #{idx + 1})",
            content_preview=item.person_name,
            filled=True,
        ))

    # Review person location (template_004 only)
    location_ph = "[Review person location goes here]"
    if location_ph in block_html:
        location = item.person_location or ""
        block_html = block_html.replace(location_ph, location)
        placements.append(PlacementSummary(
            placeholder=f"{location_ph} (review #{idx + 1})",
            content_preview=location or "[No location]",
            filled=bool(location),
        ))

    # Review text
    review_ph = "[Review goes here]"
    if review_ph in block_html:
        block_html = block_html.replace(review_ph, item.review_text)
        placements.append(PlacementSummary(
            placeholder=f"{review_ph} (review #{idx + 1})",
            content_preview=item.review_text[:100] + "..." if len(item.review_text) > 100 else item.review_text,
            filled=True,
        ))

    # Review person image - mark for later
    img_ph = "[Review person image goes here]"
    if img_ph in block_html:
        context = item.person_description or f"Photo of {item.person_name}"
        marker = f"__IMG_PLACEHOLDER_review_{idx}__"
        block_html = block_html.replace(img_ph, marker)
        placements.append(PlacementSummary(
            placeholder=f"{img_ph} (review #{idx + 1})",
            content_preview=f"[IMAGE: {context[:80]}]",
            filled=True,
        ))

    return block_html, placements


def fill_social_proof_item(
    block_html: str,
    item: SocialProof,
    idx: int,
) -> tuple[str, list[PlacementSummary]]:
    """Fill a social proof block."""
    placements = []

    # Person/group name
    person_ph = "[Social proof person/group goes here]"
    if person_ph in block_html:
        block_html = block_html.replace(person_ph, item.person_or_group)
        placements.append(PlacementSummary(
            placeholder=f"{person_ph} (proof #{idx + 1})",
            content_preview=item.person_or_group,
            filled=True,
        ))

    # Quote/content
    quote_ph = "[Social proof goes here]"
    if quote_ph in block_html:
        block_html = block_html.replace(quote_ph, item.quote)
        placements.append(PlacementSummary(
            placeholder=f"{quote_ph} (proof #{idx + 1})",
            content_preview=item.quote[:100] + "..." if len(item.quote) > 100 else item.quote,
            filled=True,
        ))

    # Image - mark for later
    img_ph = "[Social proof person/group image goes here]"
    if img_ph in block_html:
        context = item.image_context or f"Photo of {item.person_or_group}"
        marker = f"__IMG_PLACEHOLDER_social_{idx}__"
        block_html = block_html.replace(img_ph, marker)
        placements.append(PlacementSummary(
            placeholder=f"{img_ph} (proof #{idx + 1})",
            content_preview=f"[IMAGE: {context[:80]}]",
            filled=True,
        ))

    return block_html, placements



