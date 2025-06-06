from fastapi import FastAPI

from src.api import main_router


app = FastAPI(
    title="Booking API",
)


app.include_router(main_router)
