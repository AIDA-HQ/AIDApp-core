from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aidapp.api.routers import admin

app = FastAPI()

origins = ["http://localhost:5173", "https://aidapp-fe.vercel.app/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin.router, prefix="", tags=["admin"])
