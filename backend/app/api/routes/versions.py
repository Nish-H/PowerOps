"""
Versions API endpoints
"""

from fastapi import APIRouter, HTTPException
import difflib

from app.models.version import VersionCreate, VersionResponse, VersionListResponse, VersionDiff
from app.services.back4app import back4app_service

router = APIRouter()


@router.post("/", response_model=VersionResponse, status_code=201)
async def create_version(version: VersionCreate):
    """Create a new version for a script"""
    try:
        version_data = {
            "scriptId": {"__type": "Pointer", "className": "Script", "objectId": version.script_id},
            "versionNumber": version.version_number,
            "content": version.content,
            "changelog": version.changelog,
            "createdBy": version.created_by
        }

        result = await back4app_service.create_version(version_data)

        return VersionResponse(
            objectId=result["objectId"],
            scriptId=version.script_id,
            versionNumber=version.version_number,
            content=version.content,
            changelog=version.changelog,
            createdBy=version.created_by,
            createdAt=result["createdAt"],
            hash=result.get("hash", "")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create version: {str(e)}")


@router.get("/script/{script_id}", response_model=VersionListResponse)
async def list_versions(script_id: str):
    """Get all versions for a script"""
    try:
        result = await back4app_service.get_versions(script_id)

        versions = [
            VersionResponse(
                objectId=v["objectId"],
                scriptId=script_id,
                versionNumber=v["versionNumber"],
                content=v["content"],
                changelog=v.get("changelog"),
                createdBy=v.get("createdBy", "AI"),
                createdAt=v["createdAt"],
                hash=v.get("hash", "")
            )
            for v in result.get("results", [])
        ]

        return VersionListResponse(
            results=versions,
            count=len(versions),
            script_id=script_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list versions: {str(e)}")


@router.get("/{version_id}", response_model=VersionResponse)
async def get_version(version_id: str):
    """Get a specific version"""
    try:
        result = await back4app_service.get_version(version_id)

        return VersionResponse(
            objectId=result["objectId"],
            scriptId=result["scriptId"]["objectId"],
            versionNumber=result["versionNumber"],
            content=result["content"],
            changelog=result.get("changelog"),
            createdBy=result.get("createdBy", "AI"),
            createdAt=result["createdAt"],
            hash=result.get("hash", "")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get version: {str(e)}")


@router.get("/diff/{version_id_1}/{version_id_2}", response_model=VersionDiff)
async def compare_versions(version_id_1: str, version_id_2: str):
    """Compare two versions and return diff"""
    try:
        # Get both versions
        v1 = await back4app_service.get_version(version_id_1)
        v2 = await back4app_service.get_version(version_id_2)

        # Generate unified diff
        diff = difflib.unified_diff(
            v1["content"].splitlines(keepends=True),
            v2["content"].splitlines(keepends=True),
            fromfile=f'Version {v1["versionNumber"]}',
            tofile=f'Version {v2["versionNumber"]}',
            lineterm=''
        )

        diff_text = ''.join(diff)

        # Count changes
        additions = diff_text.count('\n+') - 1  # Exclude header
        deletions = diff_text.count('\n-') - 1  # Exclude header
        changes = max(additions, deletions)

        return VersionDiff(
            old_version=v1["versionNumber"],
            new_version=v2["versionNumber"],
            diff=diff_text,
            additions=additions,
            deletions=deletions,
            changes=changes
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compare versions: {str(e)}")
