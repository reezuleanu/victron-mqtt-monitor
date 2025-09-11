from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter(tags=["foo"], prefix="/foo")


@router.get("/")
def health(request: Request) -> JSONResponse:
    return JSONResponse({"detail": "foo"})
