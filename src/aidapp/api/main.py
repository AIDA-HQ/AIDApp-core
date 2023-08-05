from fastapi import FastAPI

from aidapp.api.routers import admin

app = FastAPI()

app.include_router(admin.router, prefix="", tags=["admin"])
