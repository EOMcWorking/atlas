from fastapi import APIRouter

from src.services.rule_inspector_service import (
    inspect_architecture
)

router = APIRouter()


@router.get(
    "/atlas/recommendations"
)
def recommendations():

    inspection = (
        inspect_architecture()
    )

    priorities = inspection.get(
        "priorities",
        []
    )

    return {
        "priority_1":
            priorities[0]
            if len(priorities) > 0
            else None,

        "priority_2":
            priorities[1]
            if len(priorities) > 1
            else None,

        "priority_3":
            priorities[2]
            if len(priorities) > 2
            else None
    }