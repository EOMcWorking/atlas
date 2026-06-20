from openai import OpenAI

from src.core.config import (
    GROQ_API_KEY
)

from src.providers.base import (
    AIProvider
)


class GroqProvider(
    AIProvider
):

    def __init__(self):

        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
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

        self.client.models.list()

        return True