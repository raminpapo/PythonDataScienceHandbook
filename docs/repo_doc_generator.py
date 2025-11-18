#!/usr/bin/env python3
"""
World's Best Repo Book Generator and Index Builder
Generates comprehensive documentation for the entire repository
"""

import os
import json
import hashlib
import re
import mimetypes
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import subprocess

class RepoBookGenerator:
    def __init__(self, repo_root, docs_root):
        self.repo_root = Path(repo_root)
        self.docs_root = Path(docs_root)
        self.manifest = {
            "generator_version": "1.0.0",
            "repo_name": os.path.basename(repo_root),
            "repo_source": str(repo_root),
            "repo_fingerprint": "",
            "commit_sha": "",
            "files_scanned": 0,
            "docs_created": 0,
            "words_estimated": 0,
            "bytes_written": 0,
            "timestamp_start": datetime.utcnow().isoformat(),
            "timestamp_end": "",
            "file_map": [],
            "checksums": {}
        }
        self.keywords_global = defaultdict(list)
        self.verification_issues = []
        self.progress_log = []

    def get_git_commit(self):
        """Get current git commit SHA"""
        try:
            result = subprocess.run(
                ['git', '-C', str(self.repo_root), 'rev-parse', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except:
            return "no-git"

    def compute_repo_fingerprint(self, file_list):
        """Compute fingerprint from file list"""
        hasher = hashlib.sha256()
        for f in sorted(file_list):
            hasher.update(f.encode())
        return hasher.hexdigest()[:16]

    def classify_file(self, filepath):
        """Classify file as text, binary, or special"""
        path = Path(filepath)

        # Check size
        try:
            size = path.stat().st_size
            if size > 100 * 1024 * 1024:  # 100MB
                return 'very_large', size
        except:
            return 'unreadable', 0

        # Binary extensions
        binary_exts = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.ttf', '.woff', '.eot', '.svg', '.pdf'}
        if path.suffix.lower() in binary_exts:
            return 'binary', size

        # Text extensions
        text_exts = {'.py', '.md', '.txt', '.json', '.yml', '.yaml', '.csv', '.html', '.css', '.less', '.js', '.ipynb'}
        if path.suffix.lower() in text_exts:
            return 'text', size

        # Try to detect by content
        try:
            with open(path, 'rb') as f:
                chunk = f.read(512)
                if b'\x00' in chunk:
                    return 'binary', size
                return 'text', size
        except:
            return 'unreadable', 0

    def extract_keywords_from_text(self, text, max_keywords=1000):
        """Extract keywords from text content"""
        # Remove code blocks for keyword extraction
        text_no_code = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

        # Find Python identifiers, API names, domain words
        keywords = set()

        # Python identifiers and class names
        keywords.update(re.findall(r'\b[A-Za-z_][A-Za-z0-9_]{2,}\b', text_no_code))

        # Remove common words
        common = {'the', 'and', 'for', 'with', 'from', 'import', 'this', 'that', 'will',
                  'have', 'has', 'are', 'was', 'were', 'been', 'being', 'can', 'could',
                  'should', 'would', 'may', 'might', 'must', 'shall', 'you', 'your',
                  'our', 'their', 'his', 'her', 'its', 'them', 'they', 'we', 'us'}
        keywords = {k for k in keywords if k.lower() not in common and len(k) > 2}

        return sorted(keywords)[:max_keywords]

    def read_file_content(self, filepath):
        """Read file content safely"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            self.verification_issues.append(f"Could not read {filepath}: {e}")
            return None

    def sanitize_filename(self, name):
        """Sanitize filename for documentation"""
        return re.sub(r'[^\w\-\.]', '_', name)

    def write_file_docs(self, filepath, rel_path):
        """Generate _docs.md for a file"""
        content = self.read_file_content(filepath)
        if content is None:
            return None, []

        path = Path(filepath)
        filename = path.name
        safe_name = self.sanitize_filename(filename)

        # Prepare doc content
        doc_lines = []
        doc_lines.append(f"# Documentation: {filename}\n")
        doc_lines.append(f"**Path:** `{rel_path}`\n")
        doc_lines.append(f"**Type:** {path.suffix or 'no extension'}\n")
        doc_lines.append(f"**Size:** {len(content)} characters\n")
        doc_lines.append(f"\n---\n")

        doc_lines.append(f"\n## File Metadata\n")
        doc_lines.append(f"- **Full Path:** `{rel_path}`\n")
        doc_lines.append(f"- **File Name:** `{filename}`\n")
        doc_lines.append(f"- **Extension:** `{path.suffix}`\n")
        doc_lines.append(f"- **Size:** {len(content)} bytes\n")
        doc_lines.append(f"- **Last Modified:** {datetime.fromtimestamp(path.stat().st_mtime).isoformat()}\n")

        doc_lines.append(f"\n## Original Source\n")
        doc_lines.append(f"```{path.suffix[1:] if path.suffix else 'text'}\n")
        # Include full content (truncate only if > 2M chars)
        if len(content) > 2000000:
            doc_lines.append(content[:2000000])
            doc_lines.append(f"\n... [TRUNCATED - showing first 2,000,000 of {len(content)} characters]\n")
        else:
            doc_lines.append(content)
        doc_lines.append(f"\n```\n")

        doc_lines.append(f"\n## High-Level Overview\n")

        # Analyze based on file type
        if path.suffix == '.py':
            doc_lines.append(self.analyze_python_file(content, filename))
        elif path.suffix == '.ipynb':
            doc_lines.append(self.analyze_notebook_file(content, filename))
        elif path.suffix == '.md':
            doc_lines.append(self.analyze_markdown_file(content, filename))
        elif path.suffix in ['.csv', '.txt']:
            doc_lines.append(self.analyze_data_file(content, filename))
        elif path.suffix in ['.html', '.css', '.less']:
            doc_lines.append(self.analyze_web_file(content, filename))
        elif path.suffix in ['.yml', '.yaml']:
            doc_lines.append(self.analyze_config_file(content, filename))
        else:
            doc_lines.append(f"This is a {path.suffix} file containing {len(content)} characters.\n")

        doc_lines.append(f"\n## Detailed Analysis\n")
        doc_lines.append(self.detailed_analysis(content, path.suffix, filename))

        doc_lines.append(f"\n## Usage and Integration\n")
        doc_lines.append(f"This file is part of the {self.manifest['repo_name']} repository.\n")
        doc_lines.append(f"Located at: `{rel_path}`\n")

        doc_lines.append(f"\n## Performance and Security Notes\n")
        doc_lines.append(f"- File size: {len(content)} bytes\n")
        doc_lines.append(f"- Consider security implications when using or modifying this file\n")

        doc_text = ''.join(doc_lines)

        # Extract keywords
        keywords = self.extract_keywords_from_text(doc_text)

        return doc_text, keywords

    def analyze_python_file(self, content, filename):
        """Analyze Python file"""
        lines = []
        lines.append(f"This Python file (`{filename}`) contains Python source code.\n\n")

        # Find imports
        imports = re.findall(r'^(?:from|import)\s+[\w\.]+', content, re.MULTILINE)
        if imports:
            lines.append("**Imports:**\n")
            for imp in imports[:20]:
                lines.append(f"- `{imp}`\n")
            if len(imports) > 20:
                lines.append(f"- ... and {len(imports) - 20} more\n")
            lines.append("\n")

        # Find class definitions
        classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        if classes:
            lines.append(f"**Classes Defined:** {', '.join(classes)}\n\n")

        # Find function definitions
        functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
        if functions:
            lines.append(f"**Functions Defined:** {', '.join(functions[:30])}\n")
            if len(functions) > 30:
                lines.append(f"... and {len(functions) - 30} more\n")
            lines.append("\n")

        return ''.join(lines)

    def analyze_notebook_file(self, content, filename):
        """Analyze Jupyter notebook file"""
        lines = []
        lines.append(f"This is a Jupyter Notebook file (`{filename}`).\n\n")

        try:
            nb = json.loads(content)
            cells = nb.get('cells', [])
            code_cells = [c for c in cells if c.get('cell_type') == 'code']
            markdown_cells = [c for c in cells if c.get('cell_type') == 'markdown']

            lines.append(f"**Notebook Statistics:**\n")
            lines.append(f"- Total cells: {len(cells)}\n")
            lines.append(f"- Code cells: {len(code_cells)}\n")
            lines.append(f"- Markdown cells: {len(markdown_cells)}\n")
            lines.append(f"\n")

            # Extract title from first markdown cell
            if markdown_cells:
                first_md = ''.join(markdown_cells[0].get('source', []))
                title_match = re.search(r'^#\s+(.+)$', first_md, re.MULTILINE)
                if title_match:
                    lines.append(f"**Title:** {title_match.group(1)}\n\n")

        except Exception as e:
            lines.append(f"Could not parse notebook structure: {e}\n\n")

        return ''.join(lines)

    def analyze_markdown_file(self, content, filename):
        """Analyze Markdown file"""
        lines = []
        lines.append(f"This is a Markdown documentation file (`{filename}`).\n\n")

        # Find headers
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        if headers:
            lines.append("**Document Structure:**\n")
            for level, title in headers[:15]:
                indent = "  " * (len(level) - 1)
                lines.append(f"{indent}- {title}\n")
            if len(headers) > 15:
                lines.append(f"... and {len(headers) - 15} more sections\n")
            lines.append("\n")

        return ''.join(lines)

    def analyze_data_file(self, content, filename):
        """Analyze data file (CSV, TXT)"""
        lines = []
        lines.append(f"This is a data file (`{filename}`).\n\n")

        content_lines = content.split('\n')
        lines.append(f"**Data Statistics:**\n")
        lines.append(f"- Total lines: {len(content_lines)}\n")

        if filename.endswith('.csv'):
            if content_lines:
                headers = content_lines[0].split(',')
                lines.append(f"- Columns: {len(headers)}\n")
                lines.append(f"- Column names: {', '.join(headers[:10])}\n")
                if len(headers) > 10:
                    lines.append(f"  ... and {len(headers) - 10} more\n")

        lines.append("\n")
        return ''.join(lines)

    def analyze_web_file(self, content, filename):
        """Analyze web file (HTML, CSS, etc.)"""
        lines = []
        lines.append(f"This is a web asset file (`{filename}`).\n\n")

        if filename.endswith('.html'):
            # Find title
            title_match = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
            if title_match:
                lines.append(f"**Page Title:** {title_match.group(1)}\n\n")

        lines.append(f"Content length: {len(content)} characters\n\n")
        return ''.join(lines)

    def analyze_config_file(self, content, filename):
        """Analyze configuration file"""
        lines = []
        lines.append(f"This is a configuration file (`{filename}`).\n\n")
        lines.append(f"Contains configuration settings for the project.\n\n")
        return ''.join(lines)

    def detailed_analysis(self, content, ext, filename):
        """Provide detailed analysis of file content"""
        lines = []

        word_count = len(content.split())
        line_count = len(content.split('\n'))

        lines.append(f"**Content Metrics:**\n")
        lines.append(f"- Characters: {len(content)}\n")
        lines.append(f"- Words: {word_count}\n")
        lines.append(f"- Lines: {line_count}\n")
        lines.append(f"\n")

        return ''.join(lines)

    def write_file_keywords(self, keywords, filename, rel_path):
        """Generate _kw.md for a file"""
        lines = []
        lines.append(f"# Keywords: {filename}\n\n")
        lines.append(f"**Source:** `{rel_path}`\n\n")
        lines.append(f"**Total Keywords:** {len(keywords)}\n\n")

        # Group by first letter
        by_letter = defaultdict(list)
        for kw in keywords:
            letter = kw[0].upper() if kw else 'Other'
            by_letter[letter].append(kw)

        for letter in sorted(by_letter.keys()):
            lines.append(f"## {letter}\n\n")
            for kw in sorted(by_letter[letter]):
                anchor = re.sub(r'[^\w\-]', '-', kw.lower())
                lines.append(f"- **{kw}** - Found in `{rel_path}`\n")

        return ''.join(lines)

    def write_binary_file_docs(self, filepath, rel_path):
        """Generate documentation for binary files"""
        path = Path(filepath)
        filename = path.name

        try:
            size = path.stat().st_size
        except:
            size = 0

        mime_type, _ = mimetypes.guess_type(str(path))

        lines = []
        lines.append(f"# Binary File: {filename}\n\n")
        lines.append(f"**Path:** `{rel_path}`\n")
        lines.append(f"**Type:** Binary ({mime_type or 'unknown'})\n")
        lines.append(f"**Size:** {size} bytes\n")
        lines.append(f"\n---\n\n")
        lines.append(f"## File Information\n\n")
        lines.append(f"This is a binary file that cannot be displayed as text.\n\n")
        lines.append(f"- **File Name:** `{filename}`\n")
        lines.append(f"- **Full Path:** `{rel_path}`\n")
        lines.append(f"- **MIME Type:** {mime_type or 'unknown'}\n")
        lines.append(f"- **File Size:** {size:,} bytes ({size / 1024:.2f} KB)\n")

        if path.suffix in ['.png', '.jpg', '.jpeg', '.gif']:
            lines.append(f"\n## Description\n\nThis is an image file used in the repository.\n")
        elif path.suffix in ['.ttf', '.woff', '.eot']:
            lines.append(f"\n## Description\n\nThis is a font file used for web typography.\n")
        elif path.suffix == '.ico':
            lines.append(f"\n## Description\n\nThis is a favicon icon file.\n")

        lines.append(f"\n## Handling Instructions\n\n")
        lines.append(f"Binary files should be handled by appropriate tools:\n")
        lines.append(f"- Images: Use image viewers or editors\n")
        lines.append(f"- Fonts: Use font management tools\n")
        lines.append(f"- Other binaries: Use specialized tools for the file type\n")

        return ''.join(lines), []

print("RepoBookGenerator class loaded successfully!")
