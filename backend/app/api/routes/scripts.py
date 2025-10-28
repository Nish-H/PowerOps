"""
Scripts API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.script import ScriptCreate, ScriptUpdate, ScriptResponse, ScriptListResponse
from app.services.back4app import back4app_service
from app.utils.helpers import calculate_script_metadata

router = APIRouter()


@router.post("/", response_model=ScriptResponse, status_code=201)
async def create_script(script: ScriptCreate):
    """Create a new script"""
    try:
        # Calculate metadata
        metadata = calculate_script_metadata(script.content, script.language.value)

        # Prepare data for Back4app
        script_data = {
            "name": script.name,
            "description": script.description,
            "language": script.language.value,
            "content": script.content,
            "version": script.version,
            "category": script.category.value,
            "tags": script.tags,
            "createdBy": script.created_by,
            "isLatest": True,
            "metadata": metadata.dict() if metadata else {}
        }

        # Create in Back4app
        result = await back4app_service.create_script(script_data)

        # Create initial version
        version_data = {
            "scriptId": {"__type": "Pointer", "className": "Script", "objectId": result["objectId"]},
            "versionNumber": script.version,
            "content": script.content,
            "changelog": "Initial version",
            "createdBy": script.created_by
        }
        await back4app_service.create_version(version_data)

        return ScriptResponse(
            objectId=result["objectId"],
            name=script.name,
            description=script.description,
            language=script.language,
            content=script.content,
            version=script.version,
            category=script.category,
            tags=script.tags,
            created_by=script.created_by,
            createdAt=result["createdAt"],
            updatedAt=result["updatedAt"],
            isLatest=True,
            metadata=metadata
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create script: {str(e)}")


@router.get("/", response_model=ScriptListResponse)
async def list_scripts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    language: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None
):
    """List all scripts with pagination and filters"""
    try:
        skip = (page - 1) * page_size

        # Build where clause
        where = {}
        if language:
            where["language"] = language
        if category:
            where["category"] = category
        if tag:
            where["tags"] = tag

        result = await back4app_service.list_scripts(
            skip=skip,
            limit=page_size,
            where=where if where else None
        )

        scripts = [
            ScriptResponse(
                objectId=s["objectId"],
                name=s["name"],
                description=s.get("description"),
                language=s["language"],
                content=s["content"],
                version=s.get("version", "1.0.0"),
                category=s.get("category", "other"),
                tags=s.get("tags", []),
                created_by=s.get("createdBy", "AI"),
                createdAt=s["createdAt"],
                updatedAt=s["updatedAt"],
                isLatest=s.get("isLatest", True),
                metadata=s.get("metadata")
            )
            for s in result.get("results", [])
        ]

        return ScriptListResponse(
            results=scripts,
            count=len(scripts),
            total=result.get("count", len(scripts)),
            page=page,
            page_size=page_size
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list scripts: {str(e)}")


@router.get("/{script_id}", response_model=ScriptResponse)
async def get_script(script_id: str):
    """Get a script by ID"""
    try:
        result = await back4app_service.get_script(script_id)

        return ScriptResponse(
            objectId=result["objectId"],
            name=result["name"],
            description=result.get("description"),
            language=result["language"],
            content=result["content"],
            version=result.get("version", "1.0.0"),
            category=result.get("category", "other"),
            tags=result.get("tags", []),
            created_by=result.get("createdBy", "AI"),
            createdAt=result["createdAt"],
            updatedAt=result["updatedAt"],
            isLatest=result.get("isLatest", True),
            metadata=result.get("metadata")
        )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Script not found")
        raise HTTPException(status_code=500, detail=f"Failed to get script: {str(e)}")


@router.put("/{script_id}", response_model=ScriptResponse)
async def update_script(script_id: str, script_update: ScriptUpdate):
    """Update a script"""
    try:
        # Get current script
        current = await back4app_service.get_script(script_id)

        # Prepare update data
        update_data = {}
        if script_update.name is not None:
            update_data["name"] = script_update.name
        if script_update.description is not None:
            update_data["description"] = script_update.description
        if script_update.content is not None:
            update_data["content"] = script_update.content
            # Recalculate metadata
            metadata = calculate_script_metadata(
                script_update.content,
                script_update.language.value if script_update.language else current["language"]
            )
            update_data["metadata"] = metadata.dict() if metadata else {}
        if script_update.language is not None:
            update_data["language"] = script_update.language.value
        if script_update.category is not None:
            update_data["category"] = script_update.category.value
        if script_update.tags is not None:
            update_data["tags"] = script_update.tags

        # Update in Back4app
        result = await back4app_service.update_script(script_id, update_data)

        # Get updated script
        updated = await back4app_service.get_script(script_id)

        return ScriptResponse(
            objectId=updated["objectId"],
            name=updated["name"],
            description=updated.get("description"),
            language=updated["language"],
            content=updated["content"],
            version=updated.get("version", "1.0.0"),
            category=updated.get("category", "other"),
            tags=updated.get("tags", []),
            created_by=updated.get("createdBy", "AI"),
            createdAt=updated["createdAt"],
            updatedAt=updated["updatedAt"],
            isLatest=updated.get("isLatest", True),
            metadata=updated.get("metadata")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update script: {str(e)}")


@router.delete("/{script_id}", status_code=204)
async def delete_script(script_id: str):
    """Delete a script"""
    try:
        await back4app_service.delete_script(script_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete script: {str(e)}")
