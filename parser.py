"""Parsing of TODO-style comments."""
import os
import re
from dataclasses import dataclass

KEYWORD_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE)
EXPIRE_RE = re.compile(r"expire\s*[:=]\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)
BARE_DATE_RE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")


@dataclass
class TodoItem:
    path: str
    line: int
    kind: str
    text: str
    expiry: str | None
    expired: bool


def _today():
    override = os.environ.get("TODO_EXPIRE_TODAY")
    if override:
        try:
            from datetime import date

            return date.fromisoformat(override)
        except ValueError:
            pass
    from datetime import date

    return date.today()


def parse_todo_line(path, lineno, line):
    m = KEYWORD_RE.search(line)
    if not m:
        return None
    kind = m.group(1).upper()
    text = line[m.end():].strip().rstrip("\r\n")
    expiry = None
    expired = False
    em = EXPIRE_RE.search(line)
    if em:
        try:
            from datetime import date

            d = date.fromisoformat(em.group(1))
            expiry = d.isoformat()
            expired = d < _today()
        except ValueError:
            pass
    if expiry is None:
        pm = BARE_DATE_RE.search(line)
        if pm:
            try:
                from datetime import date

                d = date.fromisoformat(pm.group(1))
                expiry = d.isoformat()
                expired = d < _today()
            except ValueError:
                pass
    return TodoItem(path=path, line=lineno, kind=kind, text=text, expiry=expiry, expired=expired)
