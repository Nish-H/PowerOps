"""
Serverless function for /api/scripts
Handles: GET (list scripts), POST (create script)
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from _lib.back4app import back4app_service
from _lib.helpers import calculate_script_metadata


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """List scripts with optional filters"""
        try:
            # Parse query parameters
            from urllib.parse import parse_qs, urlparse
            query_params = parse_qs(urlparse(self.path).query)

            page = int(query_params.get('page', ['1'])[0])
            page_size = int(query_params.get('page_size', ['20'])[0])
            language = query_params.get('language', [None])[0]
            category = query_params.get('category', [None])[0]
            tag = query_params.get('tag', [None])[0]

            skip = (page - 1) * page_size
            where = {}
            if language:
                where["language"] = language
            if category:
                where["category"] = category
            if tag:
                where["tags"] = tag

            # Use sync version for serverless
            import asyncio
            result = asyncio.run(back4app_service.list_scripts(
                skip=skip,
                limit=page_size,
                where=where if where else None
            ))

            scripts = [
                {
                    "objectId": s["objectId"],
                    "name": s["name"],
                    "description": s.get("description"),
                    "language": s["language"],
                    "content": s["content"],
                    "version": s.get("version", "1.0.0"),
                    "category": s.get("category", "other"),
                    "tags": s.get("tags", []),
                    "created_by": s.get("createdBy", "AI"),
                    "createdAt": s["createdAt"],
                    "updatedAt": s["updatedAt"],
                    "isLatest": s.get("isLatest", True),
                    "metadata": s.get("metadata")
                }
                for s in result.get("results", [])
            ]

            response = {
                "results": scripts,
                "count": len(scripts),
                "total": result.get("count", len(scripts)),
                "page": page,
                "page_size": page_size
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

    def do_POST(self):
        """Create a new script"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Calculate metadata
            metadata = calculate_script_metadata(
                data.get("content", ""),
                data.get("language", "other")
            )

            # Prepare script data
            script_data = {
                "name": data.get("name"),
                "description": data.get("description"),
                "language": data.get("language"),
                "content": data.get("content"),
                "version": data.get("version", "1.0.0"),
                "category": data.get("category", "other"),
                "tags": data.get("tags", []),
                "createdBy": data.get("created_by", "AI"),
                "isLatest": True,
                "metadata": metadata
            }

            # Create in Back4app
            import asyncio
            result = asyncio.run(back4app_service.create_script(script_data))

            # Create initial version
            version_data = {
                "scriptId": {"__type": "Pointer", "className": "Script", "objectId": result["objectId"]},
                "versionNumber": script_data["version"],
                "content": script_data["content"],
                "changelog": "Initial version",
                "createdBy": script_data["createdBy"]
            }
            asyncio.run(back4app_service.create_version(version_data))

            response = {
                "objectId": result["objectId"],
                **script_data,
                "createdAt": result["createdAt"],
                "updatedAt": result["updatedAt"]
            }

            self.send_response(201)
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
