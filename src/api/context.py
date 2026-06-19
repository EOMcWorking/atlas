from fastapi import APIRouter

from src.services.context_builder import (
    build_context
)

router = APIRouter()


@router.get(
    "/atlas/context-preview"
)
def context_preview():

    context = build_context(
        "Review Atlas architecture"
    )

    return {
        "characters":
        len(context),

        "preview":
        context[:3000]
    }