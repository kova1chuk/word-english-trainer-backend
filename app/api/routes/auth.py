from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/login",
    summary="User login",
    description="Authenticate user and return a JWT token (not implemented yet).",
    status_code=status.HTTP_200_OK,
)
def login():
    """
    **Login Endpoint**

    Authenticates the user and returns an access token.

    ⚠️ Currently not implemented.
    """
    return JSONResponse(content={"msg": "Login not implemented yet"})
