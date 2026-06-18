from abc import ABC, abstractmethod

class AIProvider(ABC):

    @abstractmethod
    def chat(self, prompt: str):
        pass