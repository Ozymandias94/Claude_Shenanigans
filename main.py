from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routers import horoscope

app = FastAPI(
    title="AI Horoscope API",
    description="Personalized daily horoscope readings powered by Claude across Western, Vedic, Chinese, and Egyptian traditions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(horoscope.router)


@app.get("/health")
def health():
    return {"status": "ok"}
