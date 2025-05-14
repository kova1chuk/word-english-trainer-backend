from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["Health"],
)


@router.get(
    "",
    summary="Health check",
    description="Returns OK if the server is running.",
    status_code=status.HTTP_200_OK,
    response_description="Status OK",
)
def health_check():
    """
    **Health Check Endpoint**

    Used for monitoring or confirming if the API is responsive.
    """
    return JSONResponse(content={"status": "OK"})
