#!/usr/bin/env python3
"""
Main execution script for generating complete repository documentation
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_doc_generator import RepoBookGenerator

def main():
    repo_root = '/home/user/PythonDataScienceHandbook'
    docs_root = '/home/user/PythonDataScienceHandbook/docs'

    print("=" * 80)
    print("WORLD'S BEST REPO BOOK GENERATOR")
    print("=" * 80)
    print()

    generator = RepoBookGenerator(repo_root, docs_root)

    # Step 1: Get git info
    print("[1/7] Getting repository information...")
    generator.manifest['commit_sha'] = generator.get_git_commit()
    print(f"  Commit SHA: {generator.manifest['commit_sha']}")

    # Step 2: Scan all files
    print("\n[2/7] Scanning repository files...")
    all_files = []
    for root, dirs, files in os.walk(repo_root):
        # Skip .git and docs directory
        dirs[:] = [d for d in dirs if d not in ['.git', 'docs']]
        for file in files:
            if not file.startswith('.'):
                filepath = os.path.join(root, file)
                all_files.append(filepath)

    all_files.sort()
    generator.manifest['files_scanned'] = len(all_files)
    generator.manifest['repo_fingerprint'] = generator.compute_repo_fingerprint(all_files)

    print(f"  Found {len(all_files)} files")
    print(f"  Repo fingerprint: {generator.manifest['repo_fingerprint']}")

    # Classify files
    text_files = []
    binary_files = []
    unreadable_files = []

    print("\n  Classifying files...")
    for filepath in all_files:
        file_type, size = generator.classify_file(filepath)
        rel_path = os.path.relpath(filepath, repo_root)

        file_info = {
            'path': rel_path,
            'type': file_type,
            'size': size
        }
        generator.manifest['file_map'].append(file_info)

        if file_type == 'text':
            text_files.append(filepath)
        elif file_type == 'binary':
            binary_files.append(filepath)
        else:
            unreadable_files.append(filepath)

    print(f"    Text files: {len(text_files)}")
    print(f"    Binary files: {len(binary_files)}")
    print(f"    Unreadable/very large: {len(unreadable_files)}")

    # Step 3: Process text files
    print(f"\n[3/7] Processing {len(text_files)} text files...")
    docs_created = 0
    total_words = 0

    for idx, filepath in enumerate(text_files, 1):
        rel_path = os.path.relpath(filepath, repo_root)
        path = Path(filepath)

        # Create doc directory
        doc_dir = Path(docs_root) / path.parent.relative_to(repo_root)
        doc_dir.mkdir(parents=True, exist_ok=True)

        print(f"  [{idx}/{len(text_files)}] {rel_path}")

        # Generate docs
        doc_content, keywords = generator.write_file_docs(filepath, rel_path)

        if doc_content:
            # Write _docs.md
            safe_name = generator.sanitize_filename(path.name)
            docs_file = doc_dir / f"{safe_name}_docs.md"

            with open(docs_file, 'w', encoding='utf-8') as f:
                f.write(doc_content)

            docs_created += 1
            total_words += len(doc_content.split())

            # Compute checksum
            checksum = hashlib.sha256(doc_content.encode()).hexdigest()
            generator.manifest['checksums'][str(docs_file.relative_to(docs_root))] = checksum

            # Write _kw.md
            if keywords:
                kw_content = generator.write_file_keywords(keywords, path.name, rel_path)
                kw_file = doc_dir / f"{safe_name}_kw.md"

                with open(kw_file, 'w', encoding='utf-8') as f:
                    f.write(kw_content)

                docs_created += 1

                # Store keywords globally
                for kw in keywords:
                    generator.keywords_global[kw].append({
                        'file': rel_path,
                        'docs': str(docs_file.relative_to(docs_root))
                    })

            generator.progress_log.append({
                'file': rel_path,
                'status': 'success',
                'docs_created': 2 if keywords else 1
            })

    print(f"  Created {docs_created} documentation files")

    # Step 4: Process binary files
    print(f"\n[4/7] Processing {len(binary_files)} binary files...")

    for idx, filepath in enumerate(binary_files, 1):
        rel_path = os.path.relpath(filepath, repo_root)
        path = Path(filepath)

        # Create doc directory
        doc_dir = Path(docs_root) / path.parent.relative_to(repo_root)
        doc_dir.mkdir(parents=True, exist_ok=True)

        if idx % 10 == 0 or idx == len(binary_files):
            print(f"  [{idx}/{len(binary_files)}] {rel_path}")

        # Generate binary file docs
        doc_content, _ = generator.write_binary_file_docs(filepath, rel_path)

        safe_name = generator.sanitize_filename(path.name)
        docs_file = doc_dir / f"{safe_name}_docs.md"

        with open(docs_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)

        docs_created += 1

        generator.progress_log.append({
            'file': rel_path,
            'status': 'binary',
            'docs_created': 1
        })

    # Step 5: Create folder indices
    print(f"\n[5/7] Creating folder indices and documentation...")

    # Get all unique directories
    all_dirs = set()
    for filepath in all_files:
        rel_path = os.path.relpath(filepath, repo_root)
        parts = Path(rel_path).parts
        for i in range(len(parts)):
            all_dirs.add('/'.join(parts[:i]) if i > 0 else '.')

    all_dirs = sorted(all_dirs)
    print(f"  Processing {len(all_dirs)} directories...")

    folder_docs_created = 0

    for dir_path in all_dirs:
        if dir_path == '.':
            doc_dir = Path(docs_root)
            source_dir = Path(repo_root)
        else:
            doc_dir = Path(docs_root) / dir_path
            source_dir = Path(repo_root) / dir_path

        doc_dir.mkdir(parents=True, exist_ok=True)

        # Create index.md
        index_lines = []
        index_lines.append(f"# Index: {dir_path if dir_path != '.' else 'Root'}\n\n")
        index_lines.append(f"**Path:** `{dir_path}`\n\n")
        index_lines.append(f"## Contents\n\n")

        # List subdirectories
        subdirs = []
        files = []

        for item in sorted(os.listdir(source_dir)):
            item_path = source_dir / item
            if item.startswith('.') or item == 'docs':
                continue

            if item_path.is_dir():
                subdirs.append(item)
            else:
                files.append(item)

        if subdirs:
            index_lines.append(f"### Subdirectories\n\n")
            for subdir in subdirs:
                rel_link = f"{subdir}/index.md"
                index_lines.append(f"- [{subdir}/]({rel_link})\n")
            index_lines.append("\n")

        if files:
            index_lines.append(f"### Files\n\n")
            for file in files:
                safe_name = generator.sanitize_filename(file)
                doc_link = f"{safe_name}_docs.md"
                index_lines.append(f"- [{file}]({doc_link})\n")
            index_lines.append("\n")

        index_content = ''.join(index_lines)
        with open(doc_dir / 'index.md', 'w', encoding='utf-8') as f:
            f.write(index_content)

        folder_docs_created += 1

        # Create doc.md
        doc_lines = []
        doc_lines.append(f"# Folder Documentation: {dir_path if dir_path != '.' else 'Root'}\n\n")
        doc_lines.append(f"**Path:** `{dir_path}`\n\n")
        doc_lines.append(f"## Purpose\n\n")

        # Add context based on folder name
        folder_name = os.path.basename(dir_path) if dir_path != '.' else 'root'

        if folder_name == 'root' or dir_path == '.':
            doc_lines.append("This is the root directory of the Python Data Science Handbook repository.\n\n")
        elif folder_name == 'notebooks':
            doc_lines.append("Contains Jupyter notebooks with data science tutorials and examples.\n\n")
        elif folder_name == 'data':
            doc_lines.append("Contains datasets used in the notebooks.\n\n")
        elif folder_name == 'figures':
            doc_lines.append("Contains images and figures used in the notebooks.\n\n")
        elif folder_name == 'tools':
            doc_lines.append("Contains utility scripts for managing the repository.\n\n")
        elif folder_name == 'website':
            doc_lines.append("Contains website generation files and templates.\n\n")
        else:
            doc_lines.append(f"This folder contains files related to {folder_name}.\n\n")

        doc_lines.append(f"## Contents Summary\n\n")
        doc_lines.append(f"- Subdirectories: {len(subdirs)}\n")
        doc_lines.append(f"- Files: {len(files)}\n")

        doc_content = ''.join(doc_lines)
        with open(doc_dir / 'doc.md', 'w', encoding='utf-8') as f:
            f.write(doc_content)

        folder_docs_created += 1

        # Create sub.md (merged keywords from this folder)
        sub_lines = []
        sub_lines.append(f"# Keywords Index: {dir_path if dir_path != '.' else 'Root'}\n\n")
        sub_lines.append(f"This index contains keywords from all files in this folder and its subfolders.\n\n")

        # Collect keywords from this folder
        folder_keywords = defaultdict(list)
        for kw, refs in generator.keywords_global.items():
            for ref in refs:
                if ref['file'].startswith(dir_path + '/') or (dir_path == '.' and '/' not in ref['file']):
                    folder_keywords[kw].append(ref)

        if folder_keywords:
            sub_lines.append(f"**Total Keywords:** {len(folder_keywords)}\n\n")

            # Group by letter
            by_letter = defaultdict(list)
            for kw in folder_keywords.keys():
                letter = kw[0].upper() if kw else 'Other'
                by_letter[letter].append(kw)

            for letter in sorted(by_letter.keys()):
                sub_lines.append(f"## {letter}\n\n")
                for kw in sorted(by_letter[letter])[:50]:  # Limit per letter
                    refs = folder_keywords[kw]
                    sub_lines.append(f"- **{kw}** (found in {len(refs)} file(s))\n")

        sub_content = ''.join(sub_lines)
        with open(doc_dir / 'sub.md', 'w', encoding='utf-8') as f:
            f.write(sub_content)

        folder_docs_created += 1

    docs_created += folder_docs_created
    print(f"  Created {folder_docs_created} folder documentation files")

    # Step 6: Create global files
    print(f"\n[6/7] Creating global index and keyword files...")

    # Global keywords.md
    print("  Creating keywords.md...")
    kw_lines = []
    kw_lines.append(f"# Global Keywords Index\n\n")
    kw_lines.append(f"**Repository:** {generator.manifest['repo_name']}\n")
    kw_lines.append(f"**Total Keywords:** {len(generator.keywords_global)}\n\n")

    by_letter = defaultdict(list)
    for kw in generator.keywords_global.keys():
        letter = kw[0].upper() if kw else 'Other'
        by_letter[letter].append(kw)

    for letter in sorted(by_letter.keys()):
        kw_lines.append(f"## {letter}\n\n")
        for kw in sorted(by_letter[letter])[:100]:  # Limit per letter
            refs = generator.keywords_global[kw]
            kw_lines.append(f"- **{kw}** - Found in {len(refs)} file(s)\n")
            for ref in refs[:5]:  # Show first 5 refs
                kw_lines.append(f"  - [{ref['file']}]({ref['docs']})\n")
            if len(refs) > 5:
                kw_lines.append(f"  - ... and {len(refs) - 5} more\n")

    kw_content = ''.join(kw_lines)
    with open(Path(docs_root) / 'keywords.md', 'w', encoding='utf-8') as f:
        f.write(kw_content)

    docs_created += 1

    # Root index.md
    print("  Creating root index.md...")
    index_lines = []
    index_lines.append(f"# Documentation Index\n\n")
    index_lines.append(f"**Repository:** {generator.manifest['repo_name']}\n")
    index_lines.append(f"**Commit:** {generator.manifest['commit_sha']}\n")
    index_lines.append(f"**Generated:** {datetime.utcnow().isoformat()}\n\n")

    index_lines.append(f"## Overview\n\n")
    index_lines.append(f"This comprehensive documentation covers all {generator.manifest['files_scanned']} files ")
    index_lines.append(f"in the repository.\n\n")

    index_lines.append(f"## Quick Links\n\n")
    index_lines.append(f"- [Global Keywords Index](keywords.md)\n")
    index_lines.append(f"- [Comprehensive Book](comprehensive_book.md)\n")
    index_lines.append(f"- [Verification Report](verification_report.md)\n")
    index_lines.append(f"- [Root Folder](index.md)\n\n")

    index_lines.append(f"## Folder Structure\n\n")
    for dir_path in all_dirs[:20]:  # First 20 folders
        if dir_path == '.':
            continue
        index_lines.append(f"- [{dir_path}/]({dir_path}/index.md)\n")

    index_content = ''.join(index_lines)
    # Write to root of docs as main index
    with open(Path(docs_root) / 'main_index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)

    docs_created += 1

    # Comprehensive book
    print("  Creating comprehensive_book.md...")
    book_lines = []
    book_lines.append(f"# Python Data Science Handbook - Complete Documentation\n\n")
    book_lines.append(f"**Repository:** {generator.manifest['repo_name']}\n")
    book_lines.append(f"**Commit:** {generator.manifest['commit_sha']}\n")
    book_lines.append(f"**Generated:** {datetime.utcnow().isoformat()}\n\n")

    book_lines.append(f"---\n\n")
    book_lines.append(f"# Introduction\n\n")
    book_lines.append(f"This comprehensive book contains complete documentation for all files ")
    book_lines.append(f"in the Python Data Science Handbook repository.\n\n")

    book_lines.append(f"## Repository Statistics\n\n")
    book_lines.append(f"- Total Files: {generator.manifest['files_scanned']}\n")
    book_lines.append(f"- Text Files: {len(text_files)}\n")
    book_lines.append(f"- Binary Files: {len(binary_files)}\n")
    book_lines.append(f"- Documentation Files Created: {docs_created}\n\n")

    book_lines.append(f"---\n\n")

    # Add folder documentation as chapters
    for dir_path in all_dirs:
        if dir_path == '.':
            doc_dir = Path(docs_root)
        else:
            doc_dir = Path(docs_root) / dir_path

        doc_file = doc_dir / 'doc.md'
        if doc_file.exists():
            book_lines.append(f"# Chapter: {dir_path if dir_path != '.' else 'Root'}\n\n")
            with open(doc_file, 'r', encoding='utf-8') as f:
                book_lines.append(f.read())
            book_lines.append(f"\n\n---\n\n")

    book_content = ''.join(book_lines)
    with open(Path(docs_root) / 'comprehensive_book.md', 'w', encoding='utf-8') as f:
        f.write(book_content)

    docs_created += 1
    total_words += len(book_content.split())

    # Step 7: Verification report
    print(f"\n[7/7] Creating verification report...")

    verif_lines = []
    verif_lines.append(f"# Verification Report\n\n")
    verif_lines.append(f"**Generated:** {datetime.utcnow().isoformat()}\n\n")

    verif_lines.append(f"## Summary\n\n")
    verif_lines.append(f"- Files scanned: {generator.manifest['files_scanned']}\n")
    verif_lines.append(f"- Text files processed: {len(text_files)}\n")
    verif_lines.append(f"- Binary files documented: {len(binary_files)}\n")
    verif_lines.append(f"- Unreadable files: {len(unreadable_files)}\n")
    verif_lines.append(f"- Documentation files created: {docs_created}\n")
    verif_lines.append(f"- Total estimated words: {total_words:,}\n\n")

    if unreadable_files:
        verif_lines.append(f"## Unreadable/Skipped Files\n\n")
        for f in unreadable_files:
            rel = os.path.relpath(f, repo_root)
            verif_lines.append(f"- `{rel}`\n")
        verif_lines.append("\n")

    if generator.verification_issues:
        verif_lines.append(f"## Issues Encountered\n\n")
        for issue in generator.verification_issues:
            verif_lines.append(f"- {issue}\n")
        verif_lines.append("\n")
    else:
        verif_lines.append(f"## Issues\n\nNo issues encountered during generation.\n\n")

    verif_lines.append(f"## File Type Distribution\n\n")
    type_counts = defaultdict(int)
    for file_info in generator.manifest['file_map']:
        type_counts[file_info['type']] += 1

    for file_type, count in sorted(type_counts.items()):
        verif_lines.append(f"- {file_type}: {count}\n")

    verif_content = ''.join(verif_lines)
    with open(Path(docs_root) / 'verification_report.md', 'w', encoding='utf-8') as f:
        f.write(verif_content)

    docs_created += 1

    # Update manifest
    generator.manifest['docs_created'] = docs_created
    generator.manifest['words_estimated'] = total_words
    generator.manifest['timestamp_end'] = datetime.utcnow().isoformat()

    # Calculate total bytes written
    total_bytes = 0
    for root, dirs, files in os.walk(docs_root):
        for file in files:
            if file.endswith('.md'):
                try:
                    total_bytes += os.path.getsize(os.path.join(root, file))
                except:
                    pass

    generator.manifest['bytes_written'] = total_bytes

    # Write manifest
    print("\nWriting manifest.json...")
    with open(Path(docs_root) / 'manifest.json', 'w', encoding='utf-8') as f:
        json.dump(generator.manifest, f, indent=2)

    # Final summary
    print("\n" + "=" * 80)
    print("GENERATION COMPLETE!")
    print("=" * 80)

    summary = {
        "repo_source": generator.manifest['repo_source'],
        "repo_fingerprint": generator.manifest['repo_fingerprint'],
        "files_scanned": generator.manifest['files_scanned'],
        "docs_created": generator.manifest['docs_created'],
        "words_estimated": generator.manifest['words_estimated'],
        "bytes_written": generator.manifest['bytes_written'],
        "errors": generator.verification_issues
    }

    print(json.dumps(summary, indent=2))
    print()

    return summary

if __name__ == '__main__':
    main()
