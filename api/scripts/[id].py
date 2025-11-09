"""
Serverless function for /api/scripts/[id]
Handles: GET (get script), PUT (update script), DELETE (delete script)
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from _lib.back4app import back4app_service
from _lib.helpers import calculate_script_metadata


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _get_script_id(self):
        """Extract script ID from path"""
        # Path format: /api/scripts/[id]
        parts = self.path.split('/')
        return parts[-1].split('?')[0]  # Remove query params if any

    def do_GET(self):
        """Get script by ID"""
        try:
            script_id = self._get_script_id()

            import asyncio
            result = asyncio.run(back4app_service.get_script(script_id))

            response = {
                "objectId": result["objectId"],
                "name": result["name"],
                "description": result.get("description"),
                "language": result["language"],
                "content": result["content"],
                "version": result.get("version", "1.0.0"),
                "category": result.get("category", "other"),
                "tags": result.get("tags", []),
                "created_by": result.get("createdBy", "AI"),
                "createdAt": result["createdAt"],
                "updatedAt": result["updatedAt"],
                "isLatest": result.get("isLatest", True),
                "metadata": result.get("metadata")
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_response(404 if "not found" in str(e).lower() else 500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_PUT(self):
        """Update script"""
        try:
            script_id = self._get_script_id()

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            update_data = {}
            if "name" in data:
                update_data["name"] = data["name"]
            if "description" in data:
                update_data["description"] = data["description"]
            if "content" in data:
                update_data["content"] = data["content"]
                # Recalculate metadata
                language = data.get("language", "other")
                metadata = calculate_script_metadata(data["content"], language)
                update_data["metadata"] = metadata
            if "language" in data:
                update_data["language"] = data["language"]
            if "category" in data:
                update_data["category"] = data["category"]
            if "tags" in data:
                update_data["tags"] = data["tags"]

            import asyncio
            asyncio.run(back4app_service.update_script(script_id, update_data))
            updated = asyncio.run(back4app_service.get_script(script_id))

            response = {
                "objectId": updated["objectId"],
                "name": updated["name"],
                "description": updated.get("description"),
                "language": updated["language"],
                "content": updated["content"],
                "version": updated.get("version", "1.0.0"),
                "category": updated.get("category", "other"),
                "tags": updated.get("tags", []),
                "created_by": updated.get("createdBy", "AI"),
                "createdAt": updated["createdAt"],
                "updatedAt": updated["updatedAt"],
                "isLatest": updated.get("isLatest", True),
                "metadata": updated.get("metadata")
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_DELETE(self):
        """Delete script"""
        try:
            script_id = self._get_script_id()

            import asyncio
            asyncio.run(back4app_service.delete_script(script_id))

            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
