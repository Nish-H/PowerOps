"""
Utility helper functions for serverless functions
"""

import re
from typing import Optional, Dict, Any


def detect_language(filename: str, content: str) -> str:
    """Detect programming language from filename and content"""
    extension_map = {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.sh': 'bash', '.bash': 'bash', '.ps1': 'powershell',
        '.rb': 'ruby', '.go': 'go', '.rs': 'rust',
        '.java': 'java', '.cpp': 'cpp', '.c': 'c'
    }

    for ext, lang in extension_map.items():
        if filename.lower().endswith(ext):
            return lang

    if content.startswith('#!/'):
        first_line = content.split('\n')[0].lower()
        if 'python' in first_line:
            return 'python'
        elif 'bash' in first_line or 'sh' in first_line:
            return 'bash'

    return 'other'


def calculate_script_metadata(content: str, language: str) -> Dict[str, Any]:
    """Calculate metadata for a script"""
    try:
        lines = content.split('\n')
        num_lines = len(lines)
        size = len(content.encode('utf-8'))
        complexity = calculate_complexity(content, language)
        dependencies = extract_dependencies(content, language)

        return {
            "size": size,
            "lines": num_lines,
            "complexity": complexity,
            "dependencies": dependencies
        }
    except Exception:
        return {"size": 0, "lines": 0, "complexity": 1, "dependencies": []}


def calculate_complexity(content: str, language: str) -> int:
    """Calculate approximate cyclomatic complexity"""
    decision_keywords = ['if', 'else', 'elif', 'while', 'for', 'switch', 'case', 'catch', 'except', 'and', 'or', '&&', '||', '?']
    complexity = 1
    content_lower = content.lower()

    for keyword in decision_keywords:
        complexity += content_lower.count(keyword)

    if complexity <= 10:
        return complexity
    elif complexity <= 50:
        return min(10, 5 + (complexity - 10) // 10)
    else:
        return 10


def extract_dependencies(content: str, language: str) -> list:
    """Extract dependencies from script content"""
    dependencies = []

    if language == 'python':
        import_patterns = [
            r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)

    elif language in ['javascript', 'typescript']:
        import_patterns = [
            r'require\([\'"]([^\'\"]+)[\'"]\)',
            r'import\s+.*\s+from\s+[\'"]([^\'\"]+)[\'"]'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)

    return list(set(dependencies))


def format_response(data: Any, status: int = 200) -> Dict[str, Any]:
    """Format response for Vercel serverless function"""
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": data
    }


def format_error(message: str, status: int = 500) -> Dict[str, Any]:
    """Format error response"""
    return format_response({"error": message}, status)
