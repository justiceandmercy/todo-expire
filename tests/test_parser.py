import os
import tempfile
from parser import parse_todo_line


def test_expired_todo():
    os.environ["TODO_EXPIRE_TODAY"] = "2025-06-15"
    it = parse_todo_line("a.py", 1, "# TODO(expire:2025-06-01): remove me\n")
    assert it is not None
    assert it.kind == "TODO"
    assert it.expiry == "2025-06-01"
    assert it.expired is True


def test_not_expired():
    os.environ["TODO_EXPIRE_TODAY"] = "2025-06-15"
    it = parse_todo_line("a.py", 2, "# TODO(expire:2025-12-01): later\n")
    assert it.expired is False


def test_no_expiry():
    os.environ["TODO_EXPIRE_TODAY"] = "2025-06-15"
    it = parse_todo_line("a.py", 3, "# TODO: plain\n")
    assert it.expiry is None
    assert it.expired is False


def test_bare_date():
    os.environ["TODO_EXPIRE_TODAY"] = "2025-06-15"
    it = parse_todo_line("a.py", 4, "// FIXME(2025-01-01) old\n")
    assert it.kind == "FIXME"
    assert it.expired is True


def test_no_todo():
    it = parse_todo_line("a.py", 5, "x = 1\n")
    assert it is None
