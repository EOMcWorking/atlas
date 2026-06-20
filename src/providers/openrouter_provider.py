from openai import OpenAI

from src.core.config import OPENROUTER_API_KEY
from src.providers.base import AIProvider


class OpenRouterProvider(
    AIProvider
):

    def __init__(self):

        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

    def chat(
        self,
        prompt: str,
        model: str
    ):

        response = (
            self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    def health_check(self):

        if not self.client:
            return False
        
        self.client.models.list()

        return True