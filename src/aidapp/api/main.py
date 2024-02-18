import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aidapp.api.routers import admin

sentry_sdk.init(
    dsn="https://a31edd4f6f92c32659dc2309eff1b95b@o4506740561149952.ingest.sentry.io/4506740561346560",
    enable_tracing=True,
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin.router, prefix="", tags=["admin"])
