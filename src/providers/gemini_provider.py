from google import genai

from src.core.config import (
    GEMINI_API_KEY
)

from src.providers.base import (
    AIProvider
)


class GeminiProvider(
    AIProvider
):

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def chat(
        self,
        prompt: str,
        model: str
    ):

        response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        )

        return response.text

    def health_check(self):

        if not GEMINI_API_KEY:
            raise Exception(
                "Gemini API key missing"
            )

        return True