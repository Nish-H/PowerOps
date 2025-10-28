"""
Integration API endpoints - Critical for Claude AI auto-save functionality
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.models.script import ScriptCreate, ScriptResponse
from app.models.artifact import ArtifactCreate, ArtifactResponse
from app.services.back4app import back4app_service
from app.utils.helpers import calculate_script_metadata, detect_language

router = APIRouter()


class AutoSaveRequest(BaseModel):
    """Request model for auto-saving scripts created by Claude"""
    name: str = Field(..., description="Script name")
    content: str = Field(..., description="Script content")
    description: Optional[str] = Field(None, description="Script description")
    language: Optional[str] = Field(None, description="Programming language (auto-detected if not provided)")
    category: Optional[str] = Field("other", description="Script category")
    tags: List[str] = Field(default_factory=list, description="Tags for the script")
    artifacts: List[Dict[str, Any]] = Field(default_factory=list, description="Associated artifacts")


class AutoSaveResponse(BaseModel):
    """Response model for auto-save operation"""
    script: ScriptResponse
    artifacts: List[ArtifactResponse]
    message: str


@router.post("/auto-save", response_model=AutoSaveResponse, status_code=201)
async def auto_save_script(request: AutoSaveRequest):
    """
    Auto-save a script created during Claude conversation.
    This endpoint is designed to be called automatically when Claude creates a script.

    Features:
    - Automatic language detection
    - Metadata calculation
    - Version creation
    - Artifact storage
    """
    try:
        # Auto-detect language if not provided
        language = request.language or detect_language(request.name, request.content)

        # Calculate metadata
        metadata = calculate_script_metadata(request.content, language)

        # Create script
        script_data = {
            "name": request.name,
            "description": request.description or f"Auto-generated {language} script",
            "language": language,
            "content": request.content,
            "version": "1.0.0",
            "category": request.category,
            "tags": request.tags if request.tags else ["auto-generated", "claude"],
            "createdBy": "Claude AI",
            "isLatest": True,
            "metadata": metadata.dict() if metadata else {}
        }

        script_result = await back4app_service.create_script(script_data)

        # Create initial version
        version_data = {
            "scriptId": {"__type": "Pointer", "className": "Script", "objectId": script_result["objectId"]},
            "versionNumber": "1.0.0",
            "content": request.content,
            "changelog": "Initial auto-save from Claude AI",
            "createdBy": "Claude AI"
        }
        await back4app_service.create_version(version_data)

        # Create artifacts if provided
        artifact_responses = []
        for artifact in request.artifacts:
            artifact_data = {
                "scriptId": {"__type": "Pointer", "className": "Script", "objectId": script_result["objectId"]},
                "scriptVersion": "1.0.0",
                "name": artifact.get("name", "output"),
                "type": artifact.get("type", "text"),
                "content": artifact.get("content"),
                "fileUrl": artifact.get("file_url"),
                "size": len(artifact.get("content", "")),
                "metadata": artifact.get("metadata", {})
            }
            artifact_result = await back4app_service.create_artifact(artifact_data)

            artifact_responses.append(ArtifactResponse(
                objectId=artifact_result["objectId"],
                scriptId=script_result["objectId"],
                scriptVersion="1.0.0",
                name=artifact_data["name"],
                type=artifact_data["type"],
                content=artifact_data.get("content"),
                file_url=artifact_data.get("fileUrl"),
                size=artifact_data["size"],
                metadata=artifact_data["metadata"],
                createdAt=artifact_result["createdAt"]
            ))

        # Create response
        script_response = ScriptResponse(
            objectId=script_result["objectId"],
            name=request.name,
            description=request.description or f"Auto-generated {language} script",
            language=language,
            content=request.content,
            version="1.0.0",
            category=request.category,
            tags=request.tags if request.tags else ["auto-generated", "claude"],
            created_by="Claude AI",
            createdAt=script_result["createdAt"],
            updatedAt=script_result["updatedAt"],
            isLatest=True,
            metadata=metadata
        )

        return AutoSaveResponse(
            script=script_response,
            artifacts=artifact_responses,
            message=f"Script '{request.name}' auto-saved successfully with {len(artifact_responses)} artifact(s)"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto-save failed: {str(e)}")


@router.get("/stats")
async def get_statistics():
    """Get platform statistics"""
    try:
        stats = await back4app_service.get_statistics()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")
