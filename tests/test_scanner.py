import os
import tempfile
from scanner import scan


def test_scan_dir():
    os.environ["TODO_EXPIRE_TODAY"] = "2025-06-15"
    d = tempfile.mkdtemp()
    p = os.path.join(d, "a.py")
    with open(p, "w") as f:
        f.write("# TODO(expire:2025-01-01): old\n# TODO: fine\n")
    items = scan(d)
    assert len(items) == 2
    assert sum(1 for i in items if i.expired) == 1
