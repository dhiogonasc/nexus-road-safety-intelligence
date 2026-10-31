from pathlib import Path
import tempfile
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException
from prefect import task, flow

router = APIRouter(
    prefix="/acidentes",
    tags=[
        "acidentes",
        "ocorrencias",
    ],
)


@task(
    name="Save File",
    task_run_name="save_file: {file_path}",
)
def save_file(
    file_path: str,
    content: bytes,
) -> str:
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    return file_path


@flow(
    name="Save Files",
    task_run_name="save_files",
)
def save_files(
    paths: List[str],
    contents: List[bytes],
) -> List[str]:
    saved_paths = save_file.map(paths, contents)
    return saved_paths.result()


@router.post("/ocorrencias")
async def ingest_ocorrencias(files: List[UploadFile] = File(...)):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            paths = []
            contents = []

            for file in files:
                if not file.filename:
                    continue

                file_path = Path(temp_dir, file.filename).as_posix()
                content = await file.read()

                paths.append(file_path)
                contents.append(content)

            if not paths:
                return {"message": "failed"}

            saved_files = save_files(
                paths=paths,
                contents=contents,
            )

            return {
                "message": "success",
                "saved_files": [Path(file_path).name for file_path in saved_files],
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
