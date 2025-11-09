"""
Serverless function for /api/search
Handles: GET (search scripts)
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from _lib.back4app import back4app_service


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Search scripts"""
        try:
            from urllib.parse import parse_qs, urlparse
            query_params = parse_qs(urlparse(self.path).query)

            query = query_params.get('q', [''])[0]
            limit = int(query_params.get('limit', ['50'])[0])

            if not query:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Query parameter 'q' is required"}).encode())
                return

            import asyncio
            result = asyncio.run(back4app_service.search_scripts(query, limit=limit))

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
                "total": len(scripts),
                "page": 1,
                "page_size": limit
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
