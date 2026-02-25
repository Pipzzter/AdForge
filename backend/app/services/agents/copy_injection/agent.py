"""
Copy & Image Injection Agent Implementation
============================================

Core logic for Agent 1 - fills HTML templates with marketing copy.

Flow:
1. Extract all placeholders from HTML template (pattern: [Something goes here])
2. Send placeholders + raw copy to LLM
3. LLM generates content for each placeholder based on the raw copy
4. Replace placeholders in template with generated content
5. Return filled HTML
"""

import logging
import re
from typing import Optional

from google.genai.types import ThinkingLevel

from app.services.agents.base import BaseAgent
from app.services.agents.copy_injection.adjuster import TemplateAdjuster
from app.services.agents.copy_injection.schemas import (
    CopyInjectionInput,
    CopyInjectionOutput,
    CopyStructureAnalysis,
    PlaceholderMapping,
    PlacementSummary,
)
from app.services.agents.copy_injection.template_service import TemplateService
from app.services.agents.llm_client import GeminiClient

logger = logging.getLogger(__name__)

# Regex pattern for placeholders like [Headline goes here], [Body section 1 goes here]
PLACEHOLDER_PATTERN = r'\[[^\]]*(?:goes here|Goes here|Goes Here)[^\]]*\]'

COPY_STRUCTURE_PROMPT = """You are analyzing advertorial copy to count how many distinct items exist for each content group.

## CONTENT GROUPS TO COUNT
{groups}

## RAW ADVERTORIAL COPY
{raw_copy}

## INSTRUCTIONS
- Read the copy carefully and count how many distinct items exist for EACH group listed above.
- A "body section" is a distinct paragraph or topic block in the main article body.
- A "review" or "testimonial" is a distinct customer quote or story.
- Count ONLY what is actually present in the copy — do not invent content.
- There is NO maximum — if the copy has 10 reviews, return 10.
- Return exactly the group labels provided, with your count for each.
"""

COPY_INJECTION_SYSTEM_PROMPT = """You are an expert marketing copywriter. Your task is to fill HTML template placeholders with content from raw advertorial copy.

## YOUR TASK
Given a list of placeholders and raw advertorial copy, generate appropriate content for EACH placeholder.

## PLACEHOLDERS TO FILL
{placeholders}

## RAW ADVERTORIAL COPY
{raw_copy}

## RULES
1. Extract the appropriate section from the raw copy for each placeholder
2. For [Headline goes here] - use the main headline or title from the copy
3. For [Hook goes here] - use the attention-grabbing opening statement
4. For [Author info goes here] - use author/expert information if available, or create a brief author attribution
5. For [Date of last edit goes here] - use the publication or last updated date from the copy if present; otherwise use today's date formatted as "Last Updated Month YYYY"
6. For [Introduction agitation goes here] - use the problem statement that agitates the reader's pain points
7. For [Body section N goes here] - split the main body content into sections, maintaining the narrative flow
8. For [Product presentation goes here] - use the product description/benefits section
9. For [Future pacing goes here] - use content about what life looks like after using the product
10. For [Conspiracy section goes here] - use any "hidden truth" or "what they don't want you to know" content
11. For [Social proof N goes here] - use testimonials, case studies, or user stories
12. For [Main Social proof goes here] - use the most compelling testimonial or proof element
13. For [Offer section goes here] - use the pricing, guarantee, and call-to-action content
14. For [Reviews goes here N] - use customer reviews/testimonials

## IMPORTANT
- Maintain the tone and style of the original copy
- If a placeholder type has no matching content in the raw copy, create appropriate content that fits the marketing narrative
- Do NOT include any HTML tags — just plain text
- Separate distinct paragraphs with a blank line (double newline \\n\\n)
- Each body section may contain multiple paragraphs separated by blank lines
- Never merge multiple paragraphs into a single block of text"""


class CopyInjectionAgent(BaseAgent[CopyInjectionInput, CopyInjectionOutput]):
    """
    Agent 1: Copy & Image Injection

    Fills predefined HTML templates with marketing copy.

    Process:
    1. Extract placeholders from template
    2. LLM maps raw copy to placeholders
    3. Replace placeholders with generated content
    """

    def __init__(self, llm_client: Optional[GeminiClient] = None) -> None:
        super().__init__(name="copy_injection")
        self.llm_client = llm_client or GeminiClient()

    def extract_placeholders(self, html_template: str) -> list[str]:
        """
        Extract all placeholders from the HTML template.

        Finds patterns like:
        - [Headline goes here]
        - [Body section 1 goes here]
        - [Reviews goes here 1 ]
        """
        placeholders = re.findall(PLACEHOLDER_PATTERN, html_template, re.IGNORECASE)
        # Remove duplicates while preserving order
        seen = set()
        unique_placeholders = []
        for p in placeholders:
            if p not in seen:
                seen.add(p)
                unique_placeholders.append(p)
        return unique_placeholders

    def build_prompt(self, input_data: CopyInjectionInput) -> str:
        """Build the prompt for the LLM (required by base class)."""
        # For the base class contract — returns the fill prompt with no placeholders
        # as a fallback. The real prompt is built inside process().
        return self._build_prompt_internal(
            placeholders=[],
            raw_copy=input_data.raw_copy,
            product_name=input_data.product_name,
            product_category=input_data.product_category,
        )

    def _build_prompt_internal(
        self,
        placeholders: list[str],
        raw_copy: str,
        product_name: Optional[str] = None,
        product_category: Optional[str] = None,
    ) -> str:
        """Build the prompt for the LLM."""
        placeholders_list = "\n".join(f"- {p}" for p in placeholders)

        prompt = COPY_INJECTION_SYSTEM_PROMPT.format(
            placeholders=placeholders_list,
            raw_copy=raw_copy,
        )

        if product_name:
            prompt += f"\n\nPRODUCT NAME: {product_name}"
        if product_category:
            prompt += f"\nPRODUCT CATEGORY: {product_category}"

        return prompt

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize a placeholder string for fuzzy matching."""
        return re.sub(r'\s+', ' ', text).strip().lower()

    @staticmethod
    def _format_content(content: str) -> str:
        """
        Convert plain-text content returned by the LLM into HTML paragraphs.

        Splits on blank lines (double newline) and wraps each non-empty
        paragraph in a <p> tag so the content renders with proper spacing
        instead of collapsing into a wall of text.
        """
        paragraphs = re.split(r'\n\s*\n', content.strip())
        formatted = "\n".join(
            f"<p>{para.strip()}</p>"
            for para in paragraphs
            if para.strip()
        )
        return formatted or f"<p>{content.strip()}</p>"

    def fill_template(
        self,
        html_template: str,
        placeholder_mapping: PlaceholderMapping,
        template_placeholders: list[str],
    ) -> tuple[str, list[PlacementSummary]]:
        """
        Replace placeholders in the template with generated content.

        Matches LLM-returned placeholder names against the actual placeholders
        extracted from the template using exact → case-insensitive → normalized
        fuzzy matching so minor LLM variations don't cause missed replacements.

        Returns the filled HTML and a summary of placements.
        """
        filled_html = html_template
        placements: list[PlacementSummary] = []

        # Build a lookup: normalized placeholder text → content from LLM
        llm_lookup: dict[str, str] = {}
        for item in placeholder_mapping.placeholders:
            llm_lookup[self._normalize(item.placeholder)] = item.content

        # Iterate over the actual placeholders found in the template
        for actual_placeholder in template_placeholders:
            # 1. Exact match in LLM mapping
            content: Optional[str] = next(
                (item.content for item in placeholder_mapping.placeholders
                 if item.placeholder == actual_placeholder),
                None,
            )

            # 2. Normalized fuzzy match
            if content is None:
                content = llm_lookup.get(self._normalize(actual_placeholder))

            if content is None:
                placements.append(
                    PlacementSummary(
                        placeholder=actual_placeholder,
                        content_preview="[NOT FOUND IN LLM RESPONSE]",
                        filled=False,
                    )
                )
                logger.warning("No LLM content for placeholder: %s", actual_placeholder)
                continue

            # Format plain text into <p>-wrapped paragraphs
            formatted_content = self._format_content(content)

            # Replace in template — use str.replace for exact, re.sub with
            # lambda for case-insensitive to avoid backslash interpretation bugs
            if actual_placeholder in filled_html:
                filled_html = filled_html.replace(actual_placeholder, formatted_content)
                logger.debug("Filled placeholder (exact): %s", actual_placeholder)
            else:
                pattern = re.escape(actual_placeholder)
                if re.search(pattern, filled_html, re.IGNORECASE):
                    filled_html = re.sub(
                        pattern,
                        lambda m, c=formatted_content: c,
                        filled_html,
                        flags=re.IGNORECASE,
                    )
                    logger.debug("Filled placeholder (case-insensitive): %s", actual_placeholder)
                else:
                    placements.append(
                        PlacementSummary(
                            placeholder=actual_placeholder,
                            content_preview="[NOT FOUND IN TEMPLATE]",
                            filled=False,
                        )
                    )
                    logger.warning("Placeholder not found in template: %s", actual_placeholder)
                    continue

            placements.append(
                PlacementSummary(
                    placeholder=actual_placeholder,
                    content_preview=content[:100] + "..." if len(content) > 100 else content,
                    filled=True,
                )
            )

        return filled_html, placements

    async def process(self, input_data: CopyInjectionInput) -> CopyInjectionOutput:
        """
        Process the template and copy, returning filled HTML.

        New flow:
        1. Read template structure JSON (no LLM, instant)
        2. LLM Call 1 — count how many of each group the copy contains
        3. Read HTML from disk (no LLM, server-side only)
        4. Adjust HTML — trim surplus slots / clone missing slots (no LLM)
        5. LLM Call 2 — fill all remaining placeholders (existing logic)
        6. Inject content into adjusted HTML
        7. Return result
        """
        logger.info(
            "Processing copy injection: template_id=%s, copy_length=%d",
            input_data.template_id,
            len(input_data.raw_copy),
        )

        try:
            # ----------------------------------------------------------------
            # Step 1: Read template structure from JSON
            # ----------------------------------------------------------------
            structure = TemplateService.get_structure(input_data.template_id)
            logger.info(
                "Loaded structure for '%s': %d groups, %d singletons",
                input_data.template_id,
                len(structure.groups),
                len(structure.singletons),
            )

            # ----------------------------------------------------------------
            # Step 2: LLM Call 1 — count what the copy actually contains
            # ----------------------------------------------------------------
            groups_description = "\n".join(
                f"- {g.label} (template has {g.count} slots)"
                for g in structure.groups
            )
            structure_prompt = COPY_STRUCTURE_PROMPT.format(
                groups=groups_description,
                raw_copy=input_data.raw_copy,
            )
            copy_analysis: CopyStructureAnalysis = await self.llm_client.generate_structured(
                prompt=structure_prompt,
                schema=CopyStructureAnalysis,
                thinking_level=ThinkingLevel.LOW,
            )
            counts: dict[str, int] = {g.label: g.count for g in copy_analysis.groups}
            logger.info("Copy structure analysis: %s", counts)

            # ----------------------------------------------------------------
            # Step 3: Read HTML from disk
            # ----------------------------------------------------------------
            html = TemplateService.get_html(input_data.template_id)

            # ----------------------------------------------------------------
            # Step 4: Adjust HTML (trim / expand)
            # ----------------------------------------------------------------
            html, updated_structure = TemplateAdjuster.adjust(html, structure, counts)
            logger.info(
                "HTML adjusted for template '%s'", input_data.template_id
            )

            # ----------------------------------------------------------------
            # Step 5: Extract placeholders from adjusted HTML
            # ----------------------------------------------------------------
            placeholders = self.extract_placeholders(html)
            logger.info("Found %d unique placeholders after adjustment", len(placeholders))

            if not placeholders:
                logger.warning("No placeholders found after adjustment")
                return CopyInjectionOutput(
                    html=html,
                    placeholders_found=[],
                    placements=[],
                    success=True,
                    error_message="No placeholders found in template",
                )

            # ----------------------------------------------------------------
            # Step 6: LLM Call 2 — fill placeholders (existing logic)
            # ----------------------------------------------------------------
            prompt = self._build_prompt_internal(
                placeholders=placeholders,
                raw_copy=input_data.raw_copy,
                product_name=input_data.product_name,
                product_category=input_data.product_category,
            )
            placeholder_mapping = await self.llm_client.generate_structured(
                prompt=prompt,
                schema=PlaceholderMapping,
                thinking_level=ThinkingLevel.LOW,
            )
            logger.info(
                "LLM generated content for %d placeholders",
                len(placeholder_mapping.placeholders),
            )

            # ----------------------------------------------------------------
            # Step 7: Fill template
            # ----------------------------------------------------------------
            filled_html, placements = self.fill_template(
                html_template=html,
                placeholder_mapping=placeholder_mapping,
                template_placeholders=placeholders,
            )

            filled_count = sum(1 for p in placements if p.filled)
            logger.info(
                "Copy injection complete: %d/%d placeholders filled",
                filled_count,
                len(placeholders),
            )

            return CopyInjectionOutput(
                html=filled_html,
                placeholders_found=placeholders,
                placements=placements,
                success=True,
            )

        except FileNotFoundError as e:
            logger.error("Template not found: %s", str(e))
            return CopyInjectionOutput(
                html="",
                placeholders_found=[],
                placements=[],
                success=False,
                error_message=str(e),
            )
        except Exception as e:
            logger.error("Copy injection failed: %s", str(e), exc_info=True)
            return CopyInjectionOutput(
                html="",
                placeholders_found=[],
                placements=[],
                success=False,
                error_message=str(e),
            )


