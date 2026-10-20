"""Filesystem scanning for TODO comments."""
import os

from parser import parse_todo_line

DEFAULT_EXTS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".cpp",
    ".h", ".rb", ".sh", ".yaml", ".yml", ".toml", ".md", ".html", ".css",
    ".sql", ".php", ".swift", ".kt",
}
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".next", "target", "vendor",
}


def scan(root, exts=None):
    exts = exts if exts is not None else DEFAULT_EXTS
    results = []
    if os.path.isfile(root):
        _scan_file(root, results, exts)
        return results
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in exts:
                _scan_file(os.path.join(dirpath, fn), results, exts)
    return results


def _scan_file(path, results, exts):
    ext = os.path.splitext(path)[1].lower()
    if ext not in exts:
        return
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return
    for idx, line in enumerate(lines, 1):
        item = parse_todo_line(path, idx, line)
        if item:
            results.append(item)
