"""
Gemini Image Client (Nano Banana)
==================================

Wraps gemini-2.5-flash-image for photorealistic image generation.
Returns base64 data URIs for direct embedding in HTML.

Model: gemini-2.5-flash-image  (cheapest / fastest — Nano Banana)
Docs:  project_docs/nano_banana.md
"""

import asyncio
import base64
import logging
import random
from enum import Enum
from typing import Optional

from google import genai
from google.genai import types

from app.core.config import get_settings

logger = logging.getLogger(__name__)

IMAGE_MODEL = "gemini-2.5-flash-image"


class ImageType(str, Enum):
    """Type of advertorial image to generate."""

    HEADLINE = "headline"
    BODY = "body"
    PRODUCT = "product"


# =============================================================================
# SYSTEM PROMPTS FOR ADVERTORIAL IMAGE GENERATION
# =============================================================================

HEADLINE_IMAGE_SYSTEM_PROMPT = """
## Headline Images – AI Generation Instructions

### Core Goal (Very Important)
The headline image exists for one reason only: Create extreme curiosity and force 
the reader to continue reading the advertorial. It must visually support what the 
headline is saying without explaining it fully.

- If the image answers the question → it FAILED.
- If the image makes the reader think "wait… why?" → it WORKED.

### Core Rules (Non-Negotiable)

1. **The image must visually express the headline**
   - The reader should instantly feel that the image and headline belong together.
   - The image should show the situation or moment the headline is hinting at — 
     NOT the solution, NOT the product.

2. **Curiosity is more important than clarity**
   The image should:
   - Feel unfinished
   - Suggest something happening or about to happen
   - Make the viewer want context
   - The goal is continuation, not explanation.

3. **It must feel real, not like an ad**
   Images should look:
   - Editorial
   - Candid
   - Observational
   - NOT staged, polished, or commercial.

### Image Type Choice (Critical)

#### GIF / Animation (Preferred)
Use a GIF or subtle animation whenever motion increases curiosity.
Best used when the headline implies:
- A process
- A change over time
- Something hidden inside the body or situation
- A cause that isn't obvious

Animation rules:
- 2–4 second loop
- Very subtle movement only
- Natural motion (breathing, hand movement, slow zoom, light change)
- No effects, no text, no dramatic transitions
- The animation should feel like a living moment, not a graphic.

#### Static Image
Use a static image only when a frozen moment creates more tension or mystery.
Best used when:
- One specific moment says enough
- The stillness itself feels uncomfortable or intriguing
- Motion would reduce impact

The static image should feel like it was captured mid-moment, not posed.

### Absolute Do-Nots
- NO product
- NO logos
- NO text or captions
- NO obvious advertising style
- NO perfect stock models
""".strip()


BODY_IMAGE_SYSTEM_PROMPT = """
## Body Section Images – AI Generation Instructions

### Core Goal
Body section images exist to visually explain the exact idea of that section in the 
simplest possible way. Each image must act like a visual translation of the section's 
core message, especially for an older reader.

If someone only skimmed the text + image, they should still "get it".

### Core Rules (Non-Negotiable)

1. **One section = one core idea = one image**
   Before generating any image, define: "What is the single idea this section is 
   trying to explain?" The image must only communicate that idea.
   - No mixing concepts
   - No jumping ahead
   
   Example logic (not prompts):
   - Section talks about treatments being destroyed before reaching lungs → 
     image shows that loss visually
   - Section talks about digestion stopping medication → 
     image shows stomach/liver blocking flow
   - Section talks about direct delivery → 
     image shows clear path to lungs

2. **Images must explain, not decorate**
   Body images are functional, not aesthetic. They must:
   - Simplify a complex idea
   - Reduce mental effort
   - Make the explanation feel obvious
   - If the image can be removed without losing understanding → it FAILED.

3. **Must be understandable for an older reader**
   Assume:
   - Slower reading pace
   - Less tolerance for abstraction
   - Needs clear cause → effect visuals
   
   That means:
   - Simple compositions
   - Clear focus
   - No clutter
   - No clever metaphors that require interpretation

### Static vs GIF / Animation (Important)

#### Static Images (Default)
Use static images when:
- Showing a situation
- Showing a person's condition
- Showing a comparison in a simple way
- Showing "this is happening" moments

Static images should feel:
- Calm
- Clear
- Observational
- Editorial (not ad-like)

#### GIF / Animation (Required for mechanisms)
Use GIFs / subtle animations when explaining a mechanism or process, especially:
- Digestion
- Absorption
- Blockage
- Delivery paths
- Cause-and-effect over time

**In this advertorial, mechanism sections MUST use GIFs.**

Animation rules:
- 2–5 second loop
- Slow, explanatory motion
- No effects, no text overlays
- Motion should clarify, not distract

Think: "Educational animation you'd see in a serious article — simplified."

### How Images Should Relate to the Copy (Critical)
- The image must reflect what the reader just read, not what comes next
- Images should sit exactly where understanding might drop
- They should visually confirm: "Yes, this makes sense now"

Examples applied to copy:
- Stuck mucus section → visual shows mucus physically blocking airways
- 5% problem section → visual shows most of substance disappearing before lungs
- Doctor discovery section → visual shows research, charts, late-night investigation
- Direct delivery vs swallowing → visual shows two paths, one failing, one reaching lungs
""".strip()


PRODUCT_IMAGE_SYSTEM_PROMPT = """
## Product Introduction Images – AI Generation Instructions

### Core Goal
Product introduction images exist to visually prove how the product works the moment 
it is introduced. This is where the reader shifts from:
"I understand the problem" → "I understand why this solution makes sense."

### Core Rules (Non-Negotiable)

1. **Images must match the exact product being sold**
   - The product shown must be identical to the real product
   - Same form factor, delivery method, and usage
   - No generic or "similar-looking" products
   - If the image doesn't match the product → it CANNOT be used.

2. **The image must explain the product's mechanism**
   This is the most important rule. The image must visually demonstrate what makes 
   the product work, not just show it.
   
   If the product works via:
   - Direct delivery
   - Bypassing digestion
   - Targeted absorption
   
   The image must show that process clearly. This is NOT optional.

### Image Types

#### Type 1 — Mechanism GIF / Animation (Primary, Mandatory)
This is the default and preferred format.

Use when:
- Introducing the product
- Explaining why it works better than alternatives
- Showing cause → effect

Typical structure:
- Split screen (recommended)
- One side: the real product
- Other side: animated mechanism (e.g. direct airway delivery)

Animation rules:
- 3–6 second loop
- Clean, slow, explanatory motion
- No text overlays
- No dramatic effects
- Feels educational, not promotional

The animation should answer: "How does this product actually reach the problem area?"

#### Type 2 — Standalone Product Images (Secondary)
Used only to:
- Ground the product visually
- Reinforce legitimacy and realism

Rules:
- Neutral background or realistic environment
- Soft lighting
- No badges, no claims, no CTA
- Clean, calm, credible

These images do not explain — they support.

### Overall Visual Tone
- Educational
- Trustworthy
- Calm
- Clinical-but-human
- Nothing should feel like an ad.
""".strip()


def get_system_prompt_for_image_type(image_type: ImageType) -> str:
    """Return the appropriate system prompt based on image type."""
    prompts = {
        ImageType.HEADLINE: HEADLINE_IMAGE_SYSTEM_PROMPT,
        ImageType.BODY: BODY_IMAGE_SYSTEM_PROMPT,
        ImageType.PRODUCT: PRODUCT_IMAGE_SYSTEM_PROMPT,
    }
    return prompts.get(image_type, BODY_IMAGE_SYSTEM_PROMPT)



class GeminiImageClient:
    """
    Generates images using Gemini 2.5 Flash Image (Nano Banana).

    Returns base64 data URIs for direct embedding in HTML, eliminating
    the need for file storage and separate HTTP requests.

    Supports three image types for advertorial generation:
    - HEADLINE: Curiosity-driven images that force readers to continue
    - BODY: Explanatory images that simplify complex ideas
    - PRODUCT: Product introduction images that demonstrate mechanism

    Usage:
        client = GeminiImageClient()

        # Headline image (creates curiosity)
        data_uri = await client.generate(
            "A photorealistic ...",
            image_type=ImageType.HEADLINE,
            aspect_ratio="16:9"
        )

        # Body image (explains concept)
        data_uri = await client.generate(
            "A clear visual showing ...",
            image_type=ImageType.BODY,
            aspect_ratio="4:3"
        )

        html = f'<img src="{data_uri}" />'
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = genai.Client(
            api_key=api_key or get_settings().gemini_api_key
        )

    async def generate(
        self,
        prompt: str,
        image_type: ImageType = ImageType.BODY,
        aspect_ratio: str = "4:3",
        max_retries: int = 3,
    ) -> str:
        """
        Generate one image from a text prompt, return as base64 data URI.

        The system prompt is automatically selected based on the image_type to ensure
        the generated image follows the advertorial guidelines:

        - HEADLINE: Creates curiosity, feels editorial/candid, no product/logos
        - BODY: Explains one core idea clearly, simple composition, educational
        - PRODUCT: Shows product mechanism, trustworthy, clinical-but-human

        Args:
            prompt:       Photorealistic description of the image.
            image_type:   Type of advertorial image (HEADLINE, BODY, PRODUCT).
            aspect_ratio: One of: 1:1 | 2:3 | 3:2 | 3:4 | 4:3 | 4:5 | 5:4
                          | 9:16 | 16:9 | 21:9
            max_retries:  Retries on transient errors.

        Returns:
            Base64 data URI string, e.g. "data:image/png;base64,iVBORw0..."
        """
        # Get the appropriate system prompt for this image type
        system_prompt = get_system_prompt_for_image_type(image_type)

        # Combine system prompt with user prompt for better guidance
        full_prompt = f"{system_prompt}\n\n---\n\n## Image Request:\n{prompt}"

        config = types.GenerateContentConfig(
            response_modalities=["Image"],
            image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
        )

        last_error: Optional[Exception] = None

        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=IMAGE_MODEL,
                    contents=[full_prompt],
                    config=config,
                )

                for part in response.parts:
                    # Skip thought parts
                    if getattr(part, "thought", False):
                        continue
                    if part.inline_data is not None:
                        # Get raw image bytes directly from inline_data
                        image_bytes = part.inline_data.data
                        mime_type = part.inline_data.mime_type or "image/png"
                        b64_data = base64.b64encode(image_bytes).decode("utf-8")
                        data_uri = f"data:{mime_type};base64,{b64_data}"

                        logger.info(
                            "Image generated: type=%s aspect_ratio=%s size=%d bytes prompt_preview=%s",
                            image_type.value,
                            aspect_ratio,
                            len(image_bytes),
                            prompt[:80],
                        )
                        return data_uri

                raise ValueError("Gemini image response contained no inline_data part")

            except Exception as e:
                last_error = e
                err_str = str(e)
                if "429" in err_str or "503" in err_str or "timeout" in err_str.lower():
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        "Image generation transient error attempt %d/%d: %s — retrying in %.1fs",
                        attempt + 1,
                        max_retries,
                        err_str[:200],
                        wait,
                    )
                    await asyncio.sleep(wait)
                else:
                    logger.error("Image generation failed (non-retryable): %s", err_str[:300])
                    raise

        if last_error:
            raise last_error
        raise RuntimeError("Image generation: max retries exhausted with no result")

