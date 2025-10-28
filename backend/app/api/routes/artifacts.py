"""
Artifacts API endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import Optional
import base64

from app.models.artifact import ArtifactCreate, ArtifactResponse, ArtifactListResponse
from app.services.back4app import back4app_service

router = APIRouter()


@router.post("/", response_model=ArtifactResponse, status_code=201)
async def create_artifact(artifact: ArtifactCreate):
    """Create a new artifact"""
    try:
        artifact_data = {
            "scriptId": {"__type": "Pointer", "className": "Script", "objectId": artifact.script_id},
            "scriptVersion": artifact.script_version,
            "name": artifact.name,
            "type": artifact.type.value,
            "content": artifact.content,
            "fileUrl": artifact.file_url,
            "size": artifact.size,
            "metadata": artifact.metadata or {}
        }

        result = await back4app_service.create_artifact(artifact_data)

        return ArtifactResponse(
            objectId=result["objectId"],
            scriptId=artifact.script_id,
            scriptVersion=artifact.script_version,
            name=artifact.name,
            type=artifact.type,
            content=artifact.content,
            file_url=artifact.file_url,
            size=artifact.size,
            metadata=artifact.metadata,
            createdAt=result["createdAt"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create artifact: {str(e)}")


@router.post("/upload", response_model=ArtifactResponse, status_code=201)
async def upload_artifact(
    file: UploadFile = File(...),
    script_id: str = Query(...),
    script_version: str = Query(...),
    artifact_type: str = Query(...)
):
    """Upload an artifact file"""
    try:
        # Read file content
        content = await file.read()

        # Upload to Back4app storage
        file_result = await back4app_service.upload_file(file.filename, content)

        # Create artifact record
        artifact_data = {
            "scriptId": {"__type": "Pointer", "className": "Script", "objectId": script_id},
            "scriptVersion": script_version,
            "name": file.filename,
            "type": artifact_type,
            "fileUrl": file_result["url"],
            "size": len(content),
            "metadata": {
                "originalName": file.filename,
                "contentType": file.content_type
            }
        }

        result = await back4app_service.create_artifact(artifact_data)

        return ArtifactResponse(
            objectId=result["objectId"],
            scriptId=script_id,
            scriptVersion=script_version,
            name=file.filename,
            type=artifact_type,
            file_url=file_result["url"],
            size=len(content),
            metadata=artifact_data["metadata"],
            createdAt=result["createdAt"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload artifact: {str(e)}")


@router.get("/", response_model=ArtifactListResponse)
async def list_artifacts(
    script_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """List artifacts with optional script filter"""
    try:
        result = await back4app_service.list_artifacts(script_id=script_id, limit=page_size)

        artifacts = [
            ArtifactResponse(
                objectId=a["objectId"],
                scriptId=a["scriptId"]["objectId"] if isinstance(a["scriptId"], dict) else a["scriptId"],
                scriptVersion=a.get("scriptVersion", "1.0.0"),
                name=a["name"],
                type=a["type"],
                content=a.get("content"),
                file_url=a.get("fileUrl"),
                size=a.get("size", 0),
                metadata=a.get("metadata"),
                createdAt=a["createdAt"]
            )
            for a in result.get("results", [])
        ]

        return ArtifactListResponse(
            results=artifacts,
            count=len(artifacts),
            total=result.get("count", len(artifacts)),
            page=page,
            page_size=page_size
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list artifacts: {str(e)}")


@router.get("/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(artifact_id: str):
    """Get an artifact by ID"""
    try:
        result = await back4app_service.get_artifact(artifact_id)

        return ArtifactResponse(
            objectId=result["objectId"],
            scriptId=result["scriptId"]["objectId"] if isinstance(result["scriptId"], dict) else result["scriptId"],
            scriptVersion=result.get("scriptVersion", "1.0.0"),
            name=result["name"],
            type=result["type"],
            content=result.get("content"),
            file_url=result.get("fileUrl"),
            size=result.get("size", 0),
            metadata=result.get("metadata"),
            createdAt=result["createdAt"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get artifact: {str(e)}")


@router.delete("/{artifact_id}", status_code=204)
async def delete_artifact(artifact_id: str):
    """Delete an artifact"""
    try:
        await back4app_service.delete_artifact(artifact_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete artifact: {str(e)}")
