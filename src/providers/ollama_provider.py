import ollama

from src.providers.base import AIProvider


class OllamaProvider(AIProvider):

    def chat(self, prompt: str, model: str):
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]