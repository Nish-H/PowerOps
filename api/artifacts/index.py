"""
Serverless function for /api/artifacts
Handles: GET (list artifacts)
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
        """List artifacts"""
        try:
            from urllib.parse import parse_qs, urlparse
            query_params = parse_qs(urlparse(self.path).query)

            script_id = query_params.get('script_id', [None])[0]
            page = int(query_params.get('page', ['1'])[0])
            page_size = int(query_params.get('page_size', ['20'])[0])

            import asyncio
            result = asyncio.run(back4app_service.list_artifacts(script_id=script_id, limit=page_size))

            artifacts = [
                {
                    "objectId": a["objectId"],
                    "scriptId": a["scriptId"]["objectId"] if isinstance(a["scriptId"], dict) else a["scriptId"],
                    "scriptVersion": a.get("scriptVersion", "1.0.0"),
                    "name": a["name"],
                    "type": a["type"],
                    "content": a.get("content"),
                    "file_url": a.get("fileUrl"),
                    "size": a.get("size", 0),
                    "metadata": a.get("metadata"),
                    "createdAt": a["createdAt"]
                }
                for a in result.get("results", [])
            ]

            response = {
                "results": artifacts,
                "count": len(artifacts),
                "total": result.get("count", len(artifacts)),
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
