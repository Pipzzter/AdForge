"""
Template Adjuster
=================

Trims surplus placeholder slots or expands (clones) card blocks so the
HTML exactly matches the number of items found in the raw copy.

Rules per group:
  - container_class is None  → text-only group (body sections, listicle items)
      trim: replace the placeholder string with ""
      expand: append a new numbered placeholder after the last existing one
  - container_class is set   → card/block group (reviews, testimonials)
      trim: remove the entire container div that wraps the surplus placeholder
      expand: clone the last container div, renumber its placeholder, insert after
"""

import copy
import logging
import re
from typing import Optional

from bs4 import BeautifulSoup, NavigableString, Tag

from app.services.agents.copy_injection.schemas import TemplateGroup, TemplateStructure

logger = logging.getLogger(__name__)


class TemplateAdjuster:
    """Adjusts an HTML string to match the required group counts."""

    @staticmethod
    def adjust(
        html: str,
        structure: TemplateStructure,
        counts: dict[str, int],
    ) -> tuple[str, TemplateStructure]:
        """
        Adjust the HTML for every group based on the copy counts.

        Args:
            html: Raw HTML string read from disk.
            structure: Pre-analyzed template structure (from JSON).
            counts: Dict of {label: needed_count} from LLM Call 1.

        Returns:
            Tuple of (adjusted_html, updated_structure).
            The updated_structure has group.placeholders lists updated to
            reflect any cloned slots so LLM Call 2 knows what to fill.
        """
        # Work with a mutable copy of the structure groups
        updated_groups: list[TemplateGroup] = []

        for group in structure.groups:
            needed = counts.get(group.label, group.count)
            needed = max(0, needed)  # allow zero — removes all slots if copy has none

            if needed == group.count:
                # No change needed
                updated_groups.append(group)
                continue

            if group.container_class is None:
                # Text-only group — trim or expand inline
                html, updated_group = TemplateAdjuster._adjust_text_group(
                    html, group, needed
                )
            else:
                # Card group — trim or expand container blocks
                html, updated_group = TemplateAdjuster._adjust_card_group(
                    html, group, needed
                )

            updated_groups.append(updated_group)

        # Return HTML with updated structure
        updated_structure = structure.model_copy(
            update={"groups": updated_groups}
        )
        return html, updated_structure

    # ------------------------------------------------------------------
    # Text-only groups (body sections, listicle items, etc.)
    # ------------------------------------------------------------------

    @staticmethod
    def _adjust_text_group(
        html: str, group: TemplateGroup, needed: int
    ) -> tuple[str, TemplateGroup]:
        placeholders = list(group.placeholders)

        if needed < group.count:
            # Trim: blank out surplus placeholders
            for placeholder in placeholders[needed:]:
                html = html.replace(placeholder, "")
                logger.debug("Trimmed text placeholder: %s", placeholder)
            placeholders = placeholders[:needed]

        elif needed > group.count:
            # Expand: derive a new placeholder name from the last one and
            # insert it as plain text right after the last existing placeholder
            last_placeholder = placeholders[-1]
            for i in range(group.count + 1, needed + 1):
                new_placeholder = TemplateAdjuster._next_placeholder(
                    last_placeholder, i
                )
                # Insert the new placeholder immediately after the last one
                html = html.replace(
                    last_placeholder,
                    f"{last_placeholder}\n{new_placeholder}",
                    1,
                )
                placeholders.append(new_placeholder)
                last_placeholder = new_placeholder
                logger.debug("Expanded text placeholder: %s", new_placeholder)

        updated_group = group.model_copy(
            update={"count": needed, "placeholders": placeholders}
        )
        return html, updated_group

    # ------------------------------------------------------------------
    # Card groups (reviews, testimonials, etc.)
    # ------------------------------------------------------------------

    @staticmethod
    def _adjust_card_group(
        html: str, group: TemplateGroup, needed: int
    ) -> tuple[str, TemplateGroup]:
        placeholders = list(group.placeholders)
        soup = BeautifulSoup(html, "html.parser")

        if needed < group.count:
            # Trim: remove entire container divs for surplus slots
            for placeholder in placeholders[needed:]:
                container = TemplateAdjuster._find_container(
                    soup, placeholder, group.container_class
                )
                if container:
                    container.decompose()
                    logger.debug(
                        "Removed card container for placeholder: %s", placeholder
                    )
                else:
                    # Fallback: just blank the placeholder text
                    logger.warning(
                        "Container not found for %s, blanking text instead", placeholder
                    )
            placeholders = placeholders[:needed]

        elif needed > group.count:
            # Expand: clone the last container div, renumber placeholder inside
            last_placeholder = placeholders[-1]
            last_container = TemplateAdjuster._find_container(
                soup, last_placeholder, group.container_class
            )

            if last_container is None:
                logger.warning(
                    "Cannot expand group '%s': container not found for last placeholder '%s'",
                    group.label,
                    last_placeholder,
                )
            else:
                for i in range(group.count + 1, needed + 1):
                    new_placeholder = TemplateAdjuster._next_placeholder(
                        last_placeholder, i
                    )
                    cloned = copy.copy(last_container)
                    # Replace old placeholder text inside the clone
                    TemplateAdjuster._replace_text_in_tag(
                        cloned, last_placeholder, new_placeholder
                    )
                    # Insert after current last container
                    last_container.insert_after(cloned)
                    last_container = cloned
                    placeholders.append(new_placeholder)
                    logger.debug(
                        "Cloned card for group '%s', new placeholder: %s",
                        group.label,
                        new_placeholder,
                    )

        html = str(soup)
        updated_group = group.model_copy(
            update={"count": needed, "placeholders": placeholders}
        )
        return html, updated_group

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _find_container(
        soup: BeautifulSoup, placeholder_text: str, container_class: str
    ) -> Optional[Tag]:
        """
        Find the outermost container tag that:
        1. Contains the exact placeholder text somewhere inside it
        2. Has container_class in its class list
        """
        # Find all tags that contain the placeholder text
        for tag in soup.find_all(string=re.compile(re.escape(placeholder_text))):
            parent = tag.parent
            while parent and parent.name not in ("body", "[document]", "html"):
                if isinstance(parent, Tag):
                    classes = parent.get("class", [])
                    # container_class may be a multi-word class string
                    target_classes = container_class.split()
                    if all(c in classes for c in target_classes):
                        return parent
                parent = parent.parent
        return None

    @staticmethod
    def _replace_text_in_tag(tag: Tag, old_text: str, new_text: str) -> None:
        """Replace all occurrences of old_text with new_text inside a tag tree."""
        for node in tag.find_all(string=True):
            if old_text in node:
                node.replace_with(NavigableString(node.replace(old_text, new_text)))

    @staticmethod
    def _next_placeholder(last_placeholder: str, n: int) -> str:
        """
        Derive the next placeholder name by replacing the highest number
        found in the string with n.

        Example:
            "[Review 3 goes here]", 4  →  "[Review 4 goes here]"
            "[Body section 5 goes here]", 6  →  "[Body section 6 goes here]"
        """
        # Find all numbers in the placeholder
        numbers = re.findall(r"\d+", last_placeholder)
        if numbers:
            # Replace the last number occurrence with n
            last_num = numbers[-1]
            # Replace only the last occurrence of that number
            idx = last_placeholder.rfind(last_num)
            return last_placeholder[:idx] + str(n) + last_placeholder[idx + len(last_num):]
        # No number found — just append the index
        closing = last_placeholder.rfind(" goes here")
        if closing != -1:
            return last_placeholder[:closing] + f" {n}" + last_placeholder[closing:]
        return last_placeholder + f" {n}"




