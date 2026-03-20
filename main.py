from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routers import horoscope

app = FastAPI(
    title="Khemet — Egyptian Astrology API",
    description="Personalized astrological readings grounded in ancient Egyptian cosmology, powered by Claude.",
    version="2.0.0",
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
