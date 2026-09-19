from fastapi import APIRouter

from src.services.system_health_service import (
    system_health
)

from src.services.system_integration_audit_service import (
    get_system_integration_report
)

router = APIRouter(
    prefix="/system",
    tags=["system"]
)


@router.get("/health")
def health():

    return system_health()

@router.get(
    "/integration-audit"
)
def integration_audit():

    return (
        get_system_integration_report()
    )