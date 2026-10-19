"""src/api/routes/ingest.py"""

from fastapi import APIRouter, BackgroundTasks, HTTPException

from config import settings
from pipeline.dag_main import flow_main
from pipeline.stage.dag_setup import flow_setup
from pipeline.stage.dag_bronze import flow_bronze
from pipeline.stage.dag_silver import flow_silver
from pipeline.stage.dag_gold import flow_gold
from src.pipeline.index import PIPELINE_CONFIG

router = APIRouter()


@router.post(
    path="/{domain}/ingest",
    status_code=202,
)
def main_ingestion(domain: str, background_tasks: BackgroundTasks):
    """
    Dispara o pipeline ETL completo (Setup, Bronze, Silver, Gold) para o domínio especificado
    de forma assíncrona em segundo plano.
    """
    if domain not in PIPELINE_CONFIG:
        raise HTTPException(
            status_code=404,
            detail=f"Domínio '{domain}' não encontrado ou não configurado no pipeline.",
        )

    database = settings.domain_db_path(domain=domain)

    background_tasks.add_task(
        flow_main,
        database=database,
        domain=domain,
    )

    return {
        "message": f"Pipeline completo para o domínio '{domain}' acionado com sucesso.",
        "domain": domain,
        "status": "processing_in_background",
    }


@router.post(
    path="/{domain}/ingest/setup",
    status_code=202,
)
def setup_stage(domain: str, background_tasks: BackgroundTasks):
    """Dispara apenas o estágio de Setup (extensões e schemas) em background."""
    if domain not in PIPELINE_CONFIG:
        raise HTTPException(
            status_code=404,
            detail=f"Domínio '{domain}' não encontrado ou não configurado no pipeline.",
        )

    database = settings.domain_db_path(domain=domain)

    background_tasks.add_task(
        flow_setup,
        database=database,
    )

    return {
        "message": f"Estágio Setup acionado para o domínio '{domain}'.",
        "domain": domain,
        "status": "processing_in_background",
    }


@router.post(
    path="/{domain}/ingest/bronze",
    status_code=202,
)
def bronze_stage(domain: str, background_tasks: BackgroundTasks):
    """Dispara apenas o estágio Bronze (Extração CSV) em background."""
    if domain not in PIPELINE_CONFIG:
        raise HTTPException(
            status_code=404,
            detail=f"Domínio '{domain}' não encontrado ou não configurado no pipeline.",
        )

    database = settings.domain_db_path(domain=domain)

    background_tasks.add_task(
        flow_bronze,
        database=database,
        domain=domain,
    )

    return {
        "message": f"Estágio Bronze acionado para o domínio '{domain}'.",
        "domain": domain,
        "status": "processing_in_background",
    }


@router.post(
    path="/{domain}/ingest/silver",
    status_code=202,
)
def silver_stage(domain: str, background_tasks: BackgroundTasks):
    """Dispara apenas o estágio Silver (Transformações/Dimensões/Fatos) em background."""
    if domain not in PIPELINE_CONFIG:
        raise HTTPException(
            status_code=404,
            detail=f"Domínio '{domain}' não encontrado ou não configurado no pipeline.",
        )

    database = settings.domain_db_path(domain=domain)

    background_tasks.add_task(
        flow_silver,
        database=database,
        domain=domain,
    )

    return {
        "message": f"Estágio Silver acionado para o domínio '{domain}'.",
        "domain": domain,
        "status": "processing_in_background",
    }


@router.post(
    path="/{domain}/ingest/gold",
    status_code=202,
)
def gold_stage(domain: str, background_tasks: BackgroundTasks):
    """Dispara apenas o estágio Gold (Agregações e Sync Cloud Postgres) em background."""
    if domain not in PIPELINE_CONFIG:
        raise HTTPException(
            status_code=404,
            detail=f"Domínio '{domain}' não encontrado ou não configurado no pipeline.",
        )

    database = settings.domain_db_path(domain=domain)

    background_tasks.add_task(
        flow_gold,
        database=database,
        domain=domain,
    )

    return {
        "message": f"Estágio Gold acionado para o domínio '{domain}'.",
        "domain": domain,
        "status": "processing_in_background",
    }
