# Documentation: repo_book_gen.py

## File Metadata
- **Path**: `repo_book_gen.py`
- **Filename**: `repo_book_gen.py`
- **Extension**: `.py`
- **Language**: python
- **Size**: 28380 bytes
- **Lines**: 786

## Original Source

```python
#!/usr/bin/env python3
"""
World's Best Repo Book Generator and Index Builder
Comprehensive documentation generator for GitHub repositories.
"""

import os
import sys
import json
import hashlib
import mimetypes
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set
from collections import defaultdict

class RepoBookGenerator:
    """Main documentation generator class."""

    def __init__(self, repo_path: str, output_dir: str = "./docs"):
        self.repo_path = Path(repo_path).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.manifest = {
            "repo_source": str(self.repo_path),
            "repo_fingerprint": "",
            "file_count": 0,
            "docs_count": 0,
            "bytes_written": 0,
            "timestamp_start": datetime.now().isoformat(),
            "timestamp_end": "",
            "generator_version": "1.0.0"
        }
        self.files_scanned = []
        self.docs_created = []
        self.errors = []
        self.skipped_files = []
        self.binary_files = []
        self.keywords_global = defaultdict(list)
        self.checksums = {}

    def compute_repo_fingerprint(self) -> str:
        """Compute a fingerprint for the repository."""
        try:
            # Try to get git commit SHA
            git_dir = self.repo_path / ".git"
            if git_dir.exists():
                head_file = git_dir / "HEAD"
                if head_file.exists():
                    with open(head_file, 'r') as f:
                        ref = f.read().strip()
                    if ref.startswith('ref:'):
                        ref_path = git_dir / ref[5:]
                        if ref_path.exists():
                            with open(ref_path, 'r') as f:
                                return f.read().strip()
        except Exception as e:
            self.errors.append(f"Error getting git SHA: {e}")

        # Fallback: hash file list
        file_list = sorted([str(f.relative_to(self.repo_path)) for f in self.scan_files()])
        file_str = "\n".join(file_list)
        return hashlib.sha256(file_str.encode()).hexdigest()

    def scan_files(self) -> List[Path]:
        """Recursively scan all files in the repository."""
        files = []
        ignore_patterns = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv'}

        for root, dirs, filenames in os.walk(self.repo_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]

            for filename in filenames:
                file_path = Path(root) / filename
                files.append(file_path)

        return sorted(files)

    def is_binary(self, file_path: Path) -> bool:
        """Check if a file is binary."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
            return b'\0' in chunk
        except Exception:
            return True

    def classify_file(self, file_path: Path) -> str:
        """Classify file as text, binary, or large."""
        try:
            size = file_path.stat().st_size
            if size > 100 * 1024 * 1024:  # 100MB
                return "large_blob"
            if self.is_binary(file_path):
                return "binary"
            return "text"
        except Exception as e:
            self.errors.append(f"Error classifying {file_path}: {e}")
            return "unknown"

    def read_file_safe(self, file_path: Path) -> Tuple[str, bool]:
        """Safely read file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, True
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                return content, True
            except Exception as e:
                self.errors.append(f"Error reading {file_path}: {e}")
                return "", False
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return "", False

    def extract_keywords(self, content: str, file_path: Path) -> List[str]:
        """Extract keywords from file content."""
        keywords = set()

        # Extract identifiers (functions, classes, variables)
        # Python patterns
        keywords.update(re.findall(r'def\s+(\w+)', content))
        keywords.update(re.findall(r'class\s+(\w+)', content))
        keywords.update(re.findall(r'import\s+(\w+)', content))
        keywords.update(re.findall(r'from\s+(\w+)', content))

        # JavaScript/TypeScript patterns
        keywords.update(re.findall(r'function\s+(\w+)', content))
        keywords.update(re.findall(r'const\s+(\w+)', content))
        keywords.update(re.findall(r'let\s+(\w+)', content))
        keywords.update(re.findall(r'var\s+(\w+)', content))

        # Rust patterns
        keywords.update(re.findall(r'fn\s+(\w+)', content))
        keywords.update(re.findall(r'struct\s+(\w+)', content))
        keywords.update(re.findall(r'enum\s+(\w+)', content))
        keywords.update(re.findall(r'trait\s+(\w+)', content))

        # General camelCase and snake_case identifiers
        keywords.update(re.findall(r'\b[a-z_][a-z0-9_]{2,}\b', content.lower()))

        # Remove common words
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        keywords = {kw for kw in keywords if kw not in common_words and len(kw) > 2}

        return sorted(list(keywords))[:5000]  # Limit to 5000 keywords

    def generate_file_docs(self, file_path: Path, content: str) -> str:
        """Generate comprehensive documentation for a single file."""
        rel_path = file_path.relative_to(self.repo_path)
        filename = file_path.name

        # Detect file type and language
        ext = file_path.suffix
        lang_map = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.rs': 'rust', '.go': 'go', '.java': 'java', '.cpp': 'cpp',
            '.c': 'c', '.md': 'markdown', '.json': 'json', '.yaml': 'yaml',
            '.yml': 'yaml', '.toml': 'toml', '.sh': 'bash', '.ipynb': 'json'
        }
        lang = lang_map.get(ext, 'text')

        # Truncate content if needed
        truncated_content = content if len(content) < 500000 else content[:500000] + "\n... (truncated)"

        # Get generated sections
        overview = self.generate_overview(content, file_path)
        walkthrough = self.generate_walkthrough(content, file_path)
        usage = self.generate_usage_examples(content, file_path)
        perf_sec = self.generate_performance_security_notes(content, file_path)
        related = self.generate_related_files(file_path)
        test_info = self.generate_test_info(content, file_path)

        # Build documentation
        doc = f"""# Documentation: {filename}

## File Metadata
- **Path**: `{rel_path}`
- **Filename**: `{filename}`
- **Extension**: `{ext}`
- **Language**: {lang}
- **Size**: {len(content)} bytes
- **Lines**: {len(content.splitlines())}

## Original Source

```{lang}
{truncated_content}
```

## High-Level Overview

{overview}

## Detailed Walkthrough

{walkthrough}

## Usage Examples

{usage}

## Performance & Security Notes

{perf_sec}

## Related Files

{related}

## Tests & How to Run

{test_info}

---
*Generated by World's Best Repo Book Generator v1.0.0*
"""
        return doc

    def generate_overview(self, content: str, file_path: Path) -> str:
        """Generate high-level overview."""
        lines = content.splitlines()
        ext = file_path.suffix

        if ext == '.py':
            # Look for module docstring
            if len(lines) > 0 and ('"""' in lines[0] or "'''" in lines[0]):
                docstring_lines = []
                in_docstring = False
                for line in lines[:50]:
                    if '"""' in line or "'''" in line:
                        if in_docstring:
                            break
                        in_docstring = True
                    if in_docstring:
                        docstring_lines.append(line)
                if docstring_lines:
                    return "\n".join(docstring_lines)

            # Count functions and classes
            func_count = len(re.findall(r'def\s+\w+', content))
            class_count = len(re.findall(r'class\s+\w+', content))
            import_count = len(re.findall(r'^\s*(?:import|from)\s+', content, re.MULTILINE))

            return f"""This Python file contains:
- {class_count} class(es)
- {func_count} function(s)
- {import_count} import statement(s)

The file appears to be a {"module" if func_count > 3 else "script"} with {"object-oriented" if class_count > 0 else "procedural"} code."""

        elif ext in ['.md', '.txt']:
            # Return first few lines
            return "\n".join(lines[:10])

        elif ext == '.ipynb':
            return "This is a Jupyter notebook containing interactive code cells and markdown documentation."

        else:
            return f"This is a {ext[1:] if ext else 'text'} file with {len(lines)} lines."

    def generate_walkthrough(self, content: str, file_path: Path) -> str:
        """Generate detailed walkthrough."""
        ext = file_path.suffix

        if ext == '.py':
            walkthrough = []

            # Extract classes
            classes = re.findall(r'class\s+(\w+)[^:]*:', content)
            if classes:
                walkthrough.append("### Classes\n")
                for cls in classes[:20]:  # Limit to 20
                    walkthrough.append(f"- **{cls}**")

            # Extract functions
            functions = re.findall(r'def\s+(\w+)\s*\([^)]*\)', content)
            if functions:
                walkthrough.append("\n### Functions\n")
                for func in functions[:50]:  # Limit to 50
                    walkthrough.append(f"- `{func}`")

            return "\n".join(walkthrough) if walkthrough else "No significant structure detected."

        return "Detailed walkthrough not available for this file type."

    def generate_usage_examples(self, content: str, file_path: Path) -> str:
        """Generate usage examples."""
        ext = file_path.suffix

        if ext == '.py':
            # Look for main block
            if 'if __name__ == "__main__":' in content:
                return "This file contains a main execution block and can be run directly as a script."

        return "Usage examples not available. Refer to the source code above."

    def generate_performance_security_notes(self, content: str, file_path: Path) -> str:
        """Generate performance and security notes."""
        notes = []

        # Check for common security issues
        if 'eval(' in content:
            notes.append("⚠️ **Security**: File uses `eval()` which can be dangerous with untrusted input.")
        if 'exec(' in content:
            notes.append("⚠️ **Security**: File uses `exec()` which can be dangerous with untrusted input.")
        if re.search(r'password\s*=\s*["\']', content, re.IGNORECASE):
            notes.append("⚠️ **Security**: Potential hardcoded password detected.")
        if re.search(r'api[_-]?key\s*=\s*["\']', content, re.IGNORECASE):
            notes.append("⚠️ **Security**: Potential hardcoded API key detected.")

        # Performance notes
        if 'import multiprocessing' in content or 'import threading' in content:
            notes.append("📊 **Performance**: File uses parallel processing.")

        if not notes:
            return "No specific performance or security concerns detected. Always review code for your specific use case."

        return "\n".join(notes)

    def generate_related_files(self, file_path: Path) -> str:
        """Generate related files section."""
        # This would need actual analysis, for now return placeholder
        return "Related files will be determined through import analysis."

    def generate_test_info(self, content: str, file_path: Path) -> str:
        """Generate test information."""
        if 'test_' in file_path.name or file_path.name.startswith('test'):
            return "This appears to be a test file. Run with your testing framework (pytest, unittest, etc.)."

        if 'import pytest' in content or 'import unittest' in content:
            return "This file contains tests. Run with the appropriate testing framework."

        return "No test information available."

    def generate_file_keywords(self, file_path: Path, keywords: List[str]) -> str:
        """Generate keyword index for a file."""
        rel_path = file_path.relative_to(self.repo_path)

        kw_doc = f"""# Keywords: {file_path.name}

## Extracted Keywords

Total keywords extracted: {len(keywords)}

"""

        # Group keywords alphabetically
        grouped = defaultdict(list)
        for kw in keywords:
            if kw:
                first_letter = kw[0].upper()
                grouped[first_letter].append(kw)

        for letter in sorted(grouped.keys()):
            kw_doc += f"\n### {letter}\n\n"
            for kw in sorted(grouped[letter]):
                kw_doc += f"- **{kw}**: Identifier found in `{rel_path}`\n"

        return kw_doc

    def generate_folder_index(self, folder_path: Path) -> str:
        """Generate index.md for a folder."""
        rel_path = folder_path.relative_to(self.repo_path) if folder_path != self.repo_path else Path(".")

        index = f"""# Index: {rel_path}

## Contents

"""

        # List subdirectories
        subdirs = sorted([d for d in folder_path.iterdir() if d.is_dir() and not d.name.startswith('.')])
        if subdirs:
            index += "### Subdirectories\n\n"
            for subdir in subdirs:
                index += f"- [{subdir.name}/](./{subdir.name}/index.md)\n"

        # List files
        files = sorted([f for f in folder_path.iterdir() if f.is_file() and not f.name.startswith('.')])
        if files:
            index += "\n### Files\n\n"
            for file in files:
                doc_name = f"{file.name}_docs.md"
                index += f"- [{file.name}](./{doc_name})\n"

        return index

    def generate_folder_doc(self, folder_path: Path) -> str:
        """Generate doc.md for a folder."""
        rel_path = folder_path.relative_to(self.repo_path) if folder_path != self.repo_path else Path(".")

        # Count contents
        files = [f for f in folder_path.iterdir() if f.is_file() and not f.name.startswith('.')]
        dirs = [d for d in folder_path.iterdir() if d.is_dir() and not d.name.startswith('.')]

        doc = f"""# Documentation: {rel_path}

## Folder Overview

**Path**: `{rel_path}`
**Files**: {len(files)}
**Subdirectories**: {len(dirs)}

## Purpose

This folder {"is the root directory of the repository" if folder_path == self.repo_path else f"is located at `{rel_path}`"}.

## Contents Summary

"""

        if dirs:
            doc += "### Subdirectories:\n"
            for d in sorted(dirs):
                doc += f"- `{d.name}/`\n"

        if files:
            doc += "\n### Files:\n"
            for f in sorted(files):
                doc += f"- `{f.name}` ({f.stat().st_size} bytes)\n"

        return doc

    def generate_folder_sub(self, folder_path: Path) -> str:
        """Generate sub.md for a folder (merged keywords)."""
        return "# Merged Keywords\n\nKeywords from all files in this folder and subfolders.\n"

    def process_file(self, file_path: Path):
        """Process a single file."""
        try:
            rel_path = file_path.relative_to(self.repo_path)
            file_class = self.classify_file(file_path)

            # Create output directory
            out_dir = self.output_dir / rel_path.parent
            out_dir.mkdir(parents=True, exist_ok=True)

            if file_class == "binary":
                self.binary_files.append(str(rel_path))
                # Create minimal doc for binary
                doc_content = f"""# Binary File: {file_path.name}

- **Path**: `{rel_path}`
- **Size**: {file_path.stat().st_size} bytes
- **Type**: Binary file (not readable as text)
- **MIME**: {mimetypes.guess_type(file_path)[0] or 'unknown'}

This file is binary and cannot be documented as text.
"""
                doc_path = out_dir / f"{file_path.name}_docs.md"
                with open(doc_path, 'w') as f:
                    f.write(doc_content)
                self.docs_created.append(str(doc_path.relative_to(self.output_dir)))
                self.manifest['bytes_written'] += len(doc_content)
                return

            elif file_class == "large_blob":
                self.skipped_files.append(f"{rel_path} (too large)")
                return

            # Read and process text file
            content, success = self.read_file_safe(file_path)
            if not success:
                self.skipped_files.append(f"{rel_path} (read error)")
                return

            self.files_scanned.append(str(rel_path))

            # Generate docs
            doc_content = self.generate_file_docs(file_path, content)
            doc_path = out_dir / f"{file_path.name}_docs.md"
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            self.docs_created.append(str(doc_path.relative_to(self.output_dir)))
            self.manifest['bytes_written'] += len(doc_content)

            # Generate keywords
            keywords = self.extract_keywords(content, file_path)
            kw_content = self.generate_file_keywords(file_path, keywords)
            kw_path = out_dir / f"{file_path.name}_kw.md"
            with open(kw_path, 'w', encoding='utf-8') as f:
                f.write(kw_content)
            self.docs_created.append(str(kw_path.relative_to(self.output_dir)))
            self.manifest['bytes_written'] += len(kw_content)

            # Add to global keywords
            for kw in keywords:
                self.keywords_global[kw].append(str(rel_path))

        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {e}")

    def process_folders(self):
        """Process all folders to create indexes."""
        for root, dirs, _ in os.walk(self.repo_path):
            root_path = Path(root)
            if '.git' in root_path.parts:
                continue

            rel_path = root_path.relative_to(self.repo_path) if root_path != self.repo_path else Path(".")
            out_dir = self.output_dir / rel_path
            out_dir.mkdir(parents=True, exist_ok=True)

            # Generate folder docs
            index_content = self.generate_folder_index(root_path)
            index_path = out_dir / "index.md"
            with open(index_path, 'w') as f:
                f.write(index_content)
            self.docs_created.append(str(index_path.relative_to(self.output_dir)))

            doc_content = self.generate_folder_doc(root_path)
            doc_path = out_dir / "doc.md"
            with open(doc_path, 'w') as f:
                f.write(doc_content)
            self.docs_created.append(str(doc_path.relative_to(self.output_dir)))

            sub_content = self.generate_folder_sub(root_path)
            sub_path = out_dir / "sub.md"
            with open(sub_path, 'w') as f:
                f.write(sub_content)
            self.docs_created.append(str(sub_path.relative_to(self.output_dir)))

    def generate_global_keyword_index(self):
        """Generate global keywords.md."""
        content = "# Global Keyword Index\n\n"
        content += f"Total unique keywords: {len(self.keywords_global)}\n\n"

        # Group by letter
        grouped = defaultdict(list)
        for kw in sorted(self.keywords_global.keys()):
            if kw:
                first_letter = kw[0].upper()
                grouped[first_letter].append(kw)

        for letter in sorted(grouped.keys()):
            content += f"\n## {letter}\n\n"
            for kw in sorted(grouped[letter]):
                files = self.keywords_global[kw][:10]  # Limit to 10 files per keyword
                content += f"### {kw}\n\n"
                content += "Found in:\n"
                for file in files:
                    content += f"- `{file}`\n"

        kw_path = self.output_dir / "keywords.md"
        with open(kw_path, 'w') as f:
            f.write(content)
        self.docs_created.append("keywords.md")
        self.manifest['bytes_written'] += len(content)

    def generate_global_index(self):
        """Generate global index.md."""
        content = """# Repository Documentation Index

Welcome to the comprehensive documentation for this repository.

## Quick Links

- [Global Keyword Index](./keywords.md)
- [Comprehensive Book](./comprehensive_book.md)
- [Verification Report](./verification_report.md)

## Folder Structure

"""
        # List all folders
        for root, dirs, _ in os.walk(self.output_dir):
            root_path = Path(root)
            if root_path == self.output_dir:
                continue
            rel_path = root_path.relative_to(self.output_dir)
            depth = len(rel_path.parts)
            indent = "  " * (depth - 1)
            content += f"{indent}- [{rel_path.name}/](./{rel_path}/index.md)\n"

        index_path = self.output_dir / "index.md"
        with open(index_path, 'w') as f:
            f.write(content)
        self.docs_created.append("index.md")

    def generate_comprehensive_book(self):
        """Generate comprehensive_book.md."""
        book = """# Comprehensive Repository Book

This is a comprehensive documentation book combining all folder and file documentation.

"""

        # Add root doc
        root_doc_path = self.output_dir / "doc.md"
        if root_doc_path.exists():
            with open(root_doc_path, 'r') as f:
                book += f.read() + "\n\n"

        # Add chapter marker
        book += "\n---\n\n# Detailed Documentation\n\n"
        book += "For detailed file-by-file documentation, please refer to the individual documentation files.\n"

        # Write book
        book_path = self.output_dir / "comprehensive_book.md"
        with open(book_path, 'w') as f:
            f.write(book)
        self.docs_created.append("comprehensive_book.md")

    def generate_verification_report(self):
        """Generate verification report."""
        report = f"""# Verification Report

Generated: {datetime.now().isoformat()}

## Summary

- **Files scanned**: {len(self.files_scanned)}
- **Docs created**: {len(self.docs_created)}
- **Errors**: {len(self.errors)}
- **Skipped files**: {len(self.skipped_files)}
- **Binary files**: {len(self.binary_files)}

## Binary Files

"""
        for bf in self.binary_files:
            report += f"- `{bf}`\n"

        report += "\n## Skipped Files\n\n"
        for sf in self.skipped_files:
            report += f"- `{sf}`\n"

        report += "\n## Errors\n\n"
        if self.errors:
            for err in self.errors:
                report += f"- {err}\n"
        else:
            report += "No errors encountered.\n"

        report_path = self.output_dir / "verification_report.md"
        with open(report_path, 'w') as f:
            f.write(report)
        self.docs_created.append("verification_report.md")

    def generate_readme(self):
        """Generate README for docs."""
        readme = """# Documentation Structure

This documentation was generated by the World's Best Repo Book Generator.

## Organization

- `index.md` - Main index linking to all folders
- `keywords.md` - Global keyword index (A-Z)
- `comprehensive_book.md` - Comprehensive documentation book
- `verification_report.md` - Generation report and errors
- `manifest.json` - Metadata about the generation process

Each folder contains:
- `index.md` - Folder index
- `doc.md` - Folder documentation
- `sub.md` - Merged keywords from subfolders

Each file has:
- `<filename>_docs.md` - Comprehensive file documentation
- `<filename>_kw.md` - File keyword index

## How to Use

1. Start with `index.md` for an overview
2. Navigate through folder indexes
3. Read individual file documentation as needed
4. Use `keywords.md` to search for specific terms

## Regenerating

To regenerate or update documentation:

```bash
python3 repo_book_gen.py --source <repo_path> --out ./docs
```
"""
        readme_path = self.output_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme)
        self.docs_created.append("README.md")

    def save_manifest(self):
        """Save manifest.json."""
        self.manifest['timestamp_end'] = datetime.now().isoformat()
        self.manifest['file_count'] = len(self.files_scanned) + len(self.binary_files)
        self.manifest['docs_count'] = len(self.docs_created)

        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def run(self):
        """Run the complete documentation generation process."""
        print("Starting World's Best Repo Book Generator...")
        print(f"Repository: {self.repo_path}")
        print(f"Output: {self.output_dir}")

        # Step 1: Bootstrap
        print("\n[Step 1/7] Bootstrap...")
        self.manifest['repo_fingerprint'] = self.compute_repo_fingerprint()
        print(f"Fingerprint: {self.manifest['repo_fingerprint'][:16]}...")

        # Step 2: Scan
        print("\n[Step 2/7] Scanning files...")
        files = self.scan_files()
        print(f"Found {len(files)} files")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Step 3: Process files
        print("\n[Step 3/7] Processing files...")
        for i, file_path in enumerate(files, 1):
            if i % 10 == 0:
                print(f"  Processed {i}/{len(files)} files...")
            self.process_file(file_path)
        print(f"  Processed {len(files)} files.")

        # Step 4: Process folders
        print("\n[Step 4/7] Processing folders...")
        self.process_folders()

        # Step 5: Global merges
        print("\n[Step 5/7] Generating global indexes...")
        self.generate_global_keyword_index()
        self.generate_global_index()
        self.generate_comprehensive_book()

        # Step 6: Verification
        print("\n[Step 6/7] Generating verification report...")
        self.generate_verification_report()

        # Step 7: Manifest
        print("\n[Step 7/7] Saving manifest and README...")
        self.generate_readme()
        self.save_manifest()

        # Print summary
        print("\n" + "="*60)
        print("GENERATION COMPLETE")
        print("="*60)
        print(f"Repository: {self.manifest['repo_source']}")
        print(f"Fingerprint: {self.manifest['repo_fingerprint']}")
        print(f"Files scanned: {self.manifest['file_count']}")
        print(f"Docs created: {self.manifest['docs_count']}")
        print(f"Bytes written: {self.manifest['bytes_written']:,}")
        print(f"Errors: {len(self.errors)}")
        print("="*60)

        # Return summary JSON
        return {
            "repo_source": self.manifest['repo_source'],
            "repo_fingerprint": self.manifest['repo_fingerprint'],
            "files_scanned": self.manifest['file_count'],
            "docs_created": self.manifest['docs_count'],
            "words_estimated": self.manifest['bytes_written'] // 5,  # Rough estimate
            "bytes_written": self.manifest['bytes_written'],
            "errors": self.errors
        }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="World's Best Repo Book Generator")
    parser.add_argument('--source', default='.', help='Repository path or URL')
    parser.add_argument('--out', default='./docs', help='Output directory')

    args = parser.parse_args()

    generator = RepoBookGenerator(args.source, args.out)
    result = generator.run()

    print("\nJSON Summary:")
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

```

## High-Level Overview

This Python file contains:
- 1 class(es)
- 28 function(s)
- 11 import statement(s)

The file appears to be a module with object-oriented code.

## Detailed Walkthrough

### Classes

- **RepoBookGenerator**

### Functions

- `__init__`
- `compute_repo_fingerprint`
- `scan_files`
- `is_binary`
- `classify_file`
- `read_file_safe`
- `extract_keywords`
- `generate_file_docs`
- `generate_overview`
- `generate_walkthrough`
- `generate_usage_examples`
- `generate_performance_security_notes`
- `generate_related_files`
- `generate_test_info`
- `generate_file_keywords`
- `generate_folder_index`
- `generate_folder_doc`
- `generate_folder_sub`
- `process_file`
- `process_folders`
- `generate_global_keyword_index`
- `generate_global_index`
- `generate_comprehensive_book`
- `generate_verification_report`
- `generate_readme`
- `save_manifest`
- `run`
- `main`

## Usage Examples

This file contains a main execution block and can be run directly as a script.

## Performance & Security Notes

⚠️ **Security**: File uses `eval()` which can be dangerous with untrusted input.
⚠️ **Security**: File uses `exec()` which can be dangerous with untrusted input.
📊 **Performance**: File uses parallel processing.

## Related Files

Related files will be determined through import analysis.

## Tests & How to Run

This file contains tests. Run with the appropriate testing framework.

---
*Generated by World's Best Repo Book Generator v1.0.0*
