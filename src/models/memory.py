from pydantic import BaseModel

class MemoryEntry(BaseModel):
    text: str