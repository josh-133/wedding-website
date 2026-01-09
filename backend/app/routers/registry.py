from fastapi import APIRouter
from .. import schemas, config

router = APIRouter(prefix="/api", tags=["registry"])


@router.get("/registry", response_model=schemas.RegistryResponse)
def get_registry():
    return schemas.RegistryResponse(registry_url=config.REGISTRY_URL)
