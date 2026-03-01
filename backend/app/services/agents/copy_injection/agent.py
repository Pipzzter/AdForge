"""
Copy Injection Agent
====================

Main agent that orchestrates the copy injection process:
1. Load template
2. Parse raw copy using LLM
3. Fill repeatable sections
4. Fill simple placeholders
5. Generate images
6. Return final HTML
"""

import logging
import re
from datetime import datetime

from app.services.agents.base import BaseAgent
from app.services.agents.copy_injection.schemas import (
    CopyInjectionInput,
    CopyInjectionOutput,
)
from app.services.agents.copy_injection.template_service import TemplateService
from app.services.agents.copy_injection.copy_parser import CopyParser
from app.services.agents.copy_injection.placeholder_filler import (
    PlaceholderFiller,
    fill_body_item,
    fill_review_item,
    fill_social_proof_item,
)
from app.services.agents.copy_injection.image_generator import ImageGenerator

logger = logging.getLogger(__name__)


class CopyInjectionAgent(BaseAgent[CopyInjectionInput, CopyInjectionOutput]):
    """
    Agent 1: Copy & Image Injection

    Takes a template and raw advertorial copy, fills all placeholders
    with appropriate content and generated images.
    """

    def __init__(self) -> None:
        super().__init__(name="CopyInjectionAgent")
        self.copy_parser = CopyParser()
        self.image_generator = ImageGenerator()

    def build_prompt(self, input_data: CopyInjectionInput) -> str:
        """Not used directly - copy_parser handles prompting."""
        return ""

    def extract_placeholders(self, html: str) -> list[str]:
        """Extract all placeholders from HTML (utility method for API)."""
        return TemplateService.extract_placeholders(html)

    async def process(self, input_data: CopyInjectionInput) -> CopyInjectionOutput:
        """
        Process the copy injection request.

        Args:
            input_data: Template ID and raw copy

        Returns:
            CopyInjectionOutput with filled HTML and metadata
        """
        try:
            logger.info(
                "Processing copy injection: template=%s, copy_length=%d",
                input_data.template_id,
                len(input_data.raw_copy),
            )

            # 1. Load template HTML and metadata
            html = TemplateService.get_html(input_data.template_id)
            metadata = TemplateService.get_metadata(input_data.template_id)

            # Extract all placeholders for reporting
            all_placeholders = TemplateService.extract_placeholders(html)
            logger.info("Found %d placeholders in template", len(all_placeholders))

            # 2. Parse raw copy using LLM
            parsed_copy = await self.copy_parser.parse(
                raw_copy=input_data.raw_copy,
                product_name=input_data.product_name,
                product_category=input_data.product_category,
            )

            # 3. Create filler and process template
            filler = PlaceholderFiller(html, input_data.template_id)

            # 4. Fill repeatable sections
            # Body sections
            filler.fill_repeat_section(
                section_name="body",
                items=parsed_copy.body_sections,
                fill_item_func=fill_body_item,
            )

            # Reviews
            filler.fill_repeat_section(
                section_name="review",
                items=parsed_copy.reviews,
                fill_item_func=fill_review_item,
            )

            # Social proofs
            filler.fill_repeat_section(
                section_name="social_proof",
                items=parsed_copy.social_proofs,
                fill_item_func=fill_social_proof_item,
            )

            # 5. Fill simple (non-repeatable) placeholders
            self._fill_simple_placeholders(filler, parsed_copy)

            # 6. Get intermediate result
            html, placements, _ = filler.get_result()

            # 7. Remove empty optional sections BEFORE generating images
            html = self._remove_empty_optional_sections(html, parsed_copy)

            # 8. Generate images and replace placeholders
            html = await self.image_generator.generate_all_images(html, parsed_copy)

            # 9. Clean up any remaining unfilled placeholders
            html = self._clean_unfilled_placeholders(html)

            logger.info(
                "Copy injection complete: placements=%d, images=%d",
                len(placements),
                self.image_generator.generated_count,
            )

            return CopyInjectionOutput(
                html=html,
                placeholders_found=all_placeholders,
                placements=placements,
                images_generated=self.image_generator.generated_count,
                success=True,
            )

        except Exception as e:
            logger.exception("Copy injection failed: %s", str(e))
            return CopyInjectionOutput(
                html="",
                placeholders_found=[],
                placements=[],
                images_generated=0,
                success=False,
                error_message=str(e),
            )
    @staticmethod
    def _fill_simple_placeholders(
        filler: PlaceholderFiller,
        parsed_copy,
    ) -> None:
        """Fill all simple (non-repeatable) placeholders."""

        # Headline
        filler.fill_simple("[Headline goes here]", parsed_copy.headline)

        # Subheadline
        if parsed_copy.subheadline:
            filler.fill_simple("[Subheadline goes here]", parsed_copy.subheadline)

        # Hook
        if parsed_copy.hook:
            filler.fill_simple("[Hook goes here]", parsed_copy.hook)

        # Post category - always fill with default if not provided
        post_category = parsed_copy.post_category
        filler.fill_simple("[POST CATEGORY GOES HERE]", post_category)

        # Author info
        if parsed_copy.author_name:
            filler.fill_simple("[Author info goes here]", parsed_copy.author_name)

        # Date - use current date
        current_date = datetime.now().strftime("%B %d, %Y")
        filler.fill_simple("[Date of last edit goes here]", current_date)

        # Introduction
        if parsed_copy.introduction:
            filler.fill_simple("[Introduction goes here]", parsed_copy.introduction)

        # Product presentation - always fill title and content if product exists
        if parsed_copy.product:
            # Always fill product title (use default if not provided)
            product_title = parsed_copy.product.title or "The Solution"
            filler.fill_simple(
                "[Product presentation title goes here]",
                product_title,
            )
            filler.fill_simple(
                "[Product presentation goes here]",
                parsed_copy.product.content,
            )

        # Product reveal (template_004)
        if parsed_copy.product_reveal:
            filler.fill_simple("[Product reveal goes here]", parsed_copy.product_reveal)

        # Solution discovery title (template_004)
        if parsed_copy.solution_discovery_title:
            filler.fill_simple("[Solution product discovery title goes here]", parsed_copy.solution_discovery_title)
        elif parsed_copy.product and parsed_copy.product.title:
            # Fallback: use product title if no specific solution discovery title
            filler.fill_simple("[Solution product discovery title goes here]", parsed_copy.product.title)

        # Main social proof (non-repeatable)
        if parsed_copy.main_social_proof_title:
            filler.fill_simple(
                "[Main Social proof title goes here]",
                parsed_copy.main_social_proof_title,
            )
        if parsed_copy.main_social_proof:
            filler.fill_simple("[Main Social proof goes here]", parsed_copy.main_social_proof)

        # Case study (non-repeatable)
        if parsed_copy.case_study_title:
            filler.fill_simple("[Case study title goes here]", parsed_copy.case_study_title)
        if parsed_copy.case_study:
            filler.fill_simple("[Case study goes here]", parsed_copy.case_study)

        # Offer section - ALWAYS fill, even with defaults
        if parsed_copy.offer:
            offer_title = parsed_copy.offer.title or "Special Offer"
            offer_content = parsed_copy.offer.content
        else:
            # Fallback: generate offer content from product info if available
            offer_title = "Special Offer"
            if parsed_copy.product:
                offer_content = f"Get {parsed_copy.product.title or 'this product'} now and experience the benefits for yourself. Limited time offer available."
            else:
                offer_content = "Take advantage of this special offer today. Limited availability."

        filler.fill_simple("[Offer section title goes here]", offer_title)
        filler.fill_simple("[Offer section goes here]", offer_content)

        # References
        if parsed_copy.references:
            filler.fill_simple("[References goes here]", parsed_copy.references)

    def _remove_empty_optional_sections(self, html: str, parsed_copy) -> str:
        """
        Remove entire optional sections from HTML when they have no content.
        Uses OPTIONAL markers in templates: <!--OPTIONAL:section_name:START--> ... <!--OPTIONAL:section_name:END-->
        """
        # Case study section - remove if no content
        if not parsed_copy.case_study:
            html = self._remove_optional_block(html, "case_study")
            logger.info("Removed empty case study section from HTML")

        # Main social proof section - remove if no content
        if not parsed_copy.main_social_proof:
            html = self._remove_optional_block(html, "main_social_proof")
            logger.info("Removed empty main social proof section from HTML")

        return html

    def _remove_optional_block(self, html: str, section_name: str) -> str:
        """
        Remove an optional block marked with OPTIONAL comments.
        Pattern: <!--OPTIONAL:section_name:START--> ... <!--OPTIONAL:section_name:END-->
        """
        pattern = rf'<!--\s*OPTIONAL:{section_name}:START\s*-->.*?<!--\s*OPTIONAL:{section_name}:END\s*-->'
        html = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
        return html

    def _clean_unfilled_placeholders(self, html: str) -> str:
        """Remove any remaining unfilled placeholders."""
        # Remove text placeholders
        html = re.sub(r'\[[^[\]]*goes here[^[\]]*]', '', html, flags=re.IGNORECASE)
        # Remove image placeholder markers that weren't filled
        html = re.sub(r'__IMG_PLACEHOLDER_[^_]+__', '', html)
        return html



