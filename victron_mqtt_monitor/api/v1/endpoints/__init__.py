from fastapi import APIRouter
from .foo import router as foo_router

router = APIRouter()
router.include_router(foo_router)
