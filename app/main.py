from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "OK"}
