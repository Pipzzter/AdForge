"""
Copy Injection Agent - Schemas
==============================

Pydantic models for input/output of the Copy Injection Agent.
"""

from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Template Models
# ---------------------------------------------------------------------------


class TemplateSummary(BaseModel):
    """Summary of a template for the frontend dropdown."""

    id: str
    name: str


class TemplateMetadata(BaseModel):
    """Metadata for a single template from template_metadata.json."""

    name: str
    file: str
    repeatable_sections: dict
    non_repeatable_placeholders: list[dict]


# ---------------------------------------------------------------------------
# Parsed Copy Models (LLM Output)
# ---------------------------------------------------------------------------


class BodySection(BaseModel):
    """A single body section with title, content, and image context."""

    title: Optional[str] = Field(None, description="Section title/heading")
    content: str = Field(
        ...,
        description="Main body text - MAX 150 words! Use short paragraphs (2-3 sentences), varied rhythm, fragment sentences for impact. HTML formatted with <br> tags."
    )
    image_context: Optional[str] = Field(
        None, description="Description of what image should show for this section"
    )


class Review(BaseModel):
    """A customer review/testimonial."""

    person_name: str = Field(..., description="Name of the reviewer")
    person_location: Optional[str] = Field(None, description="Location of reviewer (if mentioned)")
    review_text: str = Field(
        ...,
        description="The testimonial text - MUST BE 2-4 sentences MAX! Write like a real human, not marketing speak. Include specific results/timeframes."
    )
    person_description: Optional[str] = Field(
        None, description="Brief description for generating person image (age, gender, ethnicity hints)"
    )


class SocialProof(BaseModel):
    """A social proof element (expert quote, study reference, etc.)."""

    person_or_group: str = Field(..., description="Name/title of the person or group")
    quote: str = Field(
        ...,
        description="The social proof statement/quote - MUST BE 1-2 sentences MAX! Brief and credible."
    )
    image_context: Optional[str] = Field(
        None, description="Description of what image should show (expert photo, chart, etc.)"
    )


class ProductInfo(BaseModel):
    """Product presentation information."""

    title: Optional[str] = Field(None, description="Product section title")
    content: str = Field(..., description="Product description and benefits")
    image_context: Optional[str] = Field(
        None, description="Description for product image"
    )


class OfferInfo(BaseModel):
    """Offer/CTA section information."""

    title: Optional[str] = Field(None, description="Offer section title")
    content: str = Field(..., description="Offer details and CTA text")
    image_context: Optional[str] = Field(
        None, description="Description for offer image"
    )


class ParsedCopy(BaseModel):
    """
    Structured representation of parsed advertorial copy.
    This is the output from the LLM parsing step.
    """

    # Header section
    headline: str = Field(..., description="Main headline of the advertorial")
    subheadline: Optional[str] = Field(None, description="Secondary headline if present")
    hook: Optional[str] = Field(None, description="Opening hook text")
    post_category: Optional[str] = Field(
        None,
        description="Category label for the article (REQUIRED - generate based on content: Health, Wellness, Weight Loss, etc.)"
    )

    # Author info
    author_name: Optional[str] = Field(None, description="Author name and credentials")
    author_description: Optional[str] = Field(
        None, description="Brief description for generating author image"
    )

    # Introduction
    introduction: Optional[str] = Field(None, description="Introduction paragraphs")

    # Body sections (repeatable)
    body_sections: list[BodySection] = Field(
        default_factory=list, description="Main body content sections"
    )

    # Product presentation
    product: Optional[ProductInfo] = Field(None, description="Product presentation section")
    product_reveal: Optional[str] = Field(
        None, description="Product reveal text (for listicle template)"
    )
    solution_discovery_title: Optional[str] = Field(
        None, description="Title for solution/product discovery section (e.g., 'The Discovery', 'How I Found The Solution')"
    )

    # Social proof (repeatable)
    social_proofs: list[SocialProof] = Field(
        default_factory=list, description="Social proof elements"
    )

    # Main social proof (non-repeatable, scientific backing)
    main_social_proof_title: Optional[str] = Field(None, description="Main social proof section title")
    main_social_proof: Optional[str] = Field(
        None, description="Main social proof content (studies, statistics)"
    )
    main_social_proof_image_context: Optional[str] = Field(
        None, description="Description for main social proof image (chart, credentials)"
    )

    # Case study (non-repeatable) - A detailed story of ONE person's transformation
    # IMPORTANT: Look for personal stories with names like "Maria discovered...", "John's journey...", etc.
    case_study_title: Optional[str] = Field(
        None,
        description="Title for the case study section. Examples: 'Maria's Story', 'How John Found Relief', 'A Real Success Story', 'One Woman's Journey'. MUST be filled if there's a detailed personal story in the copy."
    )
    case_study: Optional[str] = Field(
        None,
        description="The detailed narrative of one person's journey/transformation. HTML formatted with <br><br> for paragraphs, <b> for bold. MUST be filled if there's a detailed personal story in the copy."
    )
    case_study_image_context: Optional[str] = Field(
        None, description="Description for case study image"
    )

    # Reviews (repeatable)
    reviews: list[Review] = Field(
        default_factory=list, description="Customer reviews/testimonials"
    )

    # Offer/CTA
    offer: Optional[OfferInfo] = Field(None, description="Offer section")

    # References
    references: Optional[str] = Field(None, description="References/sources section")

    # Overall context for headline image
    headline_image_context: Optional[str] = Field(
        None, description="Description of what the main hero image should show"
    )


# ---------------------------------------------------------------------------
# API Input/Output Models
# ---------------------------------------------------------------------------


class CopyInjectionInput(BaseModel):
    """Input for the Copy Injection Agent."""

    template_id: str = Field(..., description="ID of the template to use")
    raw_copy: str = Field(..., description="Raw advertorial copy to parse and inject")
    product_name: Optional[str] = Field(None, description="Product name (optional hint)")
    product_category: Optional[str] = Field(None, description="Product category (optional hint)")


class PlacementSummary(BaseModel):
    """Summary of a single placeholder placement."""

    placeholder: str = Field(..., description="The placeholder text")
    content_preview: str = Field(..., description="Preview of content that was placed")
    filled: bool = Field(..., description="Whether the placeholder was filled")


class CopyInjectionOutput(BaseModel):
    """Output from the Copy Injection Agent."""

    html: str = Field(default="", description="Final HTML with placeholders filled")
    placeholders_found: list[str] = Field(
        default_factory=list, description="All placeholders found in template"
    )
    placements: list[PlacementSummary] = Field(
        default_factory=list, description="Summary of each placement"
    )
    images_generated: int = Field(default=0, description="Number of images generated")
    success: bool = Field(default=False, description="Whether generation succeeded")
    error_message: Optional[str] = Field(None, description="Error message if failed")

