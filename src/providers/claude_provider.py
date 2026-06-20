from src.providers.base import AIProvider


class ClaudeProvider(
    AIProvider
):

    def chat(
        self,
        prompt: str,
        model: str
    ):
        raise NotImplementedError(
            "Claude provider not implemented"
        )
    def health_check(self):
        return False