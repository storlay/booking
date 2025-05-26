from fastapi import FastAPI

from src.hotels import router as hotels_router

app = FastAPI(
    title="Booking API",
)


app.include_router(hotels_router)