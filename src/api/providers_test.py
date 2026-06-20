from fastapi import APIRouter

from src.providers.openai_provider import (
    OpenAIProvider
)

router = APIRouter()


@router.get(
    "/atlas/test-openai"
)
def test_openai():

    provider = OpenAIProvider()

    response = provider.chat(
        "Say hello",
        "gpt-4.1-mini"
    )

    return {
        "response": response
    }