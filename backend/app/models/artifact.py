"""
Artifact data models and schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class ArtifactType(str, Enum):
    """Supported artifact types"""
    HTML = "html"
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    LOG = "log"
    IMAGE = "image"
    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    OTHER = "other"


class ArtifactBase(BaseModel):
    """Base artifact schema"""
    name: str = Field(..., min_length=1, max_length=255)
    type: ArtifactType
    content: Optional[str] = None  # For small text artifacts
    file_url: Optional[str] = None  # For large files stored in Back4app
    size: int = 0
    metadata: Optional[Dict[str, Any]] = None


class ArtifactCreate(ArtifactBase):
    """Schema for creating an artifact"""
    script_id: str
    script_version: str


class ArtifactResponse(ArtifactBase):
    """Schema for artifact response"""
    object_id: str = Field(..., alias="objectId")
    script_id: str = Field(..., alias="scriptId")
    script_version: str = Field(..., alias="scriptVersion")
    created_at: datetime = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True


class ArtifactListResponse(BaseModel):
    """Schema for list of artifacts"""
    results: List[ArtifactResponse]
    count: int
    total: int
    page: int
    page_size: int
