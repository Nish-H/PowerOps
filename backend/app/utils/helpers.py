"""
Utility helper functions
"""

import re
from typing import Optional
from app.models.script import ScriptMetadata


def detect_language(filename: str, content: str) -> str:
    """
    Detect programming language from filename and content.

    Args:
        filename: Name of the script file
        content: Script content

    Returns:
        Detected language as string
    """
    # Check file extension
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.sh': 'bash',
        '.bash': 'bash',
        '.ps1': 'powershell',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.php': 'php',
        '.pl': 'perl',
        '.r': 'r',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala'
    }

    for ext, lang in extension_map.items():
        if filename.lower().endswith(ext):
            return lang

    # Check shebang
    if content.startswith('#!/'):
        first_line = content.split('\n')[0].lower()
        if 'python' in first_line:
            return 'python'
        elif 'bash' in first_line or 'sh' in first_line:
            return 'bash'
        elif 'ruby' in first_line:
            return 'ruby'
        elif 'node' in first_line:
            return 'javascript'

    # Check content patterns
    if 'import ' in content or 'def ' in content or 'class ' in content:
        if 'import ' in content and ('from ' in content or 'as ' in content):
            return 'python'

    if 'function ' in content or 'const ' in content or 'let ' in content:
        if '=>' in content or 'console.log' in content:
            return 'javascript'

    if 'package ' in content and 'func ' in content:
        return 'go'

    if 'fn ' in content and 'let mut' in content:
        return 'rust'

    # Default
    return 'other'


def calculate_script_metadata(content: str, language: str) -> Optional[ScriptMetadata]:
    """
    Calculate metadata for a script.

    Args:
        content: Script content
        language: Programming language

    Returns:
        ScriptMetadata object
    """
    try:
        lines = content.split('\n')
        num_lines = len(lines)
        size = len(content.encode('utf-8'))

        # Calculate basic complexity (cyclomatic complexity approximation)
        complexity = calculate_complexity(content, language)

        # Extract dependencies
        dependencies = extract_dependencies(content, language)

        return ScriptMetadata(
            size=size,
            lines=num_lines,
            complexity=complexity,
            dependencies=dependencies
        )

    except Exception:
        return None


def calculate_complexity(content: str, language: str) -> int:
    """
    Calculate approximate cyclomatic complexity.

    Args:
        content: Script content
        language: Programming language

    Returns:
        Complexity score (1-10)
    """
    # Count decision points
    decision_keywords = [
        'if', 'else', 'elif', 'while', 'for', 'switch', 'case',
        'catch', 'except', 'and', 'or', '&&', '||', '?'
    ]

    complexity = 1  # Base complexity
    content_lower = content.lower()

    for keyword in decision_keywords:
        complexity += content_lower.count(keyword)

    # Normalize to 1-10 scale
    if complexity <= 10:
        return complexity
    elif complexity <= 50:
        return min(10, 5 + (complexity - 10) // 10)
    else:
        return 10


def extract_dependencies(content: str, language: str) -> list:
    """
    Extract dependencies from script content.

    Args:
        content: Script content
        language: Programming language

    Returns:
        List of dependencies
    """
    dependencies = []

    if language == 'python':
        # Match import statements
        import_patterns = [
            r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)

    elif language in ['javascript', 'typescript']:
        # Match require and import statements
        import_patterns = [
            r'require\([\'"]([^\'\"]+)[\'"]\)',
            r'import\s+.*\s+from\s+[\'"]([^\'\"]+)[\'"]'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)

    elif language == 'go':
        # Match import statements
        import_pattern = r'import\s+\"([^\"]+)\"'
        matches = re.findall(import_pattern, content)
        dependencies.extend(matches)

    elif language == 'rust':
        # Match use statements
        use_pattern = r'use\s+([a-zA-Z_][a-zA-Z0-9_:]*)'
        matches = re.findall(use_pattern, content)
        dependencies.extend(matches)

    # Remove duplicates and return
    return list(set(dependencies))


def format_size(size: int) -> str:
    """
    Format byte size to human-readable format.

    Args:
        size: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"
