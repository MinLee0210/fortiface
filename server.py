import uvicorn

from fortiface.core.config import settings

if __name__ == "__main__":
    if settings.ENVIRONMENT == "dev":
        uvicorn.run("app.main:app", host=settings.HOST, reload=True, port=settings.PORT)
    else:
        uvicorn.run(
            "app.main:app", host=settings.HOST, reload=False, port=settings.PORT
        )
