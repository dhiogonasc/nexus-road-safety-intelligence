"""src/api/main.py"""

from fastapi import FastAPI
from src.api.routes import ingest

app = FastAPI(
    title="Nexus Road Safety Intelligence API",
    description="API de controle e disparo de ingestão de dados para o pipeline ETL.",
    version="1.0.0",
)

app.include_router(ingest.router, prefix="", tags=["Ingestão"])


@app.get("/", status_code=200)
def root_endpoints():
    """Mapeia dinamicamente todos os endpoints, incluindo os de routers externos."""
    endpoints_list = []

    def extract_routes(router, prefix=""):
        for route in getattr(router, "routes", []):
            if hasattr(route, "path") and hasattr(route, "methods"):
                endpoints_list.append(
                    {
                        "path": prefix + route.path,
                        "methods": sorted(list(route.methods)),
                        "name": getattr(route, "name", "unknown"),
                    }
                )
            elif hasattr(route, "routes"):  # Caso haja sub-routers
                extract_routes(route, prefix=getattr(route, "prefix", ""))

    extract_routes(app)

    return {
        "service": "Nexus Road Safety Intelligence API",
        "version": "1.0.0",
        "total_endpoints": len(endpoints_list),
        "endpoints": endpoints_list,
        "documentation": {"swagger": "/docs", "redoc": "/redoc"},
    }


@app.get("/health", status_code=200)
def health_check():
    """Endpoint de verificação de saúde da API."""
    return {"status": "healthy", "service": "rsi-api"}
