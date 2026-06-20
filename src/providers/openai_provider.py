import os

from openai import OpenAI

from src.providers.base import AIProvider


class OpenAIProvider(AIProvider):

    def __init__(self):

        self.client = None

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if api_key:

            self.client = OpenAI(
                api_key=api_key
            )

    def chat(
        self,
        prompt: str,
        model: str
    ):

        if not self.client:

            raise Exception(
                "OpenAI API key not configured"
            )

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            response
            .choices[0]
            .message.content
        )
    def health_check(self):

        if not self.client:
            return False

        self.client.models.list()

        return True