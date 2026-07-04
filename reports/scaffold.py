"""
===============================================================================
File        : scaffold.py
Project     : Government Job Finder
Module      : Reports
Purpose     : Read-only project architecture inspection and documentation tool.

Author      : Sadananda Kumar
Created     : 2026-07-04
Python      : 3.13+

Description
-----------
Scans the Government Job Finder project and generates architecture reports
for developers.

This tool is intended ONLY for development purposes and MUST NEVER be used
as part of the runtime application.

Responsibilities
----------------
✓ Scan complete project structure
✓ Generate project tree
✓ Count folders and files
✓ Count Python modules
✓ Detect empty directories
✓ Detect missing __init__.py files
✓ Generate ARCHITECTURE.txt
✓ Generate scaffold_report.md
✓ Generate dependency_report.md
✓ Generate project_stats.md

Rules
-----
• Read-only by design.
• Never modify application source code.
• Never rename, delete or move project files.
• Only create/update files inside the reports directory.
• Safe to execute multiple times.

Generated Reports
-----------------
reports/
    ├── scaffold.py
    ├── scaffold_report.md
    ├── ARCHITECTURE.txt
    ├── dependency_report.md
    └── project_stats.md

Usage
-----
From the project root:

    python reports/scaffold.py

===============================================================================
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# =============================================================================
# Configuration
# =============================================================================

PROJECT_NAME = "Government Job Finder"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORTS_DIR = PROJECT_ROOT / "reports"

ARCHITECTURE_FILE = REPORTS_DIR / "ARCHITECTURE.txt"

SCAFFOLD_REPORT = REPORTS_DIR / "scaffold_report.md"

DEPENDENCY_REPORT = REPORTS_DIR / "dependency_report.md"

PROJECT_STATS = REPORTS_DIR / "project_stats.md"

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    ".agent_tmp",
    "node_modules",
    ".tox",
    ".eggs",
    "*.egg-info",
}

IGNORE_FILES = {
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".gitignore",
    ".dockerignore",
}

PYTHON_EXTENSIONS = {".py"}

CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".go", ".rs"}

DOC_EXTENSIONS = {".md", ".txt", ".rst", ".adoc"}

CONFIG_EXTENSIONS = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf"}

HEADER_TEMPLATE = """\
===============================================================================
File        : {filename}
Project     : Government Job Finder
Generated   : {timestamp}
Python      : 3.13+
===============================================================================
"""


# =============================================================================
# Utility Functions
# =============================================================================

def should_ignore_dir(name: str) -> bool:
    """Check if directory should be ignored."""
    return name in IGNORE_DIRS or name.startswith(".")


def should_ignore_file(name: str) -> bool:
    """Check if file should be ignored."""
    if name in IGNORE_FILES:
        return True
    for pattern in IGNORE_FILES:
        if pattern.startswith("*") and name.endswith(pattern[1:]):
            return True
    return False


def get_file_category(path: Path) -> str:
    """Categorize file by extension."""
    ext = path.suffix.lower()
    if ext in CODE_EXTENSIONS:
        return "code"
    elif ext in DOC_EXTENSIONS:
        return "doc"
    elif ext in CONFIG_EXTENSIONS:
        return "config"
    else:
        return "other"


def count_lines_of_code(path: Path) -> int:
    """Count non-empty, non-comment lines in a Python file."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        
        code_lines = 0
        in_multiline_string = False
        
        for line in lines:
            stripped = line.strip()
            
            # Toggle multiline string state
            if '"""' in stripped or "'''" in stripped:
                in_multiline_string = not in_multiline_string
                continue
            
            # Skip if in multiline or empty or comment
            if in_multiline_string or not stripped or stripped.startswith("#"):
                continue
            
            code_lines += 1
        
        return code_lines
    except Exception:
        return 0


def parse_requirements(filepath: Path) -> dict:
    """Parse requirements.txt and extract package information."""
    packages = []
    
    if not filepath.exists():
        return {"direct": [], "total": 0, "source": str(filepath)}
    
    try:
        # Try UTF-8 first, then UTF-16 (common in Windows files)
        for encoding in ["utf-8", "utf-16", "utf-16-le", "utf-16-be"]:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    content = f.read()
                    # Test if content looks valid
                    if content and not content.startswith("\ufffd"):
                        break
            except (UnicodeError, UnicodeDecodeError):
                continue
        
        for line in content.splitlines():
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            
            # Parse package name and version
            match = re.match(r"^([a-zA-Z0-9_-]+)(==|>=|<=|~=|!=)?(.+)?$", line)
            if match:
                name = match.group(1)
                operator = match.group(2) or ""
                version = match.group(3) or ""
                packages.append({
                    "name": name,
                    "version": f"{operator}{version}".strip() if operator else "latest"
                })
    except Exception:
        pass
    
    return {
        "direct": packages,
        "total": len(packages),
        "source": str(filepath)
    }


# =============================================================================
# Report Generators
# =============================================================================

def generate_architecture() -> dict:
    """Generate ARCHITECTURE.txt with project structure."""
    
    output_lines = []
    stats = {
        "total_dirs": 0,
        "total_files": 0,
        "python_files": 0,
        "empty_dirs": [],
        "missing_inits": [],
    }
    
    def walk_directory(directory: Path, prefix: str = "", is_last: bool = True):
        """Recursively walk directory and build tree."""
        nonlocal stats
        
        try:
            entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        except PermissionError:
            return
        
        dirs = []
        files = []
        
        for entry in entries:
            if should_ignore_file(entry.name):
                continue
                
            if entry.is_dir():
                if not should_ignore_dir(entry.name):
                    dirs.append(entry)
            else:
                files.append(entry)
        
        # Process directories
        for i, subdir in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and (len(files) == 0)
            connector = "└── " if is_last_dir else "├── "
            
            output_lines.append(f"{prefix}{connector}{subdir.name}/")
            stats["total_dirs"] += 1
            
            # Check if directory is empty
            try:
                if not any(subdir.iterdir()):
                    stats["empty_dirs"].append(str(subdir.relative_to(PROJECT_ROOT)))
            except Exception:
                pass
            
            # Check for __init__.py
            init_file = subdir / "__init__.py"
            if subdir.name != "reports" and not init_file.exists():
                stats["missing_inits"].append(str(subdir.relative_to(PROJECT_ROOT)))
            
            extension = "    " if is_last_dir else "│   "
            walk_directory(subdir, prefix + extension, is_last_dir)
        
        # Process files
        for i, file in enumerate(files):
            is_last_file = (i == len(files) - 1)
            connector = "└── " if is_last_file else "├── "
            
            output_lines.append(f"{prefix}{connector}{file.name}")
            stats["total_files"] += 1
            
            if file.suffix == ".py":
                stats["python_files"] += 1
    
    output_lines.append(f"{PROJECT_ROOT.name}/")
    walk_directory(PROJECT_ROOT, "", True)
    
    # Write to file
    with open(ARCHITECTURE_FILE, "w", encoding="utf-8") as f:
        f.write(HEADER_TEMPLATE.format(
            filename="ARCHITECTURE.txt",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        f.write("\n")
        f.write("Project Structure\n")
        f.write("=================\n\n")
        f.write("\n".join(output_lines))
        f.write("\n\n")
        
        # Summary section
        f.write("Summary\n")
        f.write("-------\n")
        f.write(f"Total directories : {stats['total_dirs']}\n")
        f.write(f"Total files       : {stats['total_files']}\n")
        f.write(f"Python files      : {stats['python_files']}\n")
        
        if stats["empty_dirs"]:
            f.write(f"\nEmpty directories : {len(stats['empty_dirs'])}\n")
            for ed in stats["empty_dirs"]:
                f.write(f"  - {ed}\n")
        
        if stats["missing_inits"]:
            f.write(f"\nMissing __init__.py: {len(stats['missing_inits'])}\n")
            for mi in stats["missing_inits"]:
                f.write(f"  - {mi}\n")
    
    return stats


def generate_scaffold_report(arch_stats: dict) -> dict:
    """Generate scaffold_report.md with analysis results."""
    
    stats = {
        "empty_dirs": arch_stats["empty_dirs"],
        "missing_inits": arch_stats["missing_inits"],
        "warnings": [],
        "recommendations": [],
    }
    
    # Generate warnings
    if stats["empty_dirs"]:
        stats["warnings"].append(f"Found {len(stats['empty_dirs'])} empty directory(s)")
    
    if stats["missing_inits"]:
        stats["warnings"].append(f"Found {len(stats['missing_inits'])} directory(ies) missing __init__.py")
    
    # Generate recommendations
    if stats["empty_dirs"]:
        stats["recommendations"].append(
            "Consider removing empty directories or adding a README.md if intentional"
        )
    
    if stats["missing_inits"]:
        stats["recommendations"].append(
            "Add __init__.py files to make directories proper Python packages"
        )
    
    # Write to file
    with open(SCAFFOLD_REPORT, "w", encoding="utf-8") as f:
        f.write(HEADER_TEMPLATE.format(
            filename="scaffold_report.md",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        f.write("\n")
        f.write("# Scaffold Analysis Report\n\n")
        f.write(f"**Project:** {PROJECT_NAME}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n\n")
        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total Directories | {arch_stats['total_dirs']} |\n")
        f.write(f"| Total Files | {arch_stats['total_files']} |\n")
        f.write(f"| Python Files | {arch_stats['python_files']} |\n")
        f.write(f"| Empty Directories | {len(stats['empty_dirs'])} |\n")
        f.write(f"| Missing __init__.py | {len(stats['missing_inits'])} |\n\n")
        
        if stats["warnings"]:
            f.write("## Warnings\n\n")
            for warning in stats["warnings"]:
                f.write(f"- ⚠️ {warning}\n")
            f.write("\n")
        
        if stats["recommendations"]:
            f.write("## Recommendations\n\n")
            for rec in stats["recommendations"]:
                f.write(f"- 💡 {rec}\n")
            f.write("\n")
        
        if stats["empty_dirs"]:
            f.write("### Empty Directories\n\n")
            f.write("```\n")
            for ed in stats["empty_dirs"]:
                f.write(f"  {ed}\n")
            f.write("```\n\n")
        
        if stats["missing_inits"]:
            f.write("### Missing __init__.py Files\n\n")
            f.write("```\n")
            for mi in stats["missing_inits"]:
                f.write(f"  {mi}/__init__.py\n")
            f.write("```\n\n")
        
        f.write("---\n")
        f.write("*This report is auto-generated by scaffold.py*\n")
    
    return stats


def generate_dependency_report() -> dict:
    """Generate dependency_report.md with package information."""
    
    # Parse requirements
    requirements_path = PROJECT_ROOT / "requirements.txt"
    req_data = parse_requirements(requirements_path)
    
    # Group dependencies by category
    categories = defaultdict(list)
    
    for pkg in req_data["direct"]:
        name = pkg["name"].lower()
        
        if any(x in name for x in ["flask", "django", "fastapi", "bottle"]):
            categories["Web Frameworks"].append(pkg)
        elif any(x in name for x in ["sqlalchemy", "alembic", "psycopg", "mysql", "mongodb"]):
            categories["Database"].append(pkg)
        elif any(x in name for x in ["pandas", "numpy", "scipy", "sklearn", "xgboost"]):
            categories["Data Science"].append(pkg)
        elif any(x in name for x in ["requests", "urllib", "httpx", "aiohttp"]):
            categories["HTTP Clients"].append(pkg)
        elif any(x in name for x in ["pytest", "unittest", "coverage", "tox"]):
            categories["Testing"].append(pkg)
        elif any(x in name for x in ["pillow", "opencv", "matplotlib"]):
            categories["Image Processing"].append(pkg)
        elif any(x in name for x in ["pdf", "docx", "pptx", "openpyxl"]):
            categories["Document Processing"].append(pkg)
        elif any(x in name for x in ["pytesseract", "pdfminer", "pypdf"]):
            categories["PDF Processing"].append(pkg)
        elif any(x in name for x in ["loguru", "structlog"]):
            categories["Logging"].append(pkg)
        else:
            categories["Other"].append(pkg)
    
    # Write to file
    with open(DEPENDENCY_REPORT, "w", encoding="utf-8") as f:
        f.write(HEADER_TEMPLATE.format(
            filename="dependency_report.md",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        f.write("\n")
        f.write("# Dependency Report\n\n")
        f.write(f"**Project:** {PROJECT_NAME}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Source:** {req_data['source']}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total Dependencies:** {req_data['total']}\n")
        f.write(f"- **Categories:** {len(categories)}\n\n")
        
        for category, packages in sorted(categories.items()):
            f.write(f"## {category} ({len(packages)})\n\n")
            f.write("| Package | Version |\n")
            f.write("|---------|--------|\n")
            for pkg in sorted(packages, key=lambda x: x["name"]):
                f.write(f"| `{pkg['name']}` | {pkg['version']} |\n")
            f.write("\n")
        
        f.write("---\n")
        f.write("*This report is auto-generated by scaffold.py*\n")
    
    return {
        "total": req_data["total"],
        "categories": len(categories),
        "category_counts": {k: len(v) for k, v in categories.items()}
    }


def generate_project_stats() -> dict:
    """Generate project_stats.md with code statistics."""
    
    stats = {
        "total_files": 0,
        "code_files": 0,
        "doc_files": 0,
        "config_files": 0,
        "other_files": 0,
        "total_lines": 0,
        "code_lines": 0,
        "largest_files": [],
        "by_extension": defaultdict(int),
    }
    
    file_sizes = []
    
    # Walk through project
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter directories
        dirs[:] = [d for d in dirs if not should_ignore_dir(d)]
        
        root_path = Path(root)
        
        for filename in files:
            if should_ignore_file(filename):
                continue
            
            filepath = root_path / filename
            rel_path = filepath.relative_to(PROJECT_ROOT)
            
            # Get file category
            category = get_file_category(filepath)
            stats[f"{category}_files"] = stats.get(f"{category}_files", 0) + 1
            stats["total_files"] += 1
            
            # Count extension
            stats["by_extension"][filepath.suffix or "no extension"] += 1
            
            # Count lines for Python files
            if filepath.suffix == ".py":
                lines = count_lines_of_code(filepath)
                stats["code_lines"] += lines
                stats["total_lines"] += lines
                file_sizes.append((str(rel_path), lines))
            
            # Get file size for largest files
            try:
                size = filepath.stat().st_size
                file_sizes.append((str(rel_path), size))
            except Exception:
                pass
    
    # Get largest files by lines (Python) and size
    largest_by_lines = sorted(
        [(p, l) for p, l in file_sizes if isinstance(l, int)],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    largest_by_size = sorted(
        [(p, s) for p, s in file_sizes if isinstance(s, int)],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    # Count tests
    test_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT / "tests"):
        for f in files:
            if f.startswith("test_") or f.endswith("_test.py"):
                test_files.append(f)
    
    # Write to file
    with open(PROJECT_STATS, "w", encoding="utf-8") as f:
        f.write(HEADER_TEMPLATE.format(
            filename="project_stats.md",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        f.write("\n")
        f.write("# Project Statistics\n\n")
        f.write(f"**Project:** {PROJECT_NAME}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Overview\n\n")
        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total Files | {stats['total_files']} |\n")
        f.write(f"| Code Files | {stats['code_files']} |\n")
        f.write(f"| Documentation Files | {stats['doc_files']} |\n")
        f.write(f"| Config Files | {stats['config_files']} |\n")
        f.write(f"| Test Files | {len(test_files)} |\n")
        f.write(f"| Total Lines (Code) | {stats['code_lines']:,} |\n\n")
        
        f.write("## File Types by Extension\n\n")
        f.write("| Extension | Count |\n")
        f.write("|-----------|-------|\n")
        for ext, count in sorted(stats["by_extension"].items(), key=lambda x: x[1], reverse=True):
            f.write(f"| `{ext}` | {count} |\n")
        f.write("\n")
        
        if largest_by_lines:
            f.write("## Largest Files (by Lines)\n\n")
            f.write("| File | Lines |\n")
            f.write("|------|-------|\n")
            for path, lines in largest_by_lines:
                f.write(f"| `{path}` | {lines:,} |\n")
            f.write("\n")
        
        if largest_by_size:
            f.write("## Largest Files (by Size)\n\n")
            f.write("| File | Size |\n")
            f.write("|------|------|\n")
            for path, size in largest_by_size:
                if size > 1024 * 1024:
                    size_str = f"{size / (1024*1024):.2f} MB"
                elif size > 1024:
                    size_str = f"{size / 1024:.2f} KB"
                else:
                    size_str = f"{size} B"
                f.write(f"| `{path}` | {size_str} |\n")
            f.write("\n")
        
        f.write("## Code Quality Metrics\n\n")
        f.write(f"- **Average lines per Python file:** {stats['code_lines'] / max(stats['code_files'], 1):.1f}\n")
        f.write(f"- **Test coverage ratio:** {len(test_files) / max(stats['code_files'], 1) * 100:.1f}%\n\n")
        
        f.write("---\n")
        f.write("*This report is auto-generated by scaffold.py*\n")
    
    return stats


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> None:
    """
    Main entry point.
    """

    print("=" * 70)
    print(f"{PROJECT_NAME} - Project Scaffold")
    print("=" * 70)

    print(f"Project Root : {PROJECT_ROOT}")
    print()

    # Generate all reports
    print("Generating ARCHITECTURE.txt...")
    arch_stats = generate_architecture()
    print(f"  ✓ Found {arch_stats['total_dirs']} directories, {arch_stats['total_files']} files")

    print("\nGenerating scaffold_report.md...")
    scaffold_stats = generate_scaffold_report(arch_stats)
    if scaffold_stats["warnings"]:
        for w in scaffold_stats["warnings"]:
            print(f"  ⚠️ {w}")
    else:
        print("  ✓ No issues found")

    print("\nGenerating dependency_report.md...")
    dep_stats = generate_dependency_report()
    print(f"  ✓ Found {dep_stats['total']} dependencies in {dep_stats['categories']} categories")

    print("\nGenerating project_stats.md...")
    stats = generate_project_stats()
    print(f"  ✓ Total: {stats['total_files']} files, {stats['code_lines']:,} lines of code")

    print("\n" + "=" * 70)
    print("Scaffold completed successfully!")
    print(f"Reports saved to: {REPORTS_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()