from openai import OpenAI

from src.core.config import (
    GITHUB_MODELS_API_KEY
)

from src.providers.base import (
    AIProvider
)


class GitHubProvider(
    AIProvider
):

    def __init__(self):

        self.client = OpenAI(
            api_key=GITHUB_MODELS_API_KEY,
            base_url="https://models.inference.ai.azure.com"
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