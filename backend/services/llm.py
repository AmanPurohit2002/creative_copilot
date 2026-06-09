"""
Groq API integration service.
Uses Groq (running Llama 3 8B) for blazing-fast LLM text generation.
Uses the `instructor` library to guarantee JSON formats mapped to Pydantic models.
"""

import os
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq
import instructor
from pydantic import BaseModel
from typing import Type, TypeVar

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Type variable for Pydantic models
T = TypeVar('T', bound=BaseModel)

# Lazy-initialized client
_client = None

def _get_client():
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise Exception(
                "GROQ_API_KEY is not set. Please add it to your .env file."
            )
        # Initialize Groq client and patch it with instructor to handle Pydantic structured outputs
        _client = instructor.from_groq(AsyncGroq(api_key=GROQ_API_KEY), mode=instructor.Mode.JSON)
    return _client


async def generate_structured_json(
    user_prompt: str, 
    system_prompt: str, 
    response_schema: Type[T]
) -> T:
    """
    Generate structured JSON using Groq and Pydantic models via instructor.

    Args:
        user_prompt: The user request
        system_prompt: The system instruction setting the persona/rules
        response_schema: A Pydantic BaseModel class defining the exact output structure

    Returns:
        An instance of the provided Pydantic model populated with the LLM's response
    """
    client = _get_client()

    try:
        # Instructor's patched AsyncGroq client natively returns the Pydantic model
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_model=response_schema,
            temperature=0.7,
        )

        return response

    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")
