from src.providers.base import AIProvider


class OpenAIProvider(
    AIProvider
):

    def chat(
        self,
        prompt: str,
        model: str
    ):
        raise NotImplementedError(
            "OpenAI provider not implemented"
        )