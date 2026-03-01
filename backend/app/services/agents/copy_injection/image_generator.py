"""
Image Generator
===============

Generates images for placeholders using context from the parsed copy.
"""

import logging
import re
from typing import Optional

from app.services.agents.image_client import GeminiImageClient
from app.services.agents.copy_injection.schemas import ParsedCopy

logger = logging.getLogger(__name__)


# Prompt templates for different image types
IMAGE_PROMPTS = {
    "headline": """Photorealistic hero image for an advertorial about: {context}
Style: Bright, uplifting, professional editorial photography. Warm lighting, positive atmosphere.
The image should feel hopeful and inspiring - convey transformation and better days ahead.
IMPORTANT: Absolutely NO text, words, letters, logos, or watermarks in the image.""",

    "author": """Photorealistic professional headshot photograph of {context}
Style: Clean bright background, warm professional lighting, confident and friendly smile.
The person should look approachable, trustworthy, and genuinely happy.
IMPORTANT: Absolutely NO text, words, letters, or watermarks in the image.""",

    "body_section": """Photorealistic image illustrating: {context}
Style: Bright, optimistic editorial photography. Warm natural lighting.
Focus on positive outcomes, health, vitality, and wellness. Uplifting mood.
IMPORTANT: Absolutely NO text, words, letters, logos, or watermarks in the image.""",

    "product": """Photorealistic product photograph of: {context}
Style: Clean, bright product photography with soft professional lighting.
Show the product appealingly on a clean background. Fresh, premium feel.
IMPORTANT: Absolutely NO text, words, letters, logos, labels, or watermarks in the image.""",

    "review_person": """Photorealistic portrait photograph of a happy, satisfied customer named {name}.
Description: {context}
Style: Natural, warm lighting. Genuine bright smile showing real happiness and relief.
The person should look healthy, vibrant, and full of life. Candid but positive.
IMPORTANT: Absolutely NO text, words, letters, or watermarks in the image.""",

    "social_proof": """Photorealistic image of: {context}
Style: Professional, bright, trustworthy. Clean and authoritative.
Convey credibility and positive outcomes. Warm, inviting atmosphere.
IMPORTANT: Absolutely NO text, words, letters, charts with text, logos, or watermarks in the image.""",

    "offer": """Photorealistic promotional image for: {context}
Style: Bright, eye-catching product/lifestyle photography.
Clean, premium feel. Convey value and positive transformation.
IMPORTANT: Absolutely NO text, words, letters, prices, logos, or watermarks in the image.""",

    "case_study": """Photorealistic image illustrating: {context}
Style: Warm, hopeful documentary photography.
Show positive transformation, health, and vitality. Before/after energy without being clinical.
IMPORTANT: Absolutely NO text, words, letters, or watermarks in the image.""",
}


class ImageGenerator:
    """Generates images for template placeholders."""

    def __init__(self) -> None:
        self.client = GeminiImageClient()
        self.generated_count = 0

    async def generate_image(
        self,
        image_type: str,
        context: str,
        name: Optional[str] = None,
        aspect_ratio: str = "4:3",
    ) -> str:
        """
        Generate a single image.

        Args:
            image_type: Type of image (headline, author, body_section, etc.)
            context: Context description for the image
            name: Optional name (for person images)
            aspect_ratio: Image aspect ratio

        Returns:
            URL of the generated image
        """
        prompt_template = IMAGE_PROMPTS.get(image_type, IMAGE_PROMPTS["body_section"])
        prompt = prompt_template.format(context=context, name=name or "a person")

        logger.info("Generating %s image: %s", image_type, context[:50])

        try:
            url = await self.client.generate(prompt, aspect_ratio=aspect_ratio)
            self.generated_count += 1
            return url
        except Exception as e:
            logger.error("Failed to generate %s image: %s", image_type, str(e))
            # Return a placeholder URL on failure
            return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxOCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIEdlbmVyYXRpb24gRmFpbGVkPC90ZXh0Pjwvc3ZnPg=="

    async def generate_all_images(
        self,
        html: str,
        parsed_copy: ParsedCopy,
    ) -> str:
        """
        Generate all images and replace placeholders/markers in HTML.

        Args:
            html: HTML with image placeholders or markers
            parsed_copy: Parsed copy with image contexts

        Returns:
            HTML with image URLs filled in
        """
        # Collect all image generation tasks
        replacements: dict[str, str] = {}

        # 1. Headline image
        headline_ph = "[Headline image goes here]"
        if headline_ph in html:
            context = parsed_copy.headline_image_context or f"Hero image for: {parsed_copy.headline}"
            url = await self.generate_image("headline", context, aspect_ratio="16:9")
            replacements[headline_ph] = url

        # 2. Author image
        author_ph = "[Author image goes here]"
        if author_ph in html:
            context = parsed_copy.author_description or parsed_copy.author_name or "professional author"
            url = await self.generate_image("author", context, aspect_ratio="1:1")
            replacements[author_ph] = url

        # 3. Product images
        for ph in ["[Product presentation image goes here]"]:
            if ph in html:
                context = parsed_copy.product.image_context if parsed_copy.product else "product photograph"
                url = await self.generate_image("product", context)
                replacements[ph] = url

        # 4. Offer image
        offer_ph = "[Offer section image goes here]"
        if offer_ph in html:
            context = parsed_copy.offer.image_context if parsed_copy.offer else "promotional offer"
            url = await self.generate_image("offer", context)
            replacements[offer_ph] = url

        # 5. Main social proof image
        main_sp_ph = "[Main social proof image goes here]"
        if main_sp_ph in html:
            context = parsed_copy.main_social_proof_image_context or "scientific study or credentials"
            url = await self.generate_image("social_proof", context)
            replacements[main_sp_ph] = url

        # 6. Case study image - ONLY if case study content exists
        case_ph = "[Case study image goes here]"
        if case_ph in html and parsed_copy.case_study:
            context = parsed_copy.case_study_image_context or "case study illustration"
            url = await self.generate_image("case_study", context)
            replacements[case_ph] = url

        # 7. Introduction image (template_002)
        intro_ph = "[Introduction image goes here]"
        if intro_ph in html:
            context = f"Introduction illustration for: {parsed_copy.headline}"
            url = await self.generate_image("body_section", context)
            replacements[intro_ph] = url

        # 8. Body section images (from markers)
        body_markers = re.findall(r'__IMG_PLACEHOLDER_(\d+)_\[([^]]+)]__', html)
        for idx_str, placeholder_text in body_markers:
            idx = int(idx_str)
            marker = f"__IMG_PLACEHOLDER_{idx}_[{placeholder_text}]__"
            if idx < len(parsed_copy.body_sections):
                section = parsed_copy.body_sections[idx]
                context = section.image_context or f"Image for: {section.content[:100]}"
            else:
                context = "body section illustration"
            url = await self.generate_image("body_section", context)
            replacements[marker] = url

        # 9. Review person images (from markers)
        review_markers = re.findall(r'__IMG_PLACEHOLDER_review_(\d+)__', html)
        for idx_str in review_markers:
            idx = int(idx_str)
            marker = f"__IMG_PLACEHOLDER_review_{idx}__"
            if idx < len(parsed_copy.reviews):
                review = parsed_copy.reviews[idx]
                context = review.person_description or f"portrait matching name {review.person_name}"
                url = await self.generate_image(
                    "review_person",
                    context,
                    name=review.person_name,
                    aspect_ratio="1:1",
                )
            else:
                url = await self.generate_image("review_person", "satisfied customer", aspect_ratio="1:1")
            replacements[marker] = url

        # 10. Social proof images (from markers)
        social_markers = re.findall(r'__IMG_PLACEHOLDER_social_(\d+)__', html)
        for idx_str in social_markers:
            idx = int(idx_str)
            marker = f"__IMG_PLACEHOLDER_social_{idx}__"
            if idx < len(parsed_copy.social_proofs):
                proof = parsed_copy.social_proofs[idx]
                context = proof.image_context or f"photo of {proof.person_or_group}"
            else:
                context = "expert or authority figure"
            url = await self.generate_image("social_proof", context, aspect_ratio="1:1")
            replacements[marker] = url

        # Apply all replacements
        for placeholder, url in replacements.items():
            html = html.replace(placeholder, url)

        logger.info("Generated %d images total", self.generated_count)
        return html



