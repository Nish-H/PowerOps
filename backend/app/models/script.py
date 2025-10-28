"""
Script data models and schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ScriptLanguage(str, Enum):
    """Supported script languages"""
    PYTHON = "python"
    BASH = "bash"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    POWERSHELL = "powershell"
    RUBY = "ruby"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    OTHER = "other"


class ScriptCategory(str, Enum):
    """Script categories"""
    AUTOMATION = "automation"
    DATA_PROCESSING = "data_processing"
    WEB_SCRAPING = "web_scraping"
    API_INTEGRATION = "api_integration"
    SYSTEM_ADMIN = "system_admin"
    DEVOPS = "devops"
    AI_ML = "ai_ml"
    SECURITY = "security"
    TESTING = "testing"
    UTILITY = "utility"
    OTHER = "other"


class ScriptMetadata(BaseModel):
    """Script metadata"""
    size: int = 0
    lines: int = 0
    complexity: Optional[int] = None
    dependencies: List[str] = []
    execution_time: Optional[float] = None


class ScriptBase(BaseModel):
    """Base script schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    language: ScriptLanguage
    content: str
    category: ScriptCategory = ScriptCategory.OTHER
    tags: List[str] = []
    metadata: Optional[ScriptMetadata] = None


class ScriptCreate(ScriptBase):
    """Schema for creating a script"""
    version: str = "1.0.0"
    created_by: str = "AI"


class ScriptUpdate(BaseModel):
    """Schema for updating a script"""
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    language: Optional[ScriptLanguage] = None
    category: Optional[ScriptCategory] = None
    tags: Optional[List[str]] = None
    metadata: Optional[ScriptMetadata] = None


class ScriptResponse(ScriptBase):
    """Schema for script response"""
    object_id: str = Field(..., alias="objectId")
    version: str
    created_by: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    is_latest: bool = Field(True, alias="isLatest")
    parent_script_id: Optional[str] = Field(None, alias="parentScriptId")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "objectId": "abc123",
                "name": "data_processor.py",
                "description": "Process CSV data and generate reports",
                "language": "python",
                "content": "import pandas as pd\n...",
                "version": "1.0.0",
                "category": "data_processing",
                "tags": ["csv", "reports", "pandas"],
                "created_by": "AI",
                "createdAt": "2025-10-28T10:00:00Z",
                "updatedAt": "2025-10-28T10:00:00Z",
                "isLatest": True
            }
        }


class ScriptListResponse(BaseModel):
    """Schema for list of scripts"""
    results: List[ScriptResponse]
    count: int
    total: int
    page: int
    page_size: int
