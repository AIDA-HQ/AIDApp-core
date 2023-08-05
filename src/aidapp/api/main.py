from fastapi import FastAPI

from aidapp.api.routers import admin

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(admin.router, prefix="", tags=["admin"])
