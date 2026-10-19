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


@app.get("/", status_code=200)
def root_endpoints():
    """Mapeia dinamicamente todos os endpoints ativos na aplicação."""
    endpoints_list = []

    for route in app.routes:
        if isinstance(route, APIRoute):
            endpoints_list.append(
                {
                    "path": route.path,
                    "methods": sorted(list(route.methods)),
                    "name": route.name,
                }
            )

    return {
        "service": "Nexus Road Safety Intelligence API",
        "version": "1.0.0",
        "total_endpoints": len(endpoints_list),
        "endpoints": endpoints_list,
    }


@app.get("/health", status_code=200)
def health_check():
    """Endpoint de verificação de saúde da API."""
    return {"status": "healthy", "service": "rsi-api"}
