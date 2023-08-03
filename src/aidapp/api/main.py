from fastapi import FastAPI
from aidapp.api.routers import admin

app = FastAPI()

app.include_router(admin.router, prefix="", tags=["admin"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
