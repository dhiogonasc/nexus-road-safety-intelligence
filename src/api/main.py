"""src/api/main.py"""

from fastapi import FastAPI
from fastapi.routing import APIRoute
from src.api.routes import ingest

app = FastAPI(
    title="Nexus Road Safety Intelligence API",
    description="API de controle e disparo de ingestão de dados para o pipeline ETL.",
    version="1.0.0",
)

app.include_router(ingest.router, prefix="", tags=["Ingestão"])


@app.get("/health", status_code=200)
def health_check():
    """Endpoint de verificação de saúde da API."""
    return {"status": "healthy", "service": "rsi-api"}
