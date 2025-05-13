from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", tags=["Test"])
def ping():
    return {"msg": "pong"}
