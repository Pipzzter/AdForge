"""
Gemini LLM Client
=================

Client for interacting with Google's Gemini API using the official google-genai SDK.
Supports Gemini 3.1 Pro with thinking_level parameter.
"""

import asyncio
import logging
import random
from typing import Optional, Type, TypeVar

from google import genai
from google.genai import types
from google.genai.types import ThinkingLevel
from pydantic import BaseModel

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# Gemini 3.1 Pro model ID (preview as of Feb 2026)
DEFAULT_MODEL = "gemini-3.1-pro-preview"

T = TypeVar("T", bound=BaseModel)


class GeminiResponse(BaseModel):
    """Response from Gemini API."""

    text: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    cached_tokens: Optional[int] = None


class GeminiClient:
    """
    Client for Google Gemini API using the official google-genai SDK.

    Supports Gemini 3.1 Pro with:
    - thinking_level parameter (low/medium/high)
    - Structured output via Pydantic models
    - Retry logic with exponential backoff for rate limits

    Usage:
        client = GeminiClient()
        response = await client.generate("Your prompt here")
        structured = await client.generate_structured("Your prompt", MySchema)
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
    ) -> None:
        self.model = model
        self.client = genai.Client(
            api_key=api_key or get_settings().gemini_api_key
        )

    async def generate(
        self,
        prompt: str,
        thinking_level: ThinkingLevel = ThinkingLevel.LOW,
        max_tokens: int = 65536,
        max_retries: int = 3,
    ) -> GeminiResponse:
        """
        Generate text using Gemini API.

        Args:
            prompt: The prompt to send to the model
            thinking_level: low/medium/high - controls reasoning depth
            max_tokens: Maximum output tokens (default 64k)
            max_retries: Number of retries for transient errors

        Returns:
            GeminiResponse with generated text and token usage
        """
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
            max_output_tokens=max_tokens,
        )

        logger.debug(
            "Sending request to Gemini API: model=%s, thinking_level=%s",
            self.model,
            thinking_level,
        )

        return await self._call_with_retry(prompt, config, max_retries)

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        thinking_level: ThinkingLevel = ThinkingLevel.LOW,
        max_tokens: int = 65536,
        max_retries: int = 3,
    ) -> T:
        """
        Generate structured output parsed directly into a Pydantic model.

        Args:
            prompt: The prompt to send to the model
            schema: Pydantic model class to parse the response into
            thinking_level: low/medium/high - controls reasoning depth
            max_tokens: Maximum output tokens
            max_retries: Number of retries for transient errors

        Returns:
            Instance of the provided Pydantic schema
        """
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
            max_output_tokens=max_tokens,
            response_mime_type="application/json",
            response_json_schema=schema.model_json_schema(),
        )

        logger.debug(
            "Sending structured request to Gemini API: model=%s, schema=%s, thinking_level=%s",
            self.model,
            schema.__name__,
            thinking_level,
        )

        response = await self._call_with_retry(prompt, config, max_retries)

        if not response.text:
            raise ValueError(
                f"Gemini returned empty response for schema {schema.__name__}. "
                "This can happen when thinking mode conflicts with structured output."
            )

        logger.debug(
            "Parsing structured response for schema=%s, text_length=%d, preview=%s",
            schema.__name__,
            len(response.text),
            response.text[:200],
        )

        return schema.model_validate_json(response.text)

    async def _call_with_retry(
        self,
        prompt: str,
        config: types.GenerateContentConfig,
        max_retries: int,
    ) -> GeminiResponse:
        """Execute the API call with exponential backoff retry logic."""
        last_error: Optional[Exception] = None

        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model,
                    contents=prompt,
                    config=config,
                )

                usage = response.usage_metadata
                prompt_tokens = getattr(usage, "prompt_token_count", None)
                completion_tokens = getattr(usage, "candidates_token_count", None)
                cached_tokens = getattr(usage, "cached_content_token_count", None)

                logger.info(
                    "Gemini response received: prompt_tokens=%s, completion_tokens=%s, cached=%s",
                    prompt_tokens,
                    completion_tokens,
                    cached_tokens,
                )

                return GeminiResponse(
                    text=response.text,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    cached_tokens=cached_tokens,
                )

            except Exception as e:
                last_error = e
                error_str = str(e)

                # Retry on rate limit or transient errors
                if "429" in error_str or "503" in error_str or "timeout" in error_str.lower():
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        "Transient error on attempt %d/%d: %s. Retrying in %.1fs",
                        attempt + 1,
                        max_retries,
                        error_str[:200],
                        wait_time,
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("Gemini API error (non-retryable): %s", error_str[:500])
                    raise

        if last_error:
            raise last_error
        raise RuntimeError("Max retries exhausted with no response")

