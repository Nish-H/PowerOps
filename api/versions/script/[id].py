"""
Serverless function for /api/versions/script/[id]
Handles: GET (list versions for a script)
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from _lib.back4app import back4app_service


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _get_script_id(self):
        """Extract script ID from path"""
        parts = self.path.split('/')
        return parts[-1].split('?')[0]

    def do_GET(self):
        """List versions for a script"""
        try:
            script_id = self._get_script_id()

            import asyncio
            result = asyncio.run(back4app_service.get_versions(script_id))

            versions = [
                {
                    "objectId": v["objectId"],
                    "scriptId": script_id,
                    "versionNumber": v["versionNumber"],
                    "content": v["content"],
                    "changelog": v.get("changelog"),
                    "createdBy": v.get("createdBy", "AI"),
                    "createdAt": v["createdAt"],
                    "hash": v.get("hash", "")
                }
                for v in result.get("results", [])
            ]

            response = {
                "results": versions,
                "count": len(versions),
                "script_id": script_id
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
