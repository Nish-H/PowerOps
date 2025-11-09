"""
Shared Back4app service for Vercel serverless functions
"""

import httpx
import json
import hashlib
import os
from typing import Dict, Any, Optional


class Back4appService:
    """Service for interacting with Back4app Parse Server"""

    def __init__(self):
        self.base_url = os.environ.get("BACK4APP_SERVER_URL", "https://parseapi.back4app.com")
        self.app_id = os.environ.get("BACK4APP_APPLICATION_ID", "")
        self.rest_api_key = os.environ.get("BACK4APP_REST_API_KEY", "")
        self.headers = {
            "X-Parse-Application-Id": self.app_id,
            "X-Parse-REST-API-Key": self.rest_api_key,
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Back4app"""
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    # Script Operations
    async def create_script(self, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new script in Back4app"""
        return await self._request("POST", "/classes/Script", data=script_data)

    async def get_script(self, object_id: str) -> Dict[str, Any]:
        """Get a script by ID"""
        return await self._request("GET", f"/classes/Script/{object_id}")

    async def update_script(self, object_id: str, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a script"""
        return await self._request("PUT", f"/classes/Script/{object_id}", data=script_data)

    async def delete_script(self, object_id: str) -> Dict[str, Any]:
        """Delete a script"""
        return await self._request("DELETE", f"/classes/Script/{object_id}")

    async def list_scripts(
        self,
        skip: int = 0,
        limit: int = 100,
        where: Optional[Dict] = None,
        order: str = "-createdAt"
    ) -> Dict[str, Any]:
        """List scripts with pagination"""
        params = {
            "skip": skip,
            "limit": limit,
            "order": order
        }
        if where:
            params["where"] = json.dumps(where)

        return await self._request("GET", "/classes/Script", params=params)

    async def search_scripts(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """Search scripts by name, description, or content"""
        where = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}},
                {"tags": {"$in": [query]}}
            ]
        }
        return await self.list_scripts(limit=limit, where=where)

    # Version Operations
    async def create_version(self, version_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new version"""
        content = version_data.get("content", "")
        version_data["hash"] = hashlib.sha256(content.encode()).hexdigest()
        return await self._request("POST", "/classes/ScriptVersion", data=version_data)

    async def get_versions(self, script_id: str, limit: int = 100) -> Dict[str, Any]:
        """Get all versions for a script"""
        where = {"scriptId": {"__type": "Pointer", "className": "Script", "objectId": script_id}}
        params = {
            "where": json.dumps(where),
            "limit": limit,
            "order": "-createdAt"
        }
        return await self._request("GET", "/classes/ScriptVersion", params=params)

    async def get_version(self, version_id: str) -> Dict[str, Any]:
        """Get a specific version"""
        return await self._request("GET", f"/classes/ScriptVersion/{version_id}")

    # Artifact Operations
    async def create_artifact(self, artifact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new artifact"""
        return await self._request("POST", "/classes/Artifact", data=artifact_data)

    async def get_artifact(self, object_id: str) -> Dict[str, Any]:
        """Get an artifact by ID"""
        return await self._request("GET", f"/classes/Artifact/{object_id}")

    async def list_artifacts(
        self,
        script_id: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """List artifacts, optionally filtered by script"""
        params = {"limit": limit, "order": "-createdAt"}

        if script_id:
            where = {"scriptId": {"__type": "Pointer", "className": "Script", "objectId": script_id}}
            params["where"] = json.dumps(where)

        return await self._request("GET", "/classes/Artifact", params=params)

    async def delete_artifact(self, object_id: str) -> Dict[str, Any]:
        """Delete an artifact"""
        return await self._request("DELETE", f"/classes/Artifact/{object_id}")

    # Statistics
    async def get_statistics(self) -> Dict[str, Any]:
        """Get platform statistics"""
        script_count = await self._request("GET", "/classes/Script", params={"count": 1, "limit": 0})
        artifact_count = await self._request("GET", "/classes/Artifact", params={"count": 1, "limit": 0})
        version_count = await self._request("GET", "/classes/ScriptVersion", params={"count": 1, "limit": 0})

        return {
            "total_scripts": script_count.get("count", 0),
            "total_artifacts": artifact_count.get("count", 0),
            "total_versions": version_count.get("count", 0)
        }


# Create singleton instance
back4app_service = Back4appService()
