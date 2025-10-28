"""
Search API endpoints
"""

from fastapi import APIRouter, HTTPException, Query

from app.models.script import ScriptListResponse, ScriptResponse
from app.services.back4app import back4app_service

router = APIRouter()


@router.get("/", response_model=ScriptListResponse)
async def search_scripts(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Search scripts by name, description, content, or tags.
    Returns matching scripts ranked by relevance.
    """
    try:
        result = await back4app_service.search_scripts(q, limit=limit)

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
            total=len(scripts),
            page=1,
            page_size=limit
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
