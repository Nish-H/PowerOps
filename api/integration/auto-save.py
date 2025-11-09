"""
Serverless function for /api/integration/auto-save
Critical endpoint for Claude AI auto-save functionality
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from _lib.back4app import back4app_service
from _lib.helpers import calculate_script_metadata, detect_language


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Auto-save a script created by Claude"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Auto-detect language if not provided
            language = data.get("language") or detect_language(
                data.get("name", ""),
                data.get("content", "")
            )

            # Calculate metadata
            metadata = calculate_script_metadata(data.get("content", ""), language)

            # Create script
            script_data = {
                "name": data.get("name"),
                "description": data.get("description") or f"Auto-generated {language} script",
                "language": language,
                "content": data.get("content"),
                "version": "1.0.0",
                "category": data.get("category", "other"),
                "tags": data.get("tags", []) if data.get("tags") else ["auto-generated", "claude"],
                "createdBy": "Claude AI",
                "isLatest": True,
                "metadata": metadata
            }

            import asyncio
            script_result = asyncio.run(back4app_service.create_script(script_data))

            # Create initial version
            version_data = {
                "scriptId": {"__type": "Pointer", "className": "Script", "objectId": script_result["objectId"]},
                "versionNumber": "1.0.0",
                "content": data.get("content"),
                "changelog": "Initial auto-save from Claude AI",
                "createdBy": "Claude AI"
            }
            asyncio.run(back4app_service.create_version(version_data))

            # Create artifacts if provided
            artifacts = []
            for artifact in data.get("artifacts", []):
                artifact_data = {
                    "scriptId": {"__type": "Pointer", "className": "Script", "objectId": script_result["objectId"]},
                    "scriptVersion": "1.0.0",
                    "name": artifact.get("name", "output"),
                    "type": artifact.get("type", "text"),
                    "content": artifact.get("content"),
                    "fileUrl": artifact.get("file_url"),
                    "size": len(artifact.get("content", "")),
                    "metadata": artifact.get("metadata", {})
                }
                artifact_result = asyncio.run(back4app_service.create_artifact(artifact_data))
                artifacts.append({
                    "objectId": artifact_result["objectId"],
                    **artifact_data,
                    "createdAt": artifact_result["createdAt"]
                })

            response = {
                "script": {
                    "objectId": script_result["objectId"],
                    **script_data,
                    "createdAt": script_result["createdAt"],
                    "updatedAt": script_result["updatedAt"]
                },
                "artifacts": artifacts,
                "message": f"Script '{data.get('name')}' auto-saved successfully with {len(artifacts)} artifact(s)"
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
            self.wfile.write(json.dumps({"error": f"Auto-save failed: {str(e)}"}).encode())
