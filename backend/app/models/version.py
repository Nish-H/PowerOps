"""
Version data models and schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VersionBase(BaseModel):
    """Base version schema"""
    content: str
    changelog: Optional[str] = None


class VersionCreate(VersionBase):
    """Schema for creating a version"""
    script_id: str
    version_number: str
    created_by: str = "AI"


class VersionResponse(VersionBase):
    """Schema for version response"""
    object_id: str = Field(..., alias="objectId")
    script_id: str = Field(..., alias="scriptId")
    version_number: str = Field(..., alias="versionNumber")
    created_by: str = Field(..., alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    hash: str  # SHA-256 hash of content

    class Config:
        populate_by_name = True


class VersionDiff(BaseModel):
    """Schema for version comparison"""
    old_version: str
    new_version: str
    diff: str
    additions: int
    deletions: int
    changes: int


class VersionListResponse(BaseModel):
    """Schema for list of versions"""
    results: List[VersionResponse]
    count: int
    script_id: str
